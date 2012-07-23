# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/joystickWidget.ui'
#
# Created: Mon Jul  9 18:14:21 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_joystickWidget(object):
    def setupUi(self, joystickWidget):
        joystickWidget.setObjectName(_fromUtf8("joystickWidget"))
        joystickWidget.resize(568, 444)
        joystickWidget.setWindowTitle(QtGui.QApplication.translate("joystickWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2 = QtGui.QVBoxLayout(joystickWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.joystickLabel = QtGui.QLabel(joystickWidget)
        self.joystickLabel.setText(QtGui.QApplication.translate("joystickWidget", "Joystick:", None, QtGui.QApplication.UnicodeUTF8))
        self.joystickLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.joystickLabel.setObjectName(_fromUtf8("joystickLabel"))
        self.horizontalLayout.addWidget(self.joystickLabel)
        self.joystickCombo = QtGui.QComboBox(joystickWidget)
        self.joystickCombo.setObjectName(_fromUtf8("joystickCombo"))
        self.horizontalLayout.addWidget(self.joystickCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabWidget = QtGui.QTabWidget(joystickWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(joystickWidget)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(joystickWidget)

    def retranslateUi(self, joystickWidget):
        pass

