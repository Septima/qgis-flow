# -*- coding: utf-8 -*-
"""
/***************************************************************************
 septima_flowDialog
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

from PyQt4 import QtCore, QtGui
from ui_septima_flow import Ui_septima_flow
# create the dialog for zoom to point


class septima_flowDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_septima_flow()
        self.ui.setupUi(self)
