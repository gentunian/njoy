'''
Created on Jul 7, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
import sys
from collections import defaultdict
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QObject
from src.models.common import JoystickChangeObserver
from src.models.common import events
from src.models.linux import joystick
from src.gui.qt.widgets.joystickview import JoystickWidget
from src.gui.qt.qtevents import JoystickEvent

class Main(QMainWindow):
    
    def __init__(self, axis):
        print("[Main]: Creating MainWindow")
        QMainWindow.__init__(self)
        self.setCentralWidget(axis)

class Model(QObject):
    def __init__(self, m):
        super(Model, self).__init__()
        self.current = -1
        self._model = m
        for joy in self.joysticks():
            joy.addChangeObserver(self)
        self.observers = defaultdict(list)
        for e in events.eventName.keys():
            self.observers[e] = {}
    
    def setCurrenJoystick(self, jid):
        self.current = jid
    
    def setCurrentJoystickByName(self, jname):
        try:
            self.current = [ joy.joyId() for joy in self.joysticks() if joy.name()==jname][0]
            print(self.current)
        except:
            pass
        
    def currentJoystick(self):
        return self.current
    
    def joysticks(self):
        return self._model.joysticks()
    
    def joystick(self, jid):
        return self._model.joystick(jid)
    
    def joystickNames(self):
        try:
            return [ joy.name() for joy in self.joysticks() ]
        except:
            return []
    
    def stateChanged(self, change):
        if change.event.jid() != self.current:
            return
        for observer in self.observers[change.event.eventType()][change.event.what()]:
            QApplication.postEvent(observer, JoystickEvent(change.event))
    
    def currentJoystickName(self):
        try:
            return self._model.joylist[self.current].name()
        except:
            return ""
    
    def currentJoystickNumAxes(self):
        try:
            return self._model.joylist[self.current].axes()
        except:
            return 0
    
    def currentJoystickNumButtons(self):
        for j in self.joysticks():
            print("buttons: %d"%j.buttons(), self.current)
        try:
            return self._model.joylist[self.current].buttons()
        except Exception as ex:
            print(ex)
            return 0
    
    def addObserver(self, eventType, what, observer):
        try:
            self.observers[eventType][what].append(observer)
        except KeyError:
            self.observers[eventType][what] = []
            self.observers[eventType][what].append(observer)
        
    def addButtonObserver(self, observer, buttonNumber):
        #self.buttonObservers[buttonNumber].append(observer)
        self.addObserver(events.BUTTON_EVENT, buttonNumber, observer)
        
    def addAxisObserver(self, observer, axisNumber):
        #self.axisObservers[axisNumber].append(observer)
        self.addObserver(events.AXIS_EVENT, axisNumber, observer)
        
    def removeAxisObserver(self, observer, axisNumber):
        self.axisObservers[axisNumber][events.AXIS_EVENT].remove(observer)

    def removeButtonObserver(self, observer, buttonNumber):
        self.buttonObservers[buttonNumber][events.AXIS_EVENT].remove(observer)
    
if __name__ == '__main__':
    import time
    app = QApplication(sys.argv)
    joyModel = joystick.JoystickHolder()
    time.sleep(1)
    print(joyModel.joysticks())
    model = Model(joyModel)
    #container = axisview.AxisWidgetContainer(axisModel)
    container = JoystickWidget(model)
    main = Main(container)
    print("Show")
    main.show()
    v=app.exec_()
    model.stop()
    sys.exit(v)

