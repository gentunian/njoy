# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/axisGraphWidget.ui'
#
# Created: Mon Jul  9 04:13:39 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_axisGraphWidget(object):
    def setupUi(self, axisGraphWidget):
        axisGraphWidget.setObjectName(_fromUtf8("axisGraphWidget"))
        axisGraphWidget.resize(328, 325)
        axisGraphWidget.setWindowTitle(QtGui.QApplication.translate("axisGraphWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(axisGraphWidget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.axisView = QtGui.QGraphicsView(axisGraphWidget)
        self.axisView.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing|QtGui.QPainter.NonCosmeticDefaultPen|QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.axisView.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.axisView.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.axisView.setObjectName(_fromUtf8("axisView"))
        self.verticalLayout.addWidget(self.axisView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.showGrid = QtGui.QCheckBox(axisGraphWidget)
        self.showGrid.setText(QtGui.QApplication.translate("axisGraphWidget", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.showGrid.setObjectName(_fromUtf8("showGrid"))
        self.horizontalLayout.addWidget(self.showGrid)
        self.trackHistory = QtGui.QCheckBox(axisGraphWidget)
        self.trackHistory.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.trackHistory.setText(QtGui.QApplication.translate("axisGraphWidget", "Track History", None, QtGui.QApplication.UnicodeUTF8))
        self.trackHistory.setObjectName(_fromUtf8("trackHistory"))
        self.horizontalLayout.addWidget(self.trackHistory)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(axisGraphWidget)
        QtCore.QMetaObject.connectSlotsByName(axisGraphWidget)

    def retranslateUi(self, axisGraphWidget):
        pass

