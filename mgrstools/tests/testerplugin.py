# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin

import os
from qgis.core import QgsProject, QgsApplication
from qgis.utils import plugins, iface
from qgiscommons2.layers import loadLayer, layerFromName
from processing.gui.MessageDialog import MessageDialog
from processing.gui.AlgorithmDialog import AlgorithmDialog

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

    def _executeProcessingAlgorithm(algName):
        alg = QgsApplication.processingRegistry().createAlgorithmById(algName)
        if not alg:
            return

        ok, message = alg.canExecute()
        if not ok:

            dlg = MessageDialog()
            dlg.setTitle("Error executing algorithm")
            dlg.setMessage("This algorithm cannot be run :-( </h3>\n{0}".format(message))
            dlg.exec_()
            return

        dlg = alg.createCustomParametersWidget()
        if not dlg:
            dlg = AlgorithmDialog(alg)
        dlg.show()
        dlg.exec_()

    def _setLayerStyle(layer_name,style_file_name):
        layer = layerFromName(layer_name)
        style_file = os.path.join(os.path.dirname(__file__), 'data', style_file_name + '.qml')
        layer.loadNamedStyle(style_file)
        return

    def _setTool():
        plugins["mgrstools"].setTool()

    def _zoomTo():
        plugins["mgrstools"].zoomTo()

    mgrsMaptool = Test("Test MRGS map tool")
    mgrsMaptool.addStep("Load test project", lambda: _loadTestProject("map_tools_test"))
    mgrsMaptool.addStep("Select map tool", _setTool)
    mgrsMaptool.addStep("Move the mouse over the map canvas. Verify that the mouse pointer mrgrs coord shows on the bottom-left corner", isVerifyStep=True)
    mgrsMaptool.addStep("Click within the upper left polygon. Verify that the computed mrgrs coord starts with 02HLJ", isVerifyStep=True)
    mgrsMaptool.addStep("Open a text editor and press 'Ctrl+V'. Confirm that the computed coordinate is pasted", isVerifyStep=True)

    mgrsZoomPanel = Test("Test MRGS zoom to panel")
    mgrsZoomPanel.addStep("Load test project", lambda: _loadTestProject("map_tools_test"))
    mgrsZoomPanel.addStep("Open panel", _zoomTo)
    mgrsZoomPanel.addStep("Type '02HLJ' and click on 'zoom to'. Verify it centers the view on to the lower left corner of the previously clicked polygon and adds a marker", isVerifyStep=True)
    mgrsZoomPanel.addStep("Click on 'remove marker' and verify it removes the marker", isVerifyStep=True)

    mgrsCreateMgrsPoints = Test("Test Create point layer from MRGS field")
    mgrsCreateMgrsPoints.addStep("Load test project", lambda: _loadTestProject("create_points_from_mgrs_test"))
    mgrsCreateMgrsPoints.addStep("Opening algorithm dialog. Run on the 'points_with_mgrs' layer using the MGRS field as M", lambda: _executeProcessingAlgorithm("mgrs:createpointslayerfrommgrstable"))
    mgrsCreateMgrsPoints.addStep("Confirm that a layer is added to the project, which points are at the lower left corner of the grid", isVerifyStep=True)

    mgrsAddMGRSField = Test("Test Add MRGS field algorithm")
    mgrsAddMGRSField.addStep("Load test project", lambda: _loadTestProject("add_mgrs_field"))
    mgrsAddMGRSField.addStep("Opening algorithm dialog. Run the algorithm using the 'points_no_mgrs' layer", lambda: _executeProcessingAlgorithm("mgrs:addmgrsfield"))
    mgrsAddMGRSField.addStep("Apply layer style", lambda: _setLayerStyle('Output','mgrs_compare'))
    mgrsAddMGRSField.addStep("Open 'Output' layer's table of attributes. Confirm it contains a MGRS field, which values are compatible with the 'MGRS_compare' field.", isVerifyStep=True)


    return [mgrsMaptool, mgrsZoomPanel, mgrsCreateMgrsPoints, mgrsAddMGRSField]


def unitTests():
    _tests = []
    #add unit tests with _tests.extend(test_suite)
    return _tests
