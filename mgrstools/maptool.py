# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#

from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MGRSMapTool(QgsMapTool):

    import mgrs
    ct = mgrs.MGRS()
    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.setCursor(Qt.CrossCursor)

    def toMgrs(self, pt):
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, self.epsg4326)
        pt4326 = transform.transform(pt.x(), pt.y())
        try:
            mgrsCoords = self.ct.toMGRS(pt4326.y(), pt4326.x())
        except:
            mgrsCoords = None

        return mgrsCoords

    def canvasMoveEvent(self, e):
        pt = self.toMapCoordinates(e.pos())
        mgrsCoord = self.toMgrs(pt)
        if mgrsCoord:
            iface.mainWindow().statusBar().showMessage("MGRS Coordinate: " + mgrsCoord)
        else:
            iface.mainWindow().statusBar().showMessage("")


    def canvasReleaseEvent(self, e):
        pt = self.toMapCoordinates(e.pos())
        mgrsCoord = self.toMgrs(pt)
        if mgrsCoord:
            clipboard = QApplication.clipboard()
            clipboard.setText(mgrsCoord)
            iface.messageBar().pushMessage("", "Coordinate %s copied to clipboard" % mgrsCoord, level=QgsMessageBar.INFO, duration=3)

