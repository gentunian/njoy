'''
Created on Jul 9, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
import re
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import Qt
from src.gui.qt.ui.TextValueWidgetUi import Ui_textValueWidget
from src.gui.qt.ui.GridWidgetUi import Ui_gridWidget

class TextValueWidget(QWidget, Ui_textValueWidget):
    def __init__(self, text, parent = None):
        super(TextValueWidget, self).__init__(parent)
        self.setupUi(self)
        self.label.setText(str(text))

    def customEvent(self, event):
        self.value.setText(str(event.value()))

class GridWidget(QWidget, Ui_gridWidget):
    def __init__(self, headers, parent = None):
        super(GridWidget, self).__init__(parent)
        self.setupUi(self)
        col = 0
        for header in headers:
            match = re.match(".*\(([0-9]+)\)$", header)
            if match != None:
                width = int(match.group(1))
                header = header.replace("("+match.group(1)+")","")
                self.horizontalLayout.addWidget(self.__createLabel__(header, width))
            else:
                self.horizontalLayout.addWidget(self.__createLabel__(header))
            col = col +1
    
    def __createLabel__(self, text, width = None):
        if width == None:
            width = 9999
        if re.match("^[a-zA-Z]+_$", text) != None:
            alignment = Qt.AlignRight
            text = text[:len(text)-1]
        elif re.match("^_[a-zA-Z]+_$", text) != None: 
            alignment = Qt.AlignCenter
            text = text[1:len(text)-1]
        elif re.match("^_[a-zA-Z]+$", text) != None:
            alignment = Qt.AlignLeft
            text = text[1:]
        else:
            alignment = Qt.AlignLeft # default alignment
        label = QLabel(text)
        label.setMaximumWidth(width)
        label.setAlignment(alignment)
        return label

    def addWidget(self, widget, row, col, rowspan, colspan):
        if row <= 2:
            raise ValueError("Row must be greater than 2.")
        self.gridLayout.addWidget(widget, row, col, rowspan, colspan)

    def addWidgetToScrollArea(self, widget):
        self.verticalLayout.addWidget(widget)

    def addLayoutToScrollArea(self, layout):
        self.verticalLayout.addLayout(layout)

