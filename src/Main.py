'''
Created on Jul 7, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
import sys
import axisview
import joystickview
from JoystickModel import JoystickModel

class Main(QMainWindow):
    
    def __init__(self, axis):
        print("[Main]: Creating MainWindow")
        QMainWindow.__init__(self)
        self.setCentralWidget(axis)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    axisModel = JoystickModel()
    #container = axisview.AxisWidgetContainer(axisModel)
    container = joystickview.JoystickWidget(axisModel)

    main = Main(container)
    print("Show")
    main.show()
    sys.exit(app.exec_())

