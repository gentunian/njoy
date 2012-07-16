'''
Created on Jul 14, 2012


    Ideas taken from: http://www.jezra.net/blog/Python_Joystick_Class_using_Gobject
    by Copyright 2009 Jezra Lickter 
    
    And from: http://www.kernel.org/doc/Documentation/input/joystick-api.txt
    
    Doc from joystick.h:
    
    /usr/include/linux/joystick.h:#define JSIOCGVERSION        _IOR('j', 0x01, __u32)                /* get driver version */
    /usr/include/linux/joystick.h:#define JSIOCGAXES        _IOR('j', 0x11, __u8)                /* get number of axes */
    /usr/include/linux/joystick.h:#define JSIOCGBUTTONS        _IOR('j', 0x12, __u8)                /* get number of buttons */
    /usr/include/linux/joystick.h:#define JSIOCGNAME(len)        _IOC(_IOC_READ, 'j', 0x13, len)            /* get identifier string */
    /usr/include/linux/joystick.h:#define JSIOCSCORR        _IOW('j', 0x21, struct js_corr)            /* set correction values */
    /usr/include/linux/joystick.h:#define JSIOCGCORR        _IOR('j', 0x22, struct js_corr)            /* get correction values */
    /usr/include/linux/joystick.h:#define JSIOCSAXMAP        _IOW('j', 0x31, __u8[ABS_CNT])            /* set axis mapping */
    /usr/include/linux/joystick.h:#define JSIOCGAXMAP        _IOR('j', 0x32, __u8[ABS_CNT])            /* get axis mapping */
    /usr/include/linux/joystick.h:#define JSIOCSBTNMAP        _IOW('j', 0x33, __u16[KEY_MAX - BTN_MISC + 1])    /* set button mapping */
    /usr/include/linux/joystick.h:#define JSIOCGBTNMAP        _IOR('j', 0x34, __u16[KEY_MAX - BTN_MISC + 1])    /* get button mapping */
    
@author: Sebastian Treu
@author: sebastian.treu(at)gmail.com
'''
import sys
import select
from threading import Thread
from multiprocessing import Process
from multiprocessing import Queue
from struct import unpack
from struct import calcsize
from fcntl import ioctl
from src.models import events
from src.models.common import Joystick, JoystickChangeObserver

def sizeof(atype): 
    return calcsize(atype)

def _IOC(d, atype, nr, size):  
    return int((d << _IOC_DIRSHIFT ) | (atype << _IOC_TYPESHIFT ) | (nr << _IOC_NRSHIFT ) | (size << _IOC_SIZESHIFT))

def _IO(atype, nr):
    return _IOC(_IOC_NONE,  atype, nr, 0)

def _IOR(atype,nr,size): 
    return _IOC(_IOC_READ,  atype, nr, sizeof(size))

def _IOW(atype,nr,size): 
    return _IOC(_IOC_WRITE, atype, nr, sizeof(size))

_IOC_SIZEBITS   = 14
_IOC_SIZEMASK   = (1 << _IOC_SIZEBITS ) - 1
_IOC_NRSHIFT    = 0
_IOC_NRBITS     = 8
_IOC_TYPESHIFT  = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_TYPEBITS   = 8
_IOC_SIZESHIFT  = _IOC_TYPESHIFT + _IOC_TYPEBITS
IOCSIZE_MASK    = _IOC_SIZEMASK << _IOC_SIZESHIFT
IOCSIZE_SHIFT   = _IOC_SIZESHIFT

# Python 2.2 uses a signed int for the ioctl() call, so ...
if ( sys.version_info[0] < 3 ) or ( sys.version_info[1] < 3 ):
    _IOC_WRITE      =  1
    _IOC_READ       = -2
    _IOC_INOUT      = -1
else:
    _IOC_WRITE      =  1
    _IOC_READ       =  2
    _IOC_INOUT      =  3

_IOC_DIRSHIFT   = _IOC_SIZESHIFT + _IOC_SIZEBITS
IOC_INOUT       = _IOC_INOUT << _IOC_DIRSHIFT
IOC_IN          = _IOC_WRITE << _IOC_DIRSHIFT
IOC_OUT         = _IOC_READ << _IOC_DIRSHIFT
_IOC_NONE       = 0
JOY = ord('j')



