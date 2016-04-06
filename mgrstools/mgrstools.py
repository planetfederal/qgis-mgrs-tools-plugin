# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import math
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

mgrsOk=True
try:
    import mgrs
    from maptool import MGRSMapTool
    from coorddialog import MGRSCoordInputDialog
except ImportError:
    raise
    mgrsOk = False


class MGRSTools:

    def __init__(self, iface):
        self.iface = iface        
        try:
            from tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "MGRS tools")
        except:
            pass        

    def initGui(self):
        if mgrsOk:
            self.mapTool = MGRSMapTool(self.iface.mapCanvas())
            self.iface.mapCanvas().mapToolSet.connect(self.unsetTool)

        mapToolIcon = QIcon(os.path.join(os.path.dirname(__file__), "mgrs.svg"))
        self.toolAction = QAction(mapToolIcon, "MGRS map tool",
                                     self.iface.mainWindow())        
        self.toolAction.triggered.connect(self.setTool)
        self.toolAction.setCheckable(True)
        self.iface.addToolBarIcon(self.toolAction)
        self.iface.addPluginToMenu("MGRS", self.toolAction)

        zoomToIcon = QIcon(':/images/themes/default/mActionZoomIn.svg')
        self.zoomToAction = QAction(zoomToIcon, "Zoom to MGRS coordinate",
                                     self.iface.mainWindow())        
        self.zoomToAction.triggered.connect(self.zoomTo)
        self.iface.addPluginToMenu("MGRS", self.zoomToAction)

        if mgrsOk:
            self.zoomToDialog = MGRSCoordInputDialog(self.iface.mapCanvas(), self.iface.mainWindow())
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.zoomToDialog)
            self.zoomToDialog.hide()

    def zoomTo(self):
        if mgrsOk:
            self.zoomToDialog.show()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "MRGS Tools", 
                "Cannot load mgrs library.\nOnly OSX and Win32 systems supported.")


    def unsetTool(self, tool):
        try:
            if not isinstance(tool, MGRSMapTool):
                self.toolAction.setChecked(False)
        except:
            pass
            #ignore exceptions thrown when unloading plugin, since map tool class might not exist already


    def setTool(self):
        if mgrsOk:
            self.toolAction.setChecked(True)
            self.iface.mapCanvas().setMapTool(self.mapTool)
        else:
            QMessageBox.warning(self.iface.mainWindow(), "MRGS Tools", 
                "Cannot load mgrs library.\nOnly OSX and Win32 systems supported.")

    def unload(self):
        if mgrsOk:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)
            self.iface.removeDockWidget(self.zoomToDialog) 
            self.zoomToDialog = None
        self.iface.removeToolBarIcon(self.toolAction)
        self.iface.removePluginMenu("MGRS", self.toolAction)
        self.iface.removePluginMenu("MGRS", self.zoomToAction)
        
