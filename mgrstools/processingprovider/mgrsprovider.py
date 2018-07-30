# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.

import os

from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from mgrstools.processingprovider.addmgrsfield import AddMgrsField
from mgrstools.processingprovider.layerfrommgrstable import LayerFromMgrsTable
from processing.core.ProcessingConfig import Setting, ProcessingConfig

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class MgrsProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

    def load(self):
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        ProcessingConfig.addSetting(Setting(self.name(), 'ACTIVATE_MGRS',
                                            'Activate', False))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        pass

    def isActive(self):
        """Return True if the provider is activated and ready to run algorithms"""
        return ProcessingConfig.getSetting('ACTIVATE_MGRS')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('ACTIVATE_MGRS', active)

    def id(self):
        return 'mgrs'

    def name(self):        
        return 'MGRS Tools'

    def icon(self):        
        return QIcon(os.path.join(pluginPath, 'icons', 'mgrs.svg'))

    def loadAlgorithms(self):
        for alg in [AddMgrsField(), LayerFromMgrsTable()]:
            self.addAlgorithm(alg)