class DeviceReader(Process):
    """
        This process is dedicated to do convertions from low-level API to high-level events.
        
        The main reason of this class is to read from file devices (in this case, joystick devices),
        interpret the low-level event received by the device in order to create a high-level event
        (JoystickEvent's objects) and be putted in a shared Queue. 
        
        The shared Queue is also used by EventConsumer thread. This thread creates the joysticks objects
        when appropiate (i.e. a JoystickNewEvent is read in the Queue). The main idea is to leave the
        DeviceReader process reading trying to keep latency low, instead of that process invoking 
        joystick objects method (that could slow down the next read).
        
        As soon as a JoystickEvent is put into the shared Queue, the EventConsumerthrea uses that
        information and pass back the event to the appropiate joystick object (or it creates a new one).
        Joystick objects then, notify the change of their states to the objects that are interested in
        joystick changes and implementes stateChanged() method.
    """
    EVENT_BUTTON = 0x01 #button pressed/released 
    EVENT_AXIS = 0x02  #axis moved  
    EVENT_INIT = 0x80  #button/axis initialized  
    #see http://docs.python.org/library/struct.html for the format determination 
    EVENT_FORMAT = "IhBB" 
    EVENT_SIZE = calcsize(EVENT_FORMAT)
    JSIOCGVERSION = _IOR(JOY, 0x01, 'I')
    JSIOCGAXES = _IOR(JOY, 0x11, 'c')
    JSIOCGBUTTONS = _IOR(JOY, 0x12, 'c')
    JSIOCGNAME = _IOC(_IOC_READ, JOY, 0x13, 20)
    
    def __init__(self, queue):
        print("[DeviceReader]: Init")
        super(DeviceReader, self).__init__()
        # this is while testing. devNames should be calculated
        self.devNames = ['/dev/input/js0', '/dev/input/js1'] 
        # file descriptor -> file object (is it worth it?) Just fd needed.
        self.files = {} 
        # Message events queue
        self.queue = queue
        #self.joyList = jlist 
        self.__initDevices__()
        #self.consumer = EventConsumer(jlist, self.queue)
        #self.consumer.start()

    def __del__(self):
        print("[DeviceReader]: Object no more exists.")
    
    def run(self):
        print("[DeviceReader]: Starting Main loop...")
        self.connected = True
        while(self.connected):
            try:
                r, w, x = select.select(self.files.keys(), [], []) #@UnusedVariable
                for fd in r:
                    try:
                        #read self.EVENT_SIZE bytes from the joystick 
                        read_event = self.files[fd].read(self.EVENT_SIZE)
                        #get the event structure values from  the read event 
                        time, value, eType, number = unpack(self.EVENT_FORMAT, read_event)
                        if eType == self.EVENT_AXIS:
                            self.queue.put(events.JoystickAxisEvent(time, fd, number, value))
                        elif eType == self.EVENT_BUTTON:
                            self.queue.put(events.JoystickButtonEvent(time, fd, number, value))
                    except (KeyboardInterrupt, SystemExit):
                        print("[DeviceReader]: KeyboardInterrupt or SystemExit while reading device. DeviceReader will die.")
                        self.connected = False
                        break # we need to abort the for loop
                    except:
                        print("[DeviceReader]: Error while reading fd %d. Joystick will be removed"%fd)
                        self.files.remove(fd)
                        self.queue.punt(events.JoystickDisconnectEvent(time, fd))
            except (KeyboardInterrupt, SystemExit):
                print("[DeviceReader]: KeyboardInterrupt or SystemExit while reading select() call. DeviceReader will die.")
                self.connected = False
            except:
                print("[DeviceReader]: Error while selecting")
                self.connected = False
        # send the quit event for the consumer thread to stop.
        self.queue.put(events.Event(events.QUIT_EVENT))
        
        
    def __initDevices__(self):
        """
            Initialize the devices that were found. devNames should be a list of joystick
            devices. This is a specific linux portion. Joysticks are generally register
            in kernel dev nodes as /dev/input/js*. That may vary between linux distributions.
            
            The idea is to provide a way to get a list of joysticks devices in devNames for then
            be opened by this object.
            
            Once the device was opened successfully, some information is queried to the device.
            The joystick name, buttons count, axes, etc. When all that info is filled in, a
            JoystickNewEvent is created and putted into the shared Queue.
        """
        print("[DeviceReader]: init devices...")
        for device in self.devNames:
            try:
                f = open(device)
                print("[DeviceReader]: device name: %s f descriptor: %d " % (device, f.fileno()))
                axes = unpack('B', ioctl(f, self.JSIOCGAXES, " "))[0]
                buttons = unpack('B', ioctl(f, self.JSIOCGBUTTONS, " "))[0]
                name = ioctl(f, self.JSIOCGNAME, " ".rjust(128)).strip()
                #print("[DeviceReader]: Joystick id %d, name: %s, axes: %d, buttons: %d" % (f.fileno(), name, axes, buttons))
                e = events.JoystickNewEvent(0, f.fileno(), name[:len(name)-1], buttons, axes, 0, 0)
                self.queue.put(e)
                self.files[f.fileno()] = f
                #joystick = Joystick(f.fileno(),  name, buttons, axes, 0, 0)
                #self.joyList[joystick.jid()] = joystick
            except Exception as ex:
                print("[DeviceReader]: Some Error ", ex)
    
