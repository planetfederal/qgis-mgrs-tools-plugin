# -*- coding: utf-8 -*-

import mgrs
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
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
            transform4326 = QgsCoordinateTransform(epsg4326, canvasCrs)
            center = transform4326.transform(lon, lat)             
            precision = 5 - math.floor((len(dlg.mgrsCoord) - 5) / 2) 
            dist = math.pow(10, precision) / 2
            R = 6378137
            dLat = dist / R
            dLon = dist / (R * math.cos(math.pi * lat / 180))
            pt1 = transform4326.transform(lon - dLon * 180 / math.pi , lat - dLat * 180 / math.pi) 
            pt2 = transform4326.transform(lon + dLon * 180 / math.pi , lat + dLat * 180 / math.pi)
            newExtent = QgsRectangle(pt1.x(), pt1.y(), pt2.x(), pt2.y())
            canvas.setExtent(newExtent)
            canvas.refresh()
            m = QgsVertexMarker(canvas)
            m.setCenter(center)
            m.setIconSize(8)
            m.setPenWidth(4)

            def timer_fired():
                self.iface.mapCanvas().scene().removeItem(m)
                timer.stop()
             
            timer = QTimer()
            timer.timeout.connect(timer_fired)
            timer.setSingleShot(True)
            timer.start(5000)

    def unsetTool(self, tool):
        try:
            if not isinstance(tool, MGRSMapTool):
                self.toolAction.setChecked(False)
        except:
            pass
            #ignore exceptions thrown when unloading plugin, since map tool class might not exist already


    def setTool(self):
        self.toolAction.setChecked(True)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def unload(self):
        self.menu.deleteLater()
   
