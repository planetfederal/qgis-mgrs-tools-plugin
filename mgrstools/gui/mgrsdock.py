from builtins import str
# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDockWidget
from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.gui import QgsVertexMarker

from mgrspy import mgrs

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'mgrsdockwidgetbase.ui'))


class MgrsDockWidget(BASE, WIDGET):

    epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')

    def __init__(self, canvas, parent=None):
        super(MgrsDockWidget, self).__init__(parent)
        self.setupUi(self)

        self.canvas = canvas
        self.marker = None

        self.btnZoom.setIcon(QIcon(':/images/themes/default/mActionZoomIn.svg'))
        self.btnRemoveMarker.setIcon(QIcon(':/images/themes/default/mIconDelete.svg'))

        self.leMgrsCoordinate.returnPressed.connect(self.zoomToPressed)
        self.btnZoom.clicked.connect(self.zoomToPressed)
        self.btnRemoveMarker.clicked.connect(self.removeMarker)
        self.btnRemoveMarker.setDisabled(True)

    def zoomToPressed(self):
        mgrsCoord = str(self.leMgrsCoordinate.text()).strip()
        lat, lon = mgrs.toWgs(mgrsCoord)
        canvasCrs = self.canvas.mapSettings().destinationCrs()
        transform4326 = QgsCoordinateTransform(self.epsg4326, canvasCrs, QgsProject.instance())
        center = transform4326.transform(lon, lat)
        self.canvas.zoomByFactor(1, center)
        self.canvas.refresh()
        if self.marker is None:
            self.marker = QgsVertexMarker(self.canvas)
        self.marker.setCenter(center)
        self.marker.setIconSize(8)
        self.marker.setPenWidth(4)
        self.btnRemoveMarker.setDisabled(False)

    def removeMarker(self):
        self.canvas.scene().removeItem(self.marker)
        self.marker = None

    def closeEvent(self, evt):
        if self.marker is not None:
            self.canvas.scene().removeItem(self.marker)
            self.marker = None
