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
    def __init__(self, eType, time, jid, value = None):
        super(JoystickEvent, self).__init__(eType)
        self._jid = jid
        self._type = eType
        self._value = value
        self._time = time
    
    def jid(self):
        return self._jid
    
    def time(self):
        return self._time
    
    def value(self):
        return self._value

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

class JoystickButtonEvent(JoystickEvent):
    def __init__(self, time, jid, button, value):
        print("[JoystickButtonEvent]: (%dms) jid: %d, button: %d, value: %d" % (time, jid, button, value))
        super(JoystickButtonEvent, self).__init__(BUTTON_EVENT, time, jid, value)
        self._button = button
        
    def button(self):
        return self._button
    
class JoystickAxisEvent(JoystickEvent):
    def __init__(self, time, jid, axis, value):
        print("[JoystickAxisEvent]: (%dms) jid: %d, axis: %d, value: %d" % (time, jid, axis, value))
        super(JoystickAxisEvent, self).__init__(AXIS_EVENT,time, jid, value)
        self._axis = axis

    def axis(self):
        return self._axis
    
class JoystickHatEvent(JoystickEvent):
    def __init__(self, time, jid, hat, value):
        print("[JoystickHatEvent]: (%dms) jid: %d, hat: %d, value: %d" % (time, jid, hat, value))
        super(JoystickHatEvent, self).__init__(HAT_EVENT, time, jid, value)
        self._hat = hat

    def hat(self):
        return self._hat
    
class JoystickBallEvent(JoystickEvent):
    def __init__(self, time, jid, ball, value):
        print("[JoystickBallEvent]: (%dms) jid: %d, ball: %d, value: %d" % (time, jid, ball, value))
        super(JoystickHatEvent, self).__init__(BALL_EVENT,time, jid, value)
        self._ball = ball

    def hat(self):
        return self._hat