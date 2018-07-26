# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os

from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsProcessingException,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform,
                       QgsField,
                       QgsProject,
                       QgsFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from processing.algs.qgis.QgisAlgorithm import QgisAlgorithm

from mgrspy import mgrs

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class AddMgrsField(QgisAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def group(self):
        return self.tr('MGRS Tools')

    def groupId(self):
        return 'mgrs'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT, self.tr('Input layer')))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT,
                                                            self.tr('Output')))

    def name(self):
        return 'addmgrsfield'

    def displayName(self):
        return self.tr('Add MGRS Field')

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)        
        fields = source.fields()
        field = QgsField("MGRS", QVariant.String)
        fields.append(field)
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
                                               fields, source.wkbType(), source.sourceCrs())

        features = source.getFeatures()
        total = 100.0 / source.featureCount() if source.featureCount() else 0

        epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')
        transform = QgsCoordinateTransform(source.sourceCrs(), epsg4326, QgsProject.instance())

        for current, feat in enumerate(features):
            if feedback.isCanceled():
                break

            feedback.setProgress(int(current * total))
            attrs = feat.attributes()
            pt = feat.geometry().centroid().asPoint()
            try:
                pt4326 = transform.transform(pt.x(), pt.y())
                mgrsCoord = mgrs.toMgrs(pt4326.y(), pt4326.x())
            except Exception as e :
                mgrsCoord = ''

            attrs.append(mgrsCoord)
            feat.setAttributes(attrs)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}
