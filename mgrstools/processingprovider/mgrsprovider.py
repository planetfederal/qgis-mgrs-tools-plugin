# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.

import os

from PyQt4.QtGui import QIcon

from processing.core.AlgorithmProvider import AlgorithmProvider
from mgrstools.processingprovider.addmgrsfield import AddMgrsField

pluginPath = os.path.split(os.path.dirname(__file__))[0]


class MgrsProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        self.activate = True

        # Load algorithms
        self.alglist = [AddMgrsField()]
        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)

    def unload(self):
        AlgorithmProvider.unload(self)

    def getName(self):
        return 'mgrs'

    def getDescription(self):
        return 'MGRS tools'

    def getIcon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'mgrs.svg'))

    def _loadAlgorithms(self):
        self.algs = self.alglist
