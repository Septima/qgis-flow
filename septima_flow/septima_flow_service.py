#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Asger
#
# Created:     22-02-2013
# Copyright:   (c) Asger 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import qgis.core
import urllib2

class Septima_Flow_Service:
    #server_url = r'http://wps.septima.dk/cgi-bin/zoo_loader.cgi?request=execute&service=wps&identifier=FlowPath2&version=1.0.0&RawDataOutput=FlowPath@mimeType=application/wkt&DataInputs=Geometry={"type":"Polygon","coordinates":[[[659449.3452846328,6200781.954781047],[659451.3901699438,6200782.389434838],[659453.3,6200783.239745962],[659454.9913060636,6200784.468551746],[659456.3901699438,6200786.022147478],[659457.4354545765,6200787.83263357],[659458.0814760074,6200789.8208830925],[659458.3,6200791.9],[659458.0814760074,6200793.979116908],[659457.4354545765,6200795.967366431],[659456.3901699438,6200797.777852523],[659454.9913060636,6200799.331448255],[659453.3,6200800.560254038],[659451.3901699438,6200801.410565163],[659449.3452846328,6200801.845218954],[659447.2547153673,6200801.845218954],[659445.2098300563,6200801.410565163],[659443.3,6200800.560254038],[659441.6086939365,6200799.331448255],[659440.2098300563,6200797.777852523],[659439.1645454236,6200795.967366431],[659438.5185239927,6200793.979116908],[659438.3,6200791.9],[659438.5185239927,6200789.8208830925],[659439.1645454236,6200787.83263357],[659440.2098300563,6200786.022147478],[659441.6086939365,6200784.468551746],[659443.3,6200783.239745962],[659445.2098300563,6200782.389434838],[659447.2547153673,6200781.954781047],[659449.3452846328,6200781.954781047]]]}@dataType=string;MaxPathDistance=5000'
    server_url = r'http://wps.septima.dk/cgi-bin/zoo_loader.cgi?'
    request_template = r'request=execute&service=wps&identifier=FlowPath2&version=1.0.0&RawDataOutput=FlowPath@mimeType=application/wkt&DataInputs=%s'
    datainputs_template = r'Geometry=%s@dataType=string@mimeType=application/wkt;MaxPathDistance=%s'

    def __init__(self):
        pass

    def get_flow(self, qgis_geometry, max_path_distance = 1000.0):
        if qgis_geometry is None:
            return None
        jsongeom = qgis_geometry.exportToWkt()

        datainputs = self.datainputs_template % (jsongeom,max_path_distance)
        datainputs = urllib2.quote( datainputs )

        url = self.server_url + self.request_template %  datainputs
        #qgis.core.QgsMessageLog.logMessage('Url: ' + url, "Septima Flow")
        req = urllib2.Request( url )
        u = urllib2.urlopen(req)
        data = u.read()
        geom =  qgis.core.QgsGeometry.fromWkt( data )
        #qgis.core.QgsMessageLog.logMessage('Url: ' + url, "Septima Flow")
        #qgis.core.QgsMessageLog.logMessage('Response: ' + data, "Septima Flow")
        #qgis.core.QgsMessageLog.logMessage('Geom: ' + geom.exportToWkt(), "Septima Flow")
        return geom

def main():
    s = Septima_Flow_Service()
    g = s.get_flow( qgis.core.QgsGeometry.fromWkt( 'POINT(655138.51 6203775.6)') )
    print g.exportToWkt()

if __name__ == '__main__':
    main()
