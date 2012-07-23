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

""" The *Event classes wraps pygame or sfml events into Qt Events (QEvent).
    For some purist this will sound like overloading the project with classes...Well, yes.
    
    The project does not imply or tend to use real-time scenarios where performance or latency
    is key. The project itselft has begun as a joystick-viewer tool where in an unknown future
    could derive in a calibration tool.
    
    This will imply leaving pygame or sfml and use some sort of low level library to access
    joystick data and modify axes values. So, it's hard and far away to that to happen.
    
    JoystickEvent classes will provide accesible context in order to know some values
    about the true joystick event and apply semantics to that concept for widgets (Views).
    
    The main work is done in the model. The model has a number of different kind of observers.
    Observers could be buttons observers, axis observers, hat observers, and so on. In the most
    basic way, observers should be interested objects on showing some joystick feature data, such
    as, the value of some buttons, the position of axis 0, etc. These objects mainly will provide
    user output (a view). The view could be any kind of object (in this terms, an observer) that
    KNOWS where is looking (which joystick feature is observing) and KNOWS what a JoystickEvent
    for that particular feature is.
    
    As an implementation detail, the Qt Events (QEvent) are posted using the Qt system for posting
    events to those observers (QtApplication.postEvent(observer, aJoystickEvent)). Each interested
    observer SHOULD BE a QObject. And in order to manage or handle the event posted to it, it has
    the need to implement the method 'customEvent(self, event)'. Inside that method, the observer
    could do anything. The observer has to know how to manage the event argument and manage it as
    the observer likes.
    
    The thread running and waiting on the queue of joystick events will call the model notify*
    methods in order to allow the model to post the events to the registered observer for such event.
    
    There is not much more magic than that with this wrapped joystick model to mention. One thing to
    notice is the restriction that has been implied in the model: There's only ONE joystick at a time
    being pooled. This means that the model holds a current joystick as selected, and any event upcoming
    from any other joystick rather than the selected it will be ignored.
    
    Having say so, don't expect the model to broadcast all joystick events to every observer. The model
    WILL ONLY post events for the currently selected joystick. This implies that SOMEONE ELSE must
    say which one of the available joystick will be the currently selected. This will be done by someone
    using the model and calling one of these methods:
    
            setCurrentJoystickById(jid)
            or
            setCurrentJoystickByName(jname) --- joystick names prefixes with [jid], e.g.: "[0]TheUberMegaWachistationJoystick"
    
    Of course that someone calling or using those methods should KNOW which joystick id or joystick name
    to select. That information will come with the model with both of these methods:
    
            joystickNames()
            and
            joystickCount() --- joystick ids will go from 0 to joystickCount() - 1
    
    Another thing to mention is that, any object that want to configure a set of views by using the model,
    it has a bunch of methods for doing that, and again, ALWAYS for the currently selected joystick that
    which by default it's 0 (if any joystick is detected, -1 else), they are:
    
        currentJoystickNumAxes() --- current joystick axes number
        currentJoystickNumHats() --- current joystick hats number
        currentJoystickNumBalls() --- current joystick balls (?) number
        currentJoystickNumButtons() --- current joystick buttons number
        joystickCount() --- see above
        joystickNames() --- see above
        
    In order to start receiving QEvents for yours QWidgets, you need to register or add the interested QObject
    to the model. This is done by the following way:
    
        if __name__ == '__main__':
            jmodel = JoystickModel()
            buttonTenObserver = ButtonTenObserver()
            axisOneObserver = AxisOneObserver()
            jmodel.addButtonObserver(10, buttonTenObserver)
            jmodel.addAxisObserver(1, axisOneObserver)
    
    As soon as the observers are registered to the model, they will start receiving events for the CURRENTLY
    SELECTED JOYSTICK. Note that you only register a button observer. This will be changed in the future. The
    main disadvantage is that you can connect a joystick that has NO button 10. The proper way to avoid, is
    to code something as follows:
    
        if __name__ == '__main__':
            jmodel = JoystickModel()
            for button in jmodel.currentJoystickNumButtons():
                jmodel.addButtonObserver(button, theObserver)
    
    That will ensure that theObserver is NOW observing the current joystick buttons. Of course that, if the
    current joystick is changed, the actor of that action should know what is doing so it will need to trigger
    the appropiate way of registering the appropiates observer.
    
    Anyway, nothing bad will happen. I'll explain way. Basically, the model ONLY notifies observers about the
    CURRENTLY selected joystick. You have an object responsible of selecting the current joystick. So, this
    situations arises:
    
        * If you register an observer for button, say, 10 and the currently selected joystick 
          has no button 10, nothing happens.
        
        * If you register an observer for a button, say, 10 and the currently selected joystick
          has a button number 10 it will receive a notification. If now, the currently selected
          joystick is different from the other BUT it also HAS a button number 10, it will
          receive the notification. It will NOT receive notifications for a joystick that is not
          currently selected.
          
    See? Nothing bad happens. Things are going right. The observer of button number 10 always get a button notification
    when the button number 10 is pressed/depressed. And always it will receive that notification from the currently
    selected joystick...piuf...

    As I'm writting this, 11 July 2012, the goal of this model approach will be to create an abstraction between the
    not-so-low-level driver and QObjects keeping flexibility and extensibility. The main goal is to write the model
    once and enjoy the data using views. Probably, the Qt dependency in the model should be removed in some future.
    That will allow the model to be used by Gtk, Qt, and whichever GT.
    
    July 11, 2012 Sebastian Treu
    sebastian.treu(at)gmail.com
    """
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

    def stop(self):
        print("[JoystickModel]: stop")
        pygame.event.post(pygame.event.Event(pygame.QUIT, dict()))
        pygame.quit()

class EventDispatcher(QThread):
    
    def __init__(self, model, parent = None):
        print("[EventDispatcher]: init.")
        QThread.__init__(self, parent)
        self.model = model
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYHATMOTION])
        
    def __end__(self):
        print("[EventDispatcher]: end.")
    
    def run(self):
        self.alive = True
        print("[EventDispatcher]: Main loop starting...")
        while(self.alive):
            e = pygame.event.wait()
            if e.type == locals.QUIT:
                self.alive =False
            elif e.joy == self.model.currentJoystickId():
                # Don't process any event coming from joystick that are not
            # selected by the model.
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
                    self.model.notifyButtonChange(e.button, True)
                elif e.type == locals.JOYBUTTONUP:
                    #print("[EventDispatcher]: JOYBUTTONUP")
                    self.model.notifyButtonChange(e.button, False)
        print("[EventDispatcher]: Main loop finished.")

