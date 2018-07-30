# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, Qgis
from qgis.gui import QgsMessageBar, QgsMapTool
from qgis.utils import iface

from mgrspy import mgrs

class MGRSMapTool(QgsMapTool):

    epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.setCursor(Qt.CrossCursor)

    def toMgrs(self, pt):
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, self.epsg4326, QgsProject.instance())
        pt4326 = transform.transform(pt.x(), pt.y())
        try:
            mgrsCoords = mgrs.toMgrs(pt4326.y(), pt4326.x())
        except Exception as e:
            mgrsCoords = None

        return mgrsCoords

    def canvasMoveEvent(self, e):
        pt = self.toMapCoordinates(e.pos())
        mgrsCoord = self.toMgrs(pt)
        if mgrsCoord:
            iface.statusBarIface().showMessage(self.tr('MGRS Coordinate: {}'.format(mgrsCoord)))
        else:
            iface.statusBarIface().showMessage('')

    def canvasReleaseEvent(self, e):
        pt = self.toMapCoordinates(e.pos())
        mgrsCoord = self.toMgrs(pt)
        if mgrsCoord:
            clipboard = QApplication.clipboard()
            clipboard.setText(mgrsCoord)
            iface.messageBar().pushMessage(self.tr('MGRS Tools'),
                                           self.tr('Coordinate "{}" copied to clipboard'.format(mgrsCoord)),
                                           level=Qgis.Info,
                                           duration=3)
