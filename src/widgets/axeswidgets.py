'''
Created on Jul 8, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtGui import QGraphicsScene
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QButtonGroup
from PyQt4.QtGui import QGraphicsPathItem
from PyQt4.QtGui import QPainterPath
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QRadioButton
from PyQt4.QtGui import QGraphicsEllipseItem
from PyQt4.QtCore import QPointF
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QRectF
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSizePolicy
from ui.AxisGraphWidgetUi import Ui_axisGraphWidget
from src.widgets.common import TextValueWidget
from src.widgets.common import GridWidget

class AxisWidgetContainer(GridWidget):
    def __init__(self, axisModel, parent = None):
        super(AxisWidgetContainer, self).__init__(["_Axis", "_Value_", "_X(24)", "_Y(24)"], parent)
        self.axisModel = axisModel
        self.xGroup = QButtonGroup()
        self.yGroup = QButtonGroup()
        self.xGroup.buttonClicked.connect(self.showXAxisButtonClicked)
        self.yGroup.buttonClicked.connect(self.showYAxisButtonClicked)
        axis = 0
        for axis in range(axisModel.currentJoystickNumAxes()):
            self.__createTextWidgetForAxis__(axis)
        if axis > 0:
            self.graphWidget = AxisGraphWidget(self)
            self.addWidget(self.graphWidget, 3, 0, 1, 2)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        
    def __createTextWidgetForAxis__(self, axis):
        textWidget = AxisTextWidget(axis, self)
        self.axisModel.addAxisObserver(textWidget, axis)
        showInX = QRadioButton()
        showInY = QRadioButton()
        showInX.setObjectName(str(axis))
        showInY.setObjectName(str(axis))
        showInX.setLayoutDirection(Qt.RightToLeft)
        showInY.setLayoutDirection(Qt.RightToLeft)
        showInX.setMaximumSize(24, 24)
        showInY.setMaximumSize(24, 24)
        self.xGroup.addButton(showInX)
        self.yGroup.addButton(showInY)
        gridLayout = QGridLayout()
        gridLayout.addWidget(textWidget, 0, 0, 1, 2)
        gridLayout.addWidget(showInX, 0, 2, 1, 1)
        gridLayout.addWidget(showInY, 0, 3, 1, 1)
        self.addLayoutToScrollArea(gridLayout)

    def showXAxisButtonClicked(self, button):
        if button.isChecked():
            self.graphWidget.setXAxis(int(button.objectName()))
            self.axisModel.addAxisObserver(self.graphWidget, int(button.objectName()))
        else:
            self.axisModel.removeAxisObserver(self.graphWidget, int(button.objectName()))
    
    def showYAxisButtonClicked(self, button):
        if button.isChecked():
            self.graphWidget.setYAxis(int(button.objectName()))
            self.axisModel.addAxisObserver(self.graphWidget, int(button.objectName()))
        else:
            self.axisModel.removeAxisObserver(self.graphWidget, int(button.objectName()))


class AxisGraphWidget(QWidget, Ui_axisGraphWidget):
    trackHistoryChanged = pyqtSignal('bool')
    
    def __init__(self, parent = None):
        super(AxisGraphWidget, self).__init__(parent)
        self.setupUi(self)
        self.scene = AxisScene()
        self.axisView.setScene(self.scene)
        self.showGrid.toggled.connect(self.scene.gridToggled)
        self.trackHistory.toggled.connect(self.scene.pathToggled)

    def setYAxis(self, y):
        self.yAxis = y
        self.scene.setYAxisName(y)
        
    def setXAxis(self, x):
        self.scene.setXAxisName(x)
        self.xAxis = x
    
    def resizeEvent(self, event):
        size = self.axisView.size() - QSize(10, 10)
        self.scene.setSceneRect(-(size.width() / 2), -(size.height() / 2), size.width(), size.height())

    def update(self, axis, value):
        if self.xAxis == axis:
            self.scene.updateDotX(value)
        elif self.yAxis == axis:
            self.scene.updateDotY(value)
        else:
            #Do nothing as we don't know what to do with an unregistered axis
            pass

    def customEvent(self, event):
        self.update(event.axis, event.value)


class AxisTextWidget(TextValueWidget):
    def __init__(self, axis, parent = None):
        super(AxisTextWidget, self).__init__("Axis " + str(axis) + ":", parent)
        self.value.setText(str(0.0))

    def customEvent(self, event):
        self.value.setText("%5.4f" % event.value)


class AxisScene(QGraphicsScene):
    def __init__(self, parent = None):
        super(AxisScene, self).__init__(parent)
        self.guidePen = QPen(QColor("blue"),1)
        self.dot = QGraphicsEllipseItem(-10, -10, 20, 20)
        self.dot.setPos(QPointF(0,0))
        self.dot.setPen(QPen(QColor("red"), 4))
        self.dot.setBrush(QColor("black"))
        self.lastPos = {}
        self.lastPos['x'] = 0
        self.lastPos['y'] = 0
        self.grid = False
        self.gridPen = QPen(QColor("blue"), 2)
        self.pathItem = QGraphicsPathItem()
        self.pathItem.setPen(QPen(QColor("red"), 1, Qt.DotLine))
        self.path = None
        self.xAxis = "Select Axis..."
        self.yAxis = self.xAxis
        self.addItem(self.dot)
    
    def setXAxisName(self, x):
        self.xAxis = "Axis " + str(x)
        self.invalidate()

    def setYAxisName(self, y):
        self.yAxis = "Axis " + str(y)
        self.invalidate()

    def pathToggled(self, toggled):
        if toggled:
            self.path = QPainterPath()
            self.path.moveTo(0,0)
            self.pathItem.setPath(self.path)
            self.addItem(self.pathItem)
        else:
            if self.path != None:
                self.removeItem(self.pathItem)
            self.path = None
        self.invalidate()

    def gridToggled(self, toggled):
        self.grid = toggled
        self.invalidate()

    def updateDotX(self, x):
        self.lastPos['x'] = x * (self.sceneRect().width() / 2)
        self.update(self.lastPos['x'], self.lastPos['y'])
    
    def updateDotY(self, y):
        self.lastPos['y'] = y * (self.sceneRect().height() / 2)
        self.update(self.lastPos['x'], self.lastPos['y'])
    
    def update(self, x, y):
        if self.path != None:
            self.path.lineTo(x, y)
            self.pathItem.setPath(self.path)
        self.dot.setPos(self.lastPos['x'], self.lastPos['y'])
        self.invalidate()
    
    def drawBackground(self, painter, rect):
        if self.grid:
            painter.setClipRect(rect)
            painter.setPen(self.gridPen)

    def drawForeground(self, painter, rect):
        painter.setClipRect(rect)
        painter.setPen(self.gridPen)
        r = self.sceneRect()
        if self.grid:
            painter.drawLine(r.center().x(), r.top(), r.center().x(), r.bottom())
            painter.drawLine(r.left(), r.center().y(), r.right(), r.center().y())
            painter.setPen(QPen(QColor("red"), 1))
            painter.drawText(QRectF(r.left(), r.center().y(), 80, 80), self.xAxis)
            painter.drawText(QRectF(r.center().x()+5, r.top(), 80, 80), self.yAxis)
        if self.path != None:
            painter.setPen(QPen(QColor("red"), 1))
            painter.drawLine(QPointF(self.lastPos['x'], r.top()), QPointF(self.lastPos['x'], r.bottom()))
            painter.drawLine(QPointF(r.left(), self.lastPos['y']), QPointF(r.right(), self.lastPos['y']))
