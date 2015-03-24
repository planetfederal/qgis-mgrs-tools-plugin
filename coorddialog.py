import mgrs
from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *
from qgis.utils import *

ITEMHEIGHT = 30
OFFSET = 20
HEIGHT = 60


class MGRSCoordInputDialog(QtGui.QDockWidget):
    def __init__(self, canvas, parent):
        self.canvas = canvas
        self.marker = None
        QtGui.QDockWidget.__init__(self, parent)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.initGui()

    def initGui(self):
        self.label = QtGui.QLabel('MGRS coordinate to zoom to')        
        self.coordBox = QtGui.QLineEdit()        
        self.zoomToButton = QtGui.QPushButton("Zoom to")
        self.zoomToButton.clicked.connect(self.zoomToPressed)
        self.removeMarkerButton = QtGui.QPushButton("Remove marker")
        self.removeMarkerButton.clicked.connect(self.closePressed)
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
        except Exception, e:    
            self.coordBox.setStyleSheet("QLineEdit{background: yellow}")

    def removeMarkerPressed(self):
        self.canvas.scene().removeItem(self.marker)