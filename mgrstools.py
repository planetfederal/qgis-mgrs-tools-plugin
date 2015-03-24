# -*- coding: utf-8 -*-

import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from maptool import MGRSMapTool
from coorddialog import MGRSCoordInputDialog

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

        self.zoomTo = MGRSCoordInputDialog(self.iface.mapCanvas(), self.iface.mainWindow())
        self.iface.addDockWidget(Qt.TopDockWidgetArea, self.zoomTo)
        self.zoomTo.hide()

    def zoomTo(self):
        self.zoomTo.show()

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
   
