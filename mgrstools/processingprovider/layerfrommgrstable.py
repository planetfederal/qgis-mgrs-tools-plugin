# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os
from qgis.core import (QgsApplication,
                       QgsWkbTypes,
                       QgsPoint,
                       QgsFeatureRequest,
                       QgsGeometry,
                       QgsProcessing,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterField,
                       QgsCoordinateReferenceSystem)
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm

from mgrspy import mgrs

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class LayerFromMgrsTable(QgisAlgorithm):

    INPUT = 'INPUT'
    FIELD = 'FIELD'
    OUTPUT = 'OUTPUT'

    def tags(self):
        return self.tr('points,create,values,attributes').split(',')

    def group(self):
        return self.tr('MGRS Tools')

    def groupId(self):
        return 'mgrs'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT, self.tr('Input layer'), types=[QgsProcessing.TypeVector]))
        self.addParameter(QgsProcessingParameterField(self.FIELD,
                                                      self.tr('M field'), parentLayerParameterName=self.INPUT, type=QgsProcessingParameterField.String))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Points from table'), type=QgsProcessing.TypeVectorPoint))

    def name(self):
        return 'createpointslayerfrommgrstable'

    def displayName(self):
        return self.tr('Create points layer from table with MGRS coordinates')

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        fields = source.fields()
        idx = fields.lookupField(self.parameterAsString(parameters, self.FIELD, context))

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               source.fields(), QgsWkbTypes.Point,
                                               QgsCoordinateReferenceSystem("EPSG:4326"))

        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        for current, feature in enumerate(features):
            if feedback.isCanceled():
                break

            feedback.setProgress(int(current * total))
            attrs = feature.attributes()

            try:
                mgrsCoord = feature[idx]
                y, x = mgrs.toWgs(mgrsCoord)
                point = QgsPoint(x, y)
                feature.setGeometry(QgsGeometry(point))
            except:
                pass

            sink.addFeature(feature)

        return {self.OUTPUT: dest_id}
