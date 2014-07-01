import threading
import time
class SensorTimer:
    def defaultAcquisition(self):
        return 0
    
    def __init__(self, acquisitionFrequency, callback, acquisitionFunction=defaultAcquisition):
        self.acquire = acquisitionFunction
        self.period = 1/acquisitionFrequency
        self.callback = callback


    def start(self):
       self.callback(self.acquire())
       self.threadControl = threading.Timer(self.period, self.start)
       self.threadControl.start()

    def stop(self):
        self.threadControl.cancel();


class SensorThread(threading.Thread):
    
    def defaultAcquisition(self):
        return 0
    
    def __init__(self, acquisitionFrequency, acquisitionFunction=defaultAcquisition):
        threading.Thread.__init__(self)
        self.acquire = acquisitionFunction
        self.period = 1/acquisitionFrequency
        self.readValue = 0;
        self.lock = threading.Lock()
        self._stop = False

    def run(self):
        while True:
            time.sleep(self.period)
            self.lock.acquire()
            self.readValue = self.acquire()
            if self.stop:
                self.lock.release()
                return
            self.lock.release()

    def stop(self):
        self.lock.acquire()
        self._stop = True
        self.lock.release()

    def read(self):
        self.lock.acquire()
        retValue = self.readValue
        self.lock.release()
        return retValue
