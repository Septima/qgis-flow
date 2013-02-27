# -*- coding: utf-8 -*-
"""
/***************************************************************************
 septima_flow
                                 A QGIS plugin
 Simulering af væskeudslip på Danmarks Højdmeodel
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return u"Septima Væskeudslip"


def description():
    return u"Simulering af væskeudslip på Danmarks Højdmeodel"


def version():
    return "Version 0.1.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Septima"

def email():
    return "kontakt@septima.dk"

def classFactory(iface):
    # load septima_flow class from file septima_flow
    from septima_flow import septima_flow
    return septima_flow(iface)
