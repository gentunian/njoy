'''
Created on Jul 7, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from PyQt4.QtCore import QObject, pyqtProperty
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QEvent
from PyQt4.QtGui import QApplication
from pygame import joystick
from pygame.joystick import Joystick
from pygame import locals
from collections import defaultdict
import pygame
try:
    from PyQt4.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = type("")
    
class JoystickEvent(QEvent):
    def __init__(self, jid, eType = QEvent.User):
        super(JoystickEvent, self).__init__(eType)
        self._jid = jid
    
    @pyqtProperty(int)
    def joy(self):
        return self._jid

class JoystickButtonEvent(JoystickEvent):
    def __init__(self, jid, button, value):
        super(JoystickButtonEvent, self).__init__(jid)
        self._button = button
        self._value = value
        
    @pyqtProperty(int)
    def button(self):
        return self._button
    
    @pyqtProperty(bool)
    def value(self):
        return self._value
    
class JoystickAxisEvent(JoystickEvent):
    def __init__(self, jid, axis, value):
        super(JoystickAxisEvent, self).__init__(jid)
        self._axis = axis
        self._value = value

    @pyqtProperty(int)
    def axis(self):
        return self._axis
    
    @pyqtProperty(float)
    def value(self):
        return self._value
    
class JoystickHatEvent(JoystickEvent):
    def __init__(self, jid, hat, value):
        super(JoystickHatEvent, self).__init__(jid)
        self._hat = hat
        self._value = value

    @pyqtProperty(int)
    def hat(self):
        return self._hat
    
    @pyqtProperty(tuple)
    def value(self):
        return self._value
    
class JoystickBallEvent(JoystickEvent):
    def __init__(self, jid, ball, value):
        super(JoystickHatEvent, self).__init__(jid)
        self._ball = ball
        self._value = value

    @pyqtProperty(int)
    def hat(self):
        return self._hat
    
    @pyqtProperty(tuple)
    def value(self):
        return self._value

class JoystickModel(QObject):
    
    def __init__(self, parent = None):
        pygame.init()
        joyCount = joystick.get_count()
        self.axisObservers = defaultdict(list)
        self.hatObservers = defaultdict(list)
        self.buttonObservers = defaultdict(list)
        self.current = -1
        self.joyList = {}
        self.lastAxisValue = [[] for i in range(joyCount)]
        self.lastHatValue = [[] for i in range(joyCount)]
        self.lastButtonValue = [[] for i in range(joyCount)]
        for jid in reversed(range(joystick.get_count())):
            self.__createJoystick__(jid)
            self.current = jid
        self.dispatcher = EventDispatcher(self)
        self.dispatcher.start()
    
    def __del__(self):
        self.dispatcher.alive(False)
        pygame.quit()
    
    def __createJoystick__(self, jid):
        aJoystick = Joystick(jid)
        aJoystick.init()
        self.joyList[jid] = aJoystick 
        self.joyList["[{id}]{name}".format(id=jid, name=aJoystick.get_name())] = aJoystick

    def joystickCount(self):
        return pygame.joystick.get_count()

    def joystickNames(self):
        try:
            return [ k for k in self.joyList.iterkeys() if isinstance(k, str)]
        except:
            return []
    
    def currentJoystickId(self):
        return self.current
    
    def currentJoystickName(self):
        try:
            return self.joyList[self.current].get_name()
        except:
            return ""
    
    def currentJoystickNumAxes(self):
        try:
            return self.joyList[self.current].get_numaxes()
        except:
            return 0
    
    def currentJoystickNumHats(self):
        try:
            return self.joyList[self.current].get_numhats()
        except:
            return 0
    
    def currentJoystickNumBalls(self):
        try:
            return self.joyList[self.current].get_numballs()
        except:
            return 0
    
    def currentJoystickNumButtons(self):
        try:
            return self.joyList[self.current].get_numbuttons()
        except:
            return 0
    
    def setCurrentJoystickByName(self, jname):
        self.setCurrentJoystickById(self.joyList[str(jname)].get_id())
    
    def setCurrentJoystickById(self, jid):
        self.current = jid
        self.joyList[jid].init()

    def addButtonObserver(self, observer, buttonNumber):
        self.buttonObservers[buttonNumber].append(observer)
    
    def addHatObserver(self, observer, hatNumber):
        self.hatObservers[hatNumber].append(observer)

    def addAxisObserver(self, observer, axisNumber):
        self.axisObservers[axisNumber].append(observer)

    def removeHatObserver(self, observer, hatNumber):
        self.hatObservers[hatNumber].remove(observer)

    def removeAxisObserver(self, observer, axisNumber):
        self.axisObservers[axisNumber].remove(observer)

    def removeButtonObserver(self, observer, buttonNumber):
        self.buttonObservers[buttonNumber].remove(observer)

    def notifyHatChange(self, hat, value):
        for observer in self.hatObservers[hat]:
            #observer.update(hat, value)
            QApplication.postEvent(observer, JoystickAxisEvent(self.current, hat, value)) 
        
    def notifyAxisChange(self, axis, value):
        for observer in self.axisObservers[axis]:
            #observer.update(axis, value)
            QApplication.postEvent(observer, JoystickAxisEvent(self.current, axis, value))
    
    def notifyButtonChange(self, button, value):
        for observer in self.buttonObservers[button]:
            #observer.update(button, value)
            QApplication.postEvent(observer, JoystickButtonEvent(self.current, button, value))

class EventDispatcher(QThread):
    
    def __init__(self, model, parent = None):
        print("[EventDispatcher]: init.")
        QThread.__init__(self, parent)
        self.model = model
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
        
    def __end__(self):
        print("[EventDispatcher]: end.")
    
    def alive(self, isAlive):
        self.alive = isAlive
    
    def run(self):
        print("[EventDispatcher]: Starting...")
        while(self.alive):
            e = pygame.event.wait()
            print("asdf: ", e)
            # Don't process any event coming from joystick that are not
            # selected by the model.
            if e.joy == self.model.currentJoystickId():
                if e.type == locals.JOYAXISMOTION:
                    #print("[EventDispatcher]: JOYAXISMOTION in joystick {} at axis {} with value {}".format(e.joy, e.axis, e.value))
                    self.model.notifyAxisChange(e.axis, e.value)
                elif e.type == locals.JOYHATMOTION:
                    #print("[EventDispatcher]: JOYHATMOTION")
                    self.model.notifyHatChange(e.hat, e.value)
                elif e.type == locals.JOYBALLMOTION:
                    #print("[EventDispatcher]: JOYBALLMOTION")
                    pass
                elif e.type == locals.JOYBUTTONDOWN:
                    #print("[EventDispatcher]: JOYBUTTONDOWN")
                    self.model.notifyButtonChange(e.button, False)
                elif e.type == locals.JOYBUTTONUP:
                    #print("[EventDispatcher]: JOYBUTTONUP")
                    self.model.notifyButtonChange(e.button, True)

