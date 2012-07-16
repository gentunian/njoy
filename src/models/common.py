'''
Created on Jul 15, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
from src.models import events
import abc

class Joystick(object):
    """
        Joystick object should be independent objects. An abstraction of the underlying joystick hardware and platform.
        The main idea of this class is to hold a specific joystick information and to notify objects about changes in
        this object.
        
        Each observer should implement stateChanged(change) method where change is a JoystickChange object.
        
        Joysticks object holds each states for each capability in the _states dictionary. The _states dictionary holds
        keys for each kind of event. Each value has a list of values indexed by the id of the capability (see note*)
        
        When a high-level event is consumed by the EventConsumer object, it will provide each Joystick object the event
        argument into the processEvent(event) method. The Joystick object process the event, sets the appropiate
        Joystick state and notifies state change observers.
        
        (*) This is not quite true and should be noted. The __initStates__(count) method initializes the states of a
        capability upon the quantity of that capability. So, if this joystick has 10 buttons, the joystick buttons
        states will be indexed from 0 to 9. This is an assumption (maybe a bad one) that works with the linux device
        driver. The correct thing should be index not by the number of each capability but with THE capability id.
        That is, index the button 'p' state with 'p'.
    """
    def __init__(self, jid, name, buttons, axes, hats, balls):
        self._jid = jid
        self._states = {}
        self._states[events.BUTTON_EVENT] = self.__initStates__(buttons) 
        self._states[events.AXIS_EVENT] = self.__initStates__(axes)
        self._states[events.BALL_EVENT] = self.__initStates__(balls)
        self._states[events.HAT_EVENT] = self.__initStates__(hats)
        self._name = name
        self._observers = []
    
    def obs(self):
        return self._observers
    
    def __del__(self):
        pass
    
    def __initStates__(self, count):
        states = {}
        for i in range(count):
            states[i] = 0
        return states
    
    def __setStateValue__(self, eventType, state, eventValue):
        change = JoystickChange(eventType, self._states[eventType][state], eventValue)
        self._states[eventType][state] = eventValue
        self.__notifyChange__(change)
    
    def __notifyChange__(self, change):
        for observer in self._observers:
            try:
                observer.stateChanged(change)
            except Exception as ex:
                print("[Joystick]: An error ocurrer in the stateChanged() method for observer %s"%observer, ex)
    
    def processEvent(self, event):
        try:
            if event.eventType() == events.BUTTON_EVENT:
                state = event.button()
            elif event.eventType() == events.AXIS_EVENT:
                state = event.axis()
            elif event.eventType() == events.HAT_EVENT:
                state = event.hat()
            elif event.eventType() == events.BALL_EVENT:
                state = event.ball()
            else:
                print(": ", event.eventType())
                raise KeyError
            self.__setStateValue__(event.eventType(), state, event.value())
        except KeyError as ex:
            print("[Joystick]: error, ", ex)
    
    def addChangeObserver(self, observer):
        self._observers.append(observer)
    
    def removeChangeObserver(self, observer):
        self._observers.append(observer)
    
    def joyId(self):
        return self._jid
    
    def axes(self):
        len(self._axes)
    
    def buttons(self):
        len(self._buttons)
    
    def name(self):
        self._name

class JoystickChange(object):
    def __init__(self, change, oldValue, newValue):
        self._change = change
        self._oldValue = oldValue
        self._newValue = newValue
    
    def change(self):
        return self._change
    
    def oldValue(self):
        return self._oldValue
    
    def newValue(self):
        return self._newValue
    
    def __del__(self):
        pass

class JoystickChangeObserver(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stateChanged(self, change):
        print("{0:20} {1:10} {2:10}".format("Change Event", "New Value", "Old Value"))
        print("{0:20} {1:10d} {2:10d}".format(events.eventName[change.change()], change.newValue(), change.oldValue()))
