# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'buttonWidgetContainer.ui'
#
# Created: Tue Jul 10 01:02:47 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_buttonWidgetContainer(object):
    def setupUi(self, buttonWidgetContainer):
        buttonWidgetContainer.setObjectName(_fromUtf8("buttonWidgetContainer"))
        buttonWidgetContainer.resize(405, 297)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(buttonWidgetContainer.sizePolicy().hasHeightForWidth())
        buttonWidgetContainer.setSizePolicy(sizePolicy)
        buttonWidgetContainer.setWindowTitle(QtGui.QApplication.translate("buttonWidgetContainer", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(buttonWidgetContainer)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(buttonWidgetContainer)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setText(QtGui.QApplication.translate("buttonWidgetContainer", "Button #", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.line = QtGui.QFrame(buttonWidgetContainer)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(buttonWidgetContainer)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setText(QtGui.QApplication.translate("buttonWidgetContainer", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.scrollArea = QtGui.QScrollArea(buttonWidgetContainer)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 385, 241))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 2)

        self.retranslateUi(buttonWidgetContainer)
        QtCore.QMetaObject.connectSlotsByName(buttonWidgetContainer)

    def retranslateUi(self, buttonWidgetContainer):
        pass

