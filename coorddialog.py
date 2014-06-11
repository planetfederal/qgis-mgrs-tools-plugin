import mgrs
from PyQt4 import QtGui, QtCore
from qgis.core import *

class MGRSCoordInputDialog(QtGui.QDialog):
    
    ct = mgrs.MGRS()

    def __init__(self, parent = None):
        super(MGRSCoordInputDialog, self).__init__(parent)
        self.latlon = None        
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
            
    
    def okPressed(self):
        try:
            mgrsCoord = self.coordBox.text()
            print mgrsCoord
            self.latlon = mgrs.MGRS().toLatLon(str(mgrsCoord))            
            self.close()
        except Exception, e:
            print e
            self.coordBox.setStyleSheet("QLineEdit{background: yellow}")

    def cancelPressed(self):
        self.latlon = None        
        self.close()  