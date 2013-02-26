# -*- coding: utf-8 -*-
"""
/***************************************************************************
 septima_flow
                                 A QGIS plugin
 Simlulering af væskeudslip på Danmarks Højdmeodel
                              -------------------
        begin                : 2013-02-22
        copyright            : (C) 2013 by Septima
        email                : kontakt@septima.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys, traceback
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from septima_flowdialog import septima_flowDialog

import septima_flow_service

MAX_FEATURES = 500
DEBUG = False

class septima_flow:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/septima_flow"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/septima_flow_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = septima_flowDialog()

        # Instantiate the service
        self.flow_service = septima_flow_service.Septima_Flow_Service()

        self.qgisSettings = QSettings()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/septima_flow/icon.png"),
            u"Septima Væskeudslip", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Septima Væskeudslip", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Septima Væskeudslip", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # Setup dialog
        #list QGIS Layers
    	layerlist = self.get_layers()
    	if len(layerlist)<=0:
    		QMessageBox.warning(None, 'Ingen lag', "Ingen vektorlag er tilgængelige")
    		return
    	self.dlg.ui.lagComboBox.clear()
    	self.dlg.ui.lagComboBox.insertItems(0, [name for name,layer in layerlist])
        self.dlg.ui.resultatLagLineEdit.setText( u"Septima væskeudslip" )


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            alyr = layerlist[self.dlg.ui.lagComboBox.currentIndex()][1]
            selected_only = self.dlg.ui.onlySelectedCheckBox.isChecked()

            if selected_only:
                selected_ids=alyr.selectedFeaturesIds()
                count = len( selected_ids )
            else:
                count = alyr.featureCount ()

            if count < 1:
                QMessageBox.information(None,"Ingen features","Der er 0" + (" valgte " if selected_only else " ") + "features i laget '" + alyr.name() + "'")
                return None

            if count > MAX_FEATURES:
                QMessageBox.information(None,"For mange features","Der er mere end " + str(MAX_FEATURES) + (" valgte " if selected_only else " ") + "features i laget '" + alyr.name() + "'")
                return None

            dlgProgress = QProgressDialog(QString(u'Beregner væskeudslip for ' + str(count) + " features..."), QString('Afbryd'), 0, count) #, self.iface)
            dlgProgress.setWindowModality(Qt.WindowModal)
            dlgProgress.setWindowTitle(u'Septima væskeudslip')

            try:
                outlyr = self.create_memory_layer( self.dlg.ui.resultatLagLineEdit.text(), alyr )
                outlyr.startEditing() # See http://trac.osgeo.org/qgis/ticket/3713

                #selected = alyr.selectedFeatures()
                aprovider = alyr.dataProvider()
                allAttrs = aprovider.attributeIndexes()
                alyr.select( allAttrs )
                srcfeat = QgsFeature()

                flowfound = False
                ix = 0
                while alyr.nextFeature( srcfeat ):
                    if selected_only == True and srcfeat.id() not in selected_ids:
				        continue
                    outfeat = self.process_feature( srcfeat )
                    if not outfeat is None:
                        #print outlyr.dataProvider().fields()
                        outlyr.dataProvider().addFeatures([outfeat])
                        flowfound = True
                    if dlgProgress.wasCanceled(): break
                    dlgProgress.setValue( ix )
                    ix += 1
                    QApplication.processEvents()
                outlyr.commitChanges() # See http://trac.osgeo.org/qgis/ticket/3713
                QgsMapLayerRegistry.instance().addMapLayer( outlyr )
                if flowfound:
                    outlyr.updateExtents()
                    outlyr.reload()
                    ##self.iface.mapCanvas().setExtent( outlyr.extent() )
                    self.iface.mapCanvas().refresh()
            except:
                if DEBUG == True:
                    exc_info = sys.exc_info()
                    print "Unexpected error:"
                    print "  Type: ",   exc_info[0]
                    print "  Value: ",   exc_info[1]
                    print "  Trace:",
                    traceback.print_tb(exc_info[2])
                QMessageBox.information(None,"Fejl",u"Der er opstået en ukendt fejl", QMessageBox.Ok)


            finally:
                dlgProgress.close()

    def create_memory_layer( self, layername, layer_template, crs = None ):
        # http://osgeo-org.1560.n6.nabble.com/Cleanly-create-memory-layer-in-Python-td4107077.html
        # Temporarily turn off  QGIS asking user for CRS
##        projectionSettingKey = "Projections/defaultBehaviour"
##        oldProjectionSetting = self.qgisSettings.value(projectionSettingKey)
##        self.qgisSettings.setValue(projectionSettingKey, "useGlobal")
##        try:
##            self.qgisSettings.sync()
##            layer = QgsVectorLayer("LineString?crs=epsg:25832", layername, "memory")
####            if crs:
####                crs = QgsCoordinateReferenceSystem(crs, QgsCoordinateReferenceSystem.PostgisCrsId)
####            else:
####                crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
##            crs = QgsCoordinateReferenceSystem(25832, QgsCoordinateReferenceSystem.EpsgCrsId)
##            layer.setCrs(crs)
##        finally:
##            # Reenable QGIS setting
##            self.qgisSettings.setValue(projectionSettingKey, oldProjectionSetting)
##            self.qgisSettings.sync()
        layer = QgsVectorLayer("LineString?crs=epsg:25832", layername, "memory")
        layer.startEditing()  # See http://trac.osgeo.org/qgis/ticket/3713
        srcfields = layer_template.dataProvider().fields()

        layer.dataProvider().addAttributes( [srcfields[ix] for ix in xrange(len(srcfields))] ) # In QGIS 1.8 srcfields is a dict like {0: field, 1: field....}! In 1.9 it is like [field, field]
        layer.commitChanges()  # See http://trac.osgeo.org/qgis/ticket/3713
        if DEBUG == True:
            print "Source layer fields: "
            print [ f.name() for f in layer_template.dataProvider().fields() ]
            print "Memory layer fields: "
            print [ f.name() for f in layer.dataProvider().fields() ]

        return layer


    def process_feature(self, feature):
        geom = self.flow_service.get_flow( feature.geometry() )
        if geom is None:
            return None
        outfeat = QgsFeature()
        outfeat.setGeometry( geom )

        # Copy attribute values
        if hasattr(QgsFeature, 'attributes') and callable(getattr(QgsFeature, 'attributes')):
            # QGis 1.9
            outfeat.setAttributes( feature.attributes() )
            outfeat.setFields( feature.fields() )
        else:
            # QGis 1.8
            outfeat.setAttributeMap( feature.attributeMap() )
        if DEBUG == True:
            print "Source feature: "
            self.print_feature( feature, "  " )
            print "Processed feature: "
            self.print_feature( outfeat, "  " )
        return outfeat

    def get_layers(self):
    	layermap = QgsMapLayerRegistry.instance().mapLayers()
    	layerlist = []
    	for name, layer in layermap.iteritems():
    		if layer.type() == QgsMapLayer.VectorLayer:
    			layerlist.append( [unicode( layer.name() ),layer] )
    	return layerlist

    def print_feature( self, feature, padleft = "" ):
        geom = feature.geometry()
        print str(padleft) + "Geom: " + geom.exportToWkt()[:100]
        print str(padleft) + "Attributes:"
##
##        fields = feature.fields()
##        if not fields is None:

##            for f in fields:
##                print "  %s: " % f.name(), feature.attribute( f )
        # fetch map of attributes
        if hasattr(QgsFeature, 'attributes') and callable(getattr(QgsFeature, 'attributes')):
            attrs = feature.attributes()
            fields = feature.fields()
            for ix in xrange(len(attrs)):
                print str(padleft) + "  %s: %s" % (fields[ix].name(), attrs[ix].toString())

        else:
            attrs = feature.attributeMap()
            # attrs is a dictionary: key = field index, value = QgsFeatureAttribute
            # show all attributes and their values
            for (k,attr) in attrs.iteritems():
                print str(padleft) + "  %d: %s" % (k, attr.toString())