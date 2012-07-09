# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/axisTextWidget.ui'
#
# Created: Sun Jul  8 22:10:35 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_axisTextWidget(object):
    def setupUi(self, axisTextWidget):
        axisTextWidget.setObjectName(_fromUtf8("axisTextWidget"))
        axisTextWidget.resize(214, 25)
        axisTextWidget.setWindowTitle(QtGui.QApplication.translate("axisTextWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(axisTextWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.axisValue = QtGui.QLabel(axisTextWidget)
        self.axisValue.setStyleSheet(_fromUtf8("QLabel { background-color: white;}"))
        self.axisValue.setFrameShape(QtGui.QFrame.Box)
        self.axisValue.setFrameShadow(QtGui.QFrame.Plain)
        self.axisValue.setText(QtGui.QApplication.translate("axisTextWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.axisValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.axisValue.setObjectName(_fromUtf8("axisValue"))
        self.gridLayout.addWidget(self.axisValue, 0, 1, 1, 1)
        self.axisLabel = QtGui.QLabel(axisTextWidget)
        self.axisLabel.setText(QtGui.QApplication.translate("axisTextWidget", "Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.axisLabel.setObjectName(_fromUtf8("axisLabel"))
        self.gridLayout.addWidget(self.axisLabel, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(axisTextWidget)
        QtCore.QMetaObject.connectSlotsByName(axisTextWidget)

    def retranslateUi(self, axisTextWidget):
        pass

