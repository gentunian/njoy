'''
Created on Jul 14, 2012

@author: Sebastian Treu
@authot: sebastian.treu(at)gmail.com
'''
BUTTON_EVENT = 0
AXIS_EVENT = 1
HAT_EVENT = 2
BALL_EVENT = 3
NEW_EVENT = 4
QUIT_EVENT = 5
DISCONNECT_EVENT = 6

eventName = { BUTTON_EVENT : 'BUTTON_EVENT',
             AXIS_EVENT : 'AXIS_EVENT',
             HAT_EVENT: 'HAT_EVENT',
             BALL_EVENT: 'BALL_EVENT',
             NEW_EVENT: 'NEW_EVENT',
             QUIT_EVENT: 'QUIT_EVENT',
             DISCONNECT_EVENT: 'DISCONNECT_EVENT'
             }

class Event(object):
    def __init__(self, eType):
        super(Event, self).__init__()
        self._eType = eType
    
    def eventType(self):
        return self._eType

class JoystickEvent(Event):
    def __init__(self, eType, time, jid, what = None, value = None):
        super(JoystickEvent, self).__init__(eType)
        self._jid = jid
        self._type = eType
        self._value = value
        self._time = time
        self._what = what
    
    def jid(self):
        return self._jid
    
    def time(self):
        return self._time
    
    def value(self):
        return self._value

    def what(self):
        return self._what
    
class JoystickNewEvent(JoystickEvent):
    def __init__(self, time, jid, name, buttons, axes, hats, balls):
        print("[JoystickNewEvent]: (%dms) jid: %d, name: %s, buttons: %d, axes: %d, hats: %d, balls: %d" % (time, jid, name, buttons, axes, hats, balls))
        super(JoystickNewEvent, self).__init__(NEW_EVENT, time, jid)
        self._name = name
        self._buttons = buttons
        self._axes = axes
        self._hats = hats
        self._balls = balls
    
    def name(self):
        return self._name
    
    def buttons(self):
        return self._buttons
    
    def hats(self):
        return self._hats
    
    def balls(self):
        return self._balls
    
    def axes(self):
        return self._axes

class JoystickDisconnectEvent(JoystickEvent):
    def __init__(self, time, jid):
        super(JoystickDisconnectEvent, self).__init__(DISCONNECT_EVENT, time, jid)
