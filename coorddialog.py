import mgrs
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from qgis.utils import *

class MGRSCoordInputDialog(QtGui.QDialog):
    
    def __init__(self, canvas, parent = None):
        super(MGRSCoordInputDialog, self).__init__(parent)
        self.canvas = canvas
        self.initGui()        
        
    def initGui(self):                         
        self.setWindowTitle('MGRS Coordinate')
        verticalLayout = QtGui.QVBoxLayout()                                            
                
        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)        
        coordLabel = QtGui.QLabel('MGRS coordinate to zoom to')        
        self.coordBox = QtGui.QLineEdit()        
        horizontalLayout.addWidget(coordLabel)
        horizontalLayout.addWidget(self.coordBox)
        verticalLayout.addLayout(horizontalLayout)
                      
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setLayout(verticalLayout)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.groupBox) 
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)
        
        self.setLayout(layout)
          
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        
        self.resize(350,150)

        self.marker = None
    
    def okPressed(self):
        try:
            self.mgrsCoord = str(self.coordBox.text()).replace(" ", "")
            lat, lon = mgrs.MGRS().toLatLon(self.mgrsCoord) 
            canvasCrs = self.canvas.mapRenderer().destinationCrs() 
            epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            transform4326 = QgsCoordinateTransform(epsg4326, canvasCrs)
            center = transform4326.transform(lon, lat)             
            self.canvas.zoomByFactor(1, center)
            self.canvas.refresh()
            if self.marker is None:
                self.marker = QgsVertexMarker(self.canvas)
            self.marker.setCenter(center)
            self.marker.setIconSize(8)
            self.marker.setPenWidth(4)
        except Exception, e: 
            print e        
            self.coordBox.setStyleSheet("QLineEdit{background: yellow}")

    def cancelPressed(self):
        self.close()  