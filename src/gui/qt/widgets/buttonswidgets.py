'''
Created on Jul 9, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtCore import Qt
from src.gui.qt.widgets.common import TextValueWidget
from src.gui.qt.widgets.common import GridWidget


class ButtonWidgetContainer(GridWidget):
    def __init__(self, buttonModel, parent= None):
        super(ButtonWidgetContainer, self).__init__(["_Button", "Value_"], parent)
        self.buttonModel = buttonModel
        for button in range(self.buttonModel.currentJoystickNumButtons()):
            self.__createButtonValueWidget__(button)
        print("ASDFAFA F: ", self.buttonModel.currentJoystickNumButtons())
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
    
    def __createButtonValueWidget__(self, button):
        buttonWidget = ButtonValueWidget("Button " +str(button)+":")
        self.buttonModel.addButtonObserver(buttonWidget, button)
        self.addWidgetToScrollArea(buttonWidget)
    
class ButtonValueWidget(TextValueWidget):
    def __init__(self, label, parent = None):
        super(ButtonValueWidget, self).__init__(label, parent)
        self.css = "QLabel { background-color: %s; border-radius:5px; border: 1px solid black;}"
        self.value.setText(str(False))
        self.value.setStyleSheet(self.css%"white")
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setMaximumSize(48, 24)

    def customEvent(self, event):
        super(ButtonValueWidget, self).customEvent(event)
        color = "red" if event.value() else "white"
        self.value.setStyleSheet(self.css%color)

