# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin

from qgis.utils import *
from qgis.core import *

def functionalTests():
    try:
        from qgistester.test import Test
        from qgistester.utils import loadLayer
        import mgrs
    except:
        return []

    def _loadLayer():
        layerfile = os.path.join(os.path.dirname(__file__), "data", "MGRS_100kmSQ_ID_02H.shp")
        layer = loadLayer(layerfile)
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def _setTool():
        plugins["mgrstools"].setTool()

    def _zoomTo():
        plugins["mgrstools"].zoomTo()

    mgrsTest = Test("Test MRGS tools")
    mgrsTest.addStep("Load layer", _loadLayer)
    mgrsTest.addStep("Select map tool", _setTool)
    mgrsTest.addStep("Click within the upper left polygon. Verify that the computed mrgrs coord starts with 02HKK'", isVerifyStep = True)
    mgrsTest.addStep("Open panel", _zoomTo)
    mgrsTest.addStep("Enter '02HKK' and click on 'zoom to'. Verify it centers the view on to the upper left polygon and adds a marker")
    mgrsTest.addStep("Click on 'remove marker' and verify it removes the marker")
    return [mgrsTest]


def unitTests():
    _tests = []
    #add unit tests with _tests.extend(test_suite)    
    return _tests