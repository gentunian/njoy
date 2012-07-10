# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/axisWidgetContainer.ui'
#
# Created: Mon Jul  9 04:39:48 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_axisWidgetContainer(object):
    def setupUi(self, axisWidgetContainer):
        axisWidgetContainer.setObjectName(_fromUtf8("axisWidgetContainer"))
        axisWidgetContainer.resize(400, 300)
        axisWidgetContainer.setWindowTitle(QtGui.QApplication.translate("axisWidgetContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(axisWidgetContainer)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(axisWidgetContainer)
        self.label_4.setMaximumSize(QtCore.QSize(24, 24))
        self.label_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_4.setText(QtGui.QApplication.translate("axisWidgetContainer", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(axisWidgetContainer)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setText(QtGui.QApplication.translate("axisWidgetContainer", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtGui.QLabel(axisWidgetContainer)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setText(QtGui.QApplication.translate("axisWidgetContainer", "Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(axisWidgetContainer)
        self.label_3.setMaximumSize(QtCore.QSize(24, 24))
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setText(QtGui.QApplication.translate("axisWidgetContainer", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.retranslateUi(axisWidgetContainer)
        QtCore.QMetaObject.connectSlotsByName(axisWidgetContainer)

    def retranslateUi(self, axisWidgetContainer):
        pass