class EventConsumer(Thread):
    """
        The EventConsumer class is a thread that waits input in a shared Queue. The shared queue is filled in
        by the DeviceReader process and it's shared between this two processes. EventConsumer thread interprets
        high-level events and distributes these events to each joystick in the joystick list.
    """
    def __init__(self, jlist, q):
        print("[EventConsumer]: Init ")
        super(EventConsumer, self).__init__()
        self.consuming = False
        self.joyList = jlist
        self.queue = q
        
    def __del__(self):
        print("[EventConsumer]: Object no more exists.")
    
    def run(self):
        self.consuming = True

        while(self.consuming):
            e = self.queue.get()
            if e.eventType() == events.NEW_EVENT:
                print("[EventConsumer]: New joystick event (%d, %d, %d, %d, %d, %s)" % (e.jid(), e.buttons(), e.axes(), e.hats(), e.balls(), e.name()))
                joystick = Joystick(e.jid(),  e.name(), e.buttons(), e.axes(), e.hats(), e.balls())
                self.joyList[e.jid()] = joystick
            elif e.eventType() == events.QUIT_EVENT:
                self.consuming = False
            elif e.eventType() == events.DISCONNECT_EVENT:
                print("[EventConsumoer]: Joystick %d won't receive events anymore."%e.jid())
                del self.joyList[e.jid()]
            else:
                print("[EventConsumer]: Event: %s"%events.eventName[e.eventType()])
                p = Process(target=self.processEvent, args=(e,))
                p.start()

    def processEvent(self, e):
        print("[EventConsumer]: Processing event %s"%events.eventName[e.eventType()])
        self.joyList[e.jid()].processEvent(e)

class JoystickModel(object):
    """
        This class holds the joysticks objects. The joystick list is passed to the EventConsumer thread in order
        to fill the list with joystick objects. This fill procedure is done when a JoystickNewEvent is found in the
        queue by the EventConsumer thread.
        
        If someone is interested in a specific joystick in order to detect changes in its state, the procedure should
        be as follows:
        
            model = JoystickModel()
            # some wait must be done here
            time.sleep(2)
            # retrieve the joystick list
            for joystick in model.joysticks():
                joystick.addChangeObserver(observer)
        
        Each object interested in states changes should implement stateChanged(change) method, where change is an object
        providing information about what have changed in the joystick object. A class JoystickChangeObserver is provided
        as an abstract class. Its stateChanged(change) method does nothing more than print the change object. No restriction
        is provided in the addChangeObserver(observer) method, so any object could be passed by as an argument. The reason
        is that joystick objects will "try" to call stateChanged(change) method, if that fails, nothing is done:
        
            def __notifyChange__(self, change):
                for observer in self._observers:
                    try:
                        observer.stateChanged(change)
                    except Exception as ex:
                        print("[Joystick]: An error ocurrer in the stateChanged() method for observer %s"%observer, ex)
        
        Change objects provides the change made (the event type, i.e. events.AXIS_EVENT), the old value, and the new value.
    """
    def __init__(self):
        self.joylist = {}
        self.queue = Queue()
        self.reader = DeviceReader(self.queue)
        self.reader.start()
        self.consumer = EventConsumer(self.joylist, self.queue)
        self.consumer.start()
    
    def joysticks(self):
        return self.joylist.values()
    
    def __del__(self):
        print("[JoystickModel]: Object no more exists.")
        self.reader.join(5)
    
if __name__ == '__main__':
    import time
    class Observer(JoystickChangeObserver):
        def stateChanged(self, change):
            super(Observer, self).stateChanged(change)
            while(True):
                pass

    observer = Observer()
    model = JoystickModel()
    time.sleep(2)
    for joy in model.joysticks():
        joy.addChangeObserver(observer)

