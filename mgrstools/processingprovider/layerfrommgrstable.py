# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon

try:
    from qgis.core import  QGis
except ImportError:
    from qgis.core import  Qgis as QGis

from qgis.core import QgsCoordinateReferenceSystem, QgsPoint, QgsFeature, QgsGeometry

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterTable, ParameterTableField
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector

from mgrspy import mgrs

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class LayerFromMgrsTable(GeoAlgorithm):

    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OUTPUT = 'OUTPUT'

    def getIcon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'mgrs.svg'))

    def defineCharacteristics(self):
        self.name = 'Create vector layer from table with MGRS field'
        self.i18n_name = self.tr(self.name)
        self.group = 'MGRS tools'
        self.i18n_group = self.tr(self.group)

        self.addParameter(ParameterTable(self.INPUT,
                                         self.tr('Input table')))
        self.addParameter(ParameterTableField(self.FIELD,
                                              self.tr('MGRS field'),
                                              self.INPUT,
                                              ParameterTableField.DATA_TYPE_STRING))
        self.addOutput(OutputVector(self.OUTPUT, self.tr('Output')))

    def processAlgorithm(self, progress):
        layer = dataobjects.getObjectFromUri(
                self.getParameterValue(self.INPUT))
        field = self.getParameterValue(self.FIELD)
        output = self.getOutputFromName(self.OUTPUT)

        idx = layer.fieldNameIndex(field)
        fields = layer.fields()

        epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')

        if QGis.QGIS_VERSION_INT < 29900:
            writer = output.getVectorWriter(fields, QGis.WKBPoint, epsg4326)
        else:
            from qgis.core import QgsWkbTypes
            writer = output.getVectorWriter(fields, QgsWkbTypes.Point, epsg4326)

        features = vector.features(layer)
        total = 100.0 / len(features)

        outFeat = QgsFeature()
        for current, feature in enumerate(features):
            try:
                mgrsCoord = feature[idx]
                y, x = mgrs.toWgs(mgrsCoord)
            except:
                pass

            pt = QgsPoint(x, y)
            outFeat.setGeometry(QgsGeometry.fromPoint(pt))
            outFeat.setAttributes(feature.attributes())
            writer.addFeature(outFeat)
            progress.setPercentage(int(current * total))

        del writer
