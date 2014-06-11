import os
import site

site.addsitedir(os.path.abspath(os.path.dirname(__file__) + '/ext-libs'))

def classFactory(iface):
    # load QGis2OL class from file QGis2OL
    from mgrstools import MGRSTools
    return MGRSTools(iface)
