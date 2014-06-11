# -*- coding: utf-8 -*-

import mgrs
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from maptool import MGRSMapTool
from coorddialog import MGRSCoordInputDialog
from qgis.utils import iface

class MGRSTools:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.mapTool = MGRSMapTool(self.iface.mapCanvas())
        
        self.menu = QMenu(self.iface.mainWindow().menuBar())        
        self.menu.setTitle("MGRS Tools")

        self.toolAction = QAction("MGRS map tool",
                                     self.iface.mainWindow())        
        self.toolAction.triggered.connect(self.setTool)
        self.toolAction.setCheckable(True)
        self.menu.addAction(self.toolAction)

        self.zoomToAction = QAction("Zoom to MGRS coordinate",
                                     self.iface.mainWindow())        
        self.zoomToAction.triggered.connect(self.zoomTo)
        self.menu.addAction(self.zoomToAction)

        menuBar = self.iface.mainWindow().menuBar()
        menuBar.insertMenu(
            self.iface.firstRightStandardMenu().menuAction(), self.menu)

        self.iface.mapCanvas().mapToolSet.connect(self.unsetTool)

    def zoomTo(self):
        dlg = MGRSCoordInputDialog(self.iface.mainWindow())
        dlg.exec_()
        if dlg.latlon is not None:                 
            lat, lon = dlg.latlon
            canvas = iface.mapCanvas()
            canvasCrs = canvas.mapRenderer().destinationCrs() 
            epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            transform = QgsCoordinateTransform(epsg4326, canvasCrs)
            pt = transform.transform(lon, lat) 
            extent = canvas.extent()
            w = extent.width()/2.0
            h = extent.height()/2.0
            newExtent = QgsRectangle(pt.x() - w, pt.y() - h, pt.x() + w, pt.y() + h)
            canvas.setExtent(newExtent)
            canvas.refresh()

    def unsetTool(self, tool):
        if not isinstance(tool, MGRSMapTool):
            self.toolAction.setChecked(False)

    def setTool(self):
        self.toolAction.setChecked(True)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def unload(self):
        self.menu.deleteLater()
   
