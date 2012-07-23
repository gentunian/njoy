'''
Created on Jul 16, 2012

@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''

from PyQt4.QtCore import QEvent

class JoystickEvent(QEvent):
    def __init__(self, event):
        super(JoystickEvent, self).__init__(QEvent.User)
        self.e = event
    
    def what(self):
        return self.e.what()
    
    def value(self):
        return self.e.value()
    
    def eventType(self):
        return self.e.eventType()