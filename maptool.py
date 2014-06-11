import mgrs
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PyQt4.QtCore import *

class MGRSMapTool(QgsMapTool):
     
    ct = mgrs.MGRS()
    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    def __init__(self, canvas):        
        QgsMapTool.__init__(self, canvas)        
        self.setCursor(Qt.CrossCursor)

    def canvasMoveEvent(self, e):                
        pt = self.toMapCoordinates(e.pos())
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapRenderer().destinationCrs()         
        transform = QgsCoordinateTransform(canvasCrs, self.epsg4326)
        pt4326 = transform.transform(pt.x(), pt.y())      
        try:
            mgrsCoords = self.ct.toMGRS(pt4326.y(), pt4326.x())
            iface.mainWindow().statusBar().showMessage("MGRS Coordinate: " + mgrsCoords)
        except:
            iface.mainWindow().statusBar().showMessage("")
        
        

        
