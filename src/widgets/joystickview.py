'''
Created on Jul 9, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QString
from ui.JoystickWidgetUi import Ui_joystickWidget
from src.widgets.axeswidgets import AxisWidgetContainer
from src.widgets.buttonswidgets import ButtonWidgetContainer

class JoystickWidget(QWidget, Ui_joystickWidget):
    
    def __init__(self, model, parent = None):
        super(JoystickWidget, self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.__configureJoystickCombo__()
        self.buttonsWidget = ButtonWidgetContainer(model, None)
        self.tabWidget.addTab(self.buttonsWidget, "Buttons")
        self.axisWidget = AxisWidgetContainer(model, None)
        self.tabWidget.addTab(self.axisWidget, "Axes")
    
    def __configureJoystickCombo__(self):
        for joyName in self.model.joystickNames():
            self.joystickCombo.addItem(joyName)
        self.joystickCombo.currentIndexChanged[QString].connect(self.joystickSelected)

    def joystickSelected(self, joyName):
        self.model.setCurrentJoystickByName(joyName)