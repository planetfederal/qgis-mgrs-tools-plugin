# Tests for the QGIS Tester plugin. To know more see
# https://github.com/boundlessgeo/qgis-tester-plugin


def functionalTests():
    try:
        from qgistester.test import Test
        from qgistester.utils import *
    except:
        return []

    #write tests here and return them
    return []


def unitTests():
    _tests = []
    #add unit tests with _tests.extend(test_suite)    
    return _tests