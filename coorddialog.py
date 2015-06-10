import mgrs
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from qgis.utils import *

class MGRSCoordInputDialog(QtGui.QDockWidget):
    def __init__(self, canvas, parent):
        self.canvas = canvas
        self.marker = None
        QtGui.QDockWidget.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.initGui()

    def initGui(self):
        self.setWindowTitle("MGRS Coordinate Zoom")
        self.label = QtGui.QLabel('MGRS coordinate')        
        self.coordBox = QtGui.QLineEdit()      
        self.coordBox.returnPressed.connect(self.zoomToPressed)  
        self.zoomToButton = QtGui.QPushButton("Zoom to")
        self.zoomToButton.clicked.connect(self.zoomToPressed)
        self.removeMarkerButton = QtGui.QPushButton("Remove marker")
        self.removeMarkerButton.clicked.connect(self.removeMarker)
        self.removeMarkerButton.setDisabled(True)
        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.setSpacing(6)
        self.hlayout.setMargin(9)
        self.hlayout.addWidget(self.label)
        self.hlayout.addWidget(self.coordBox)
        self.hlayout.addWidget(self.zoomToButton)
        self.hlayout.addWidget(self.removeMarkerButton)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setLayout(self.hlayout)
        self.setWidget(self.dockWidgetContents)

    def zoomToPressed(self):
        try:
            mgrsCoord = str(self.coordBox.text()).replace(" ", "")
            lat, lon = mgrs.MGRS().toLatLon(mgrsCoord) 
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
            self.removeMarkerButton.setDisabled(False)
            self.coordBox.setStyleSheet("QLineEdit{background: white}")
        except Exception, e:    
            self.coordBox.setStyleSheet("QLineEdit{background: yellow}")

    def removeMarker(self):
        self.canvas.scene().removeItem(self.marker)
        self.marker = None

    def closeEvent(self, evt):
        if self.marker is not None:
            self.canvas.scene().removeItem(self.marker)
            self.marker = None
