import win32gui,time
import threading
from dataBase import Database
import sys

db = Database()
class monitor():
    def __init__(self) -> None:
        self.app = ''
        self.context = ''
        self.time = time.time()
        self.lap = self.time
        self.event = threading.Event()
        self.a = threading.Thread(target = self.mointoring)
        self.a.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.event.set()
            time.sleep(0.2)
            sys.exit(0)

    def signal_handler(self,s,t):
        print('You pressed Ctrl+C!')
        self.event.set()
        time.sleep(0.2)
        sys.exit(0)

    def mointoring(self):
        while not self.event.is_set():
                hwnd = win32gui.GetForegroundWindow()
                name = win32gui.GetWindowText(hwnd)
                new_window_name = name.split(' - ')
                application = new_window_name[-1][0:30]
                context = new_window_name[1 if len(new_window_name)>2 else 0][0:50]

                if application != self.app or context != self.context and name != "Task Switching" and application != '':
                    # print(new_window_name)
                    self.changed()
                    # print(self.time,self.lap)
                    self.lap = self.time
                
                if self.time - self.lap >240:
                    self.changed()

                self.app = application
                self.context = context
                self.time = time.time()
                time.sleep(1)

    def changed(self):
        difference = self.time-self.lap
        print(difference)
        if difference >3:
            # print("Entered loop")
            x,exist = db.exists(self.app,self.context)
            if exist:
                db.updateTime(x,difference/60)
            else:
                db.addEntry(self.app,self.context,difference/60)

d = monitor()

