# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin

import os
from qgis.core import QgsProject
from qgis.utils import plugins, iface
from qgiscommons2.layers import loadLayer

def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    def _loadLayer():
        layerfile = os.path.join(os.path.dirname(__file__), "data", "clean_MGRS_100kmSQ_ID_02H.shp")
        layer = loadLayer(layerfile, provider="ogr")
        QgsProject.instance().addMapLayer(layer)

    def _loadTestProject(fileName='general'):
        projectFile = os.path.join(os.path.dirname(__file__), 'data', fileName + '.qgs')
        currentProjectFile = QgsProject.instance().fileName()
        if os.path.normpath(currentProjectFile) != os.path.normpath(projectFile):
            iface.addProject(projectFile)

    def _setTool():
        plugins["mgrstools"].setTool()

    def _zoomTo():
        plugins["mgrstools"].zoomTo()

    mgrsMaptool = Test("Test MRGS map tool")
    mgrsMaptool.addStep("Load test project", lambda: _loadTestProject("map_tools_test"))
    mgrsMaptool.addStep("Select map tool", _setTool)
    mgrsMaptool.addStep("Click within the upper left polygon. Verify that the computed mrgrs coord starts with 02HLJ'", isVerifyStep=True)
    mgrsMaptool.addStep("Open a text editor and press 'Ctrl+V'. Confirm that the computed coordinate is pasted", isVerifyStep=True)

    mgrsZoomPanel = Test("Test MRGS zoomtopanel")
    mgrsZoomPanel.addStep("Load test project", lambda: _loadTestProject("map_tools_test"))
    mgrsZoomPanel.addStep("Open panel", _zoomTo)
    mgrsZoomPanel.addStep("Type '02HLJ' and click on 'zoom to'. Verify it centers the view on to the lower left corner of the previously clicked polygon and adds a marker", isVerifyStep=True)
    mgrsZoomPanel.addStep("Click on 'remove marker' and verify it removes the marker", isVerifyStep=True)

    return [mgrsMaptool, mgrsZoomPanel]


def unitTests():
    _tests = []
    #add unit tests with _tests.extend(test_suite)
    return _tests
