# -*- coding: utf-8 -*-

# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.


import os

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QIcon

try:
    from qgis.core import  Qgis
except ImportError:
    from qgis.core import  QGis as Qgis

from qgis.core import (QgsVectorDataProvider,
                       QgsField,
                       QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform
                      )

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from processing.core.parameters import ParameterVector
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector

from mgrspy import mgrs

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class AddMgrsField(GeoAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def getIcon(self):
        return QIcon(os.path.join(pluginPath, 'icons', 'mgrs.svg'))

    def defineCharacteristics(self):
        self.name = 'Add MGRS field to points layer'
        self.i18n_name = self.tr(self.name)
        self.group = 'MGRS tools'
        self.i18n_group = self.tr(self.group)

        if Qgis.QGIS_VERSION_INT < 29900:
            self.addParameter(ParameterVector(self.INPUT,
                                              self.tr('Input layer'),
                                              [ParameterVector.VECTOR_TYPE_POINT]))
        else:
            self.addParameter(ParameterVector(self.INPUT,
                                              self.tr('Input layer'),
                                              [dataobjects.TYPE_VECTOR_POINT]))
        self.addOutput(OutputVector(self.OUTPUT, self.tr('Output'), True))

    def processAlgorithm(self, progress):
        filename = self.getParameterValue(self.INPUT)
        layer = dataobjects.getObjectFromUri(filename)
        provider = layer.dataProvider()

        caps = provider.capabilities()
        if not (caps & QgsVectorDataProvider.AddAttributes):
            raise GeoAlgorithmExecutionException('The selected layer does not '
                                                ' support adding new attributes.')

        fields = layer.fields()
        idxField = fields.indexFromName('MGRS')
        if idxField == -1:
            provider.addAttributes([QgsField('MGRS', QVariant.String)])
            layer.updateFields()
            idxField = len(fields)

        epsg4326 = QgsCoordinateReferenceSystem('EPSG:4326')
        transform = QgsCoordinateTransform(layer.crs(), epsg4326)

        features = vector.features(layer)
        total = 100.0 / float(len(features))
        for i, feat in enumerate(features):
            pt = feat.geometry().asPoint()
            try:
                pt4326 = transform.transform(pt.x(), pt.y())
                mgrsCoord = mgrs.toMgrs(pt4326.y(), pt4326.x())
            except Exception as e :
                mgrsCoord = ''

            provider.changeAttributeValues({feat.id() : {idxField: mgrsCoord}})

        self.setOutputValue(self.OUTPUT, filename)
