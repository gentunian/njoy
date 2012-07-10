# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'textValueWidget.ui'
#
# Created: Mon Jul  9 21:53:42 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_textValueWidget(object):
    def setupUi(self, textValueWidget):
        textValueWidget.setObjectName(_fromUtf8("textValueWidget"))
        textValueWidget.resize(214, 25)
        textValueWidget.setWindowTitle(QtGui.QApplication.translate("textValueWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(textValueWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.value = QtGui.QLabel(textValueWidget)
        self.value.setStyleSheet(_fromUtf8("QLabel { background-color: white;}"))
        self.value.setFrameShape(QtGui.QFrame.Box)
        self.value.setFrameShadow(QtGui.QFrame.Plain)
        self.value.setText(QtGui.QApplication.translate("textValueWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.value.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.value.setObjectName(_fromUtf8("value"))
        self.gridLayout.addWidget(self.value, 0, 1, 1, 1)
        self.label = QtGui.QLabel(textValueWidget)
        self.label.setText(QtGui.QApplication.translate("textValueWidget", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(textValueWidget)
        QtCore.QMetaObject.connectSlotsByName(textValueWidget)

    def retranslateUi(self, textValueWidget):
        pass

