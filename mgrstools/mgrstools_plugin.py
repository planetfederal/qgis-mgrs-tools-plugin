from builtins import object
# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os

from qgis.PyQt.QtCore import Qt, QCoreApplication, QUrl
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox

from qgis.core import QgsApplication

from mgrstools.maptool import MGRSMapTool
from mgrstools.gui.mgrsdock import MgrsDockWidget
from mgrstools.processingprovider.mgrsprovider import MgrsProvider

from qgiscommons2.gui import (addAboutMenu,
                             removeAboutMenu,
                             addHelpMenu,
                             removeHelpMenu)

pluginPath = os.path.dirname(__file__)


class MGRSToolsPlugin(object):

    def __init__(self, iface):
        self.iface = iface
        try:
            from mgrstools.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, 'MGRS tools')
        except:
            pass

        self.provider = MgrsProvider()

    def initGui(self):
        self.mapTool = MGRSMapTool(self.iface.mapCanvas())
        self.iface.mapCanvas().mapToolSet.connect(self.unsetTool)

        self.toolAction = QAction(QIcon(os.path.join(pluginPath, 'icons', 'mgrs.svg')),
                                  'MGRS map tool',
                                  self.iface.mainWindow())
        self.toolAction.setCheckable(True)
        self.iface.addToolBarIcon(self.toolAction)
        self.iface.addPluginToMenu('MGRS', self.toolAction)
        self.toolAction.triggered.connect(self.setTool)

        zoomToIcon = QIcon(':/images/themes/default/mActionZoomIn.svg')
        self.zoomToAction = QAction(zoomToIcon,
                                    'Zoom to MGRS coordinate',
                                    self.iface.mainWindow())
        self.iface.addPluginToMenu('MGRS', self.zoomToAction)
        self.zoomToAction.triggered.connect(self.zoomTo)

        addHelpMenu("MGRS", self.iface.addPluginToMenu)
        addAboutMenu("MGRS", self.iface.addPluginToMenu)

        self.mgrsDock = MgrsDockWidget(self.iface.mapCanvas(), self.iface.mainWindow())
        self.iface.addDockWidget(Qt.TopDockWidgetArea, self.mgrsDock)
        self.mgrsDock.hide()

        try:
            from lessons import addLessonsFolder, addGroup
            folder = os.path.join(os.path.dirname(__file__), "_lessons")
            addLessonsFolder(folder, "MGRS tools")
        except:
            pass

        QgsApplication.processingRegistry().addProvider(self.provider)

    def zoomTo(self):
        self.mgrsDock.show()

    def unsetTool(self, tool):
        try:
            if not isinstance(tool, MGRSMapTool):
                self.toolAction.setChecked(False)
        except:
            # Ignore exceptions thrown when unloading plugin, since map
            # tool class might not exist already
            pass

    def setTool(self):
        self.toolAction.setChecked(True)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def unload(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.iface.removeDockWidget(self.mgrsDock)
        self.mgrsDock = None
        self.iface.removeToolBarIcon(self.toolAction)
        self.iface.removePluginMenu('MGRS', self.toolAction)
        self.iface.removePluginMenu('MGRS', self.zoomToAction)

        removeHelpMenu("MGRS")
        removeAboutMenu("MGRS")

        QgsApplication.processingRegistry().removeProvider(self.provider)

        try:
            from mgrstools.tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, 'MGRS tools')
        except:
            pass

        try:
            from lessons import removeLessonsFolder
            folder = os.path.join(pluginPath, '_lessons')
            removeLessonsFolder(folder)
        except:
            pass
