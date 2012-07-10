'''
Created on Jul 7, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
import sys
from src.models.JoystickModel import JoystickModel
from src.widgets.joystickview import JoystickWidget

class Main(QMainWindow):
    
    def __init__(self, axis):
        print("[Main]: Creating MainWindow")
        QMainWindow.__init__(self)
        self.setCentralWidget(axis)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = JoystickModel()
    #container = axisview.AxisWidgetContainer(axisModel)
    container = JoystickWidget(model)
    main = Main(container)
    print("Show")
    main.show()
    v=app.exec_()
    model.stop()
    sys.exit(v)

