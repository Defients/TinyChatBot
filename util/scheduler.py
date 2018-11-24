
'''
Instantiate a Scheduler object, then schedule calls with
    S.add(Schedule.Event(delay, function-to-call))

Calling S.stop(delay) will exit the scheduler after delay seconds;
any events schedule after the stop time will not occur.

The delays can be specified as a number of seconds, or a string
such as '1h2m3s' for one hour plus two minutes plus three seconds.
'''

import time
from collections import namedtuple
import threading
from string_util import convert_to_seconds

class Event(object):
    def __init__(self, delay, f):
        try:
            delay = delay + 0
        except TypeError:
            delay = convert_to_seconds(delay)
        self.time = time.time() + delay
        self.f = f

class Scheduler(object):
    def __init__(self):
        self.events = []
        t = threading.Thread(name='Recur', target=self.sleep).start()

    def add(self, event):
        self.events.append(event)
        self.events.sort(key=lambda e: e.time)

    def sleep(self):
        if not self.events:
            time.sleep(1)
        else:
            event = self.events.pop(0)
            if event.f is None:
                print("\n\n\nFOUND STOP\n\n")
                self.events.clear()
                return
            delay = max(event.time - time.time(), 1)
            if delay > 1:
                self.events.insert(0, event)
                time.sleep(1)
            else:
                time.sleep(delay)
                try:
                    threading.Thread(target=event.f).start()
                except:
                    pass
        self.sleep()

    def stop(self, delay=0):
        self.add(Event(delay, None))
    
    def __str__(self):
        return '\nRecur: ' + '\n   '.join(f'{e.time-time.time()},{e.f}' for e in self.events)

if __name__ == '__main__':
    S = Scheduler()
    def f():
        print('f called')

    def runf():
        S.add(Event(1, f))

    base = 5
    S.add(Event(f'{base}s', f))
    S.add(Event(base + 3, f))
    S.add(Event(base + 4, f))
    S.stop(base + 7)
