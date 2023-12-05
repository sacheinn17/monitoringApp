import win32gui,time
import threading
from dataBase import Database

db = Database()

class monitor():
    def __init__(self) -> None:
        self.app = ''
        self.context = ''
        self.time = int(time.time())
        self.lap = self.time
        self.event = threading.Event()
        self.a = threading.Thread(target = self.mointoring)
        self.a.daemon = True
    
    def startThread(self):
        db.refreshDate()
        self.a.start()

    def mointoring(self):
        while not self.event.is_set():
                hwnd = win32gui.GetForegroundWindow()
                # print(self.time)
                name = win32gui.GetWindowText(hwnd)
                new_window_name = name.split(' - ')
                application = new_window_name[-1][0:30]
                context = new_window_name[1 if len(new_window_name)>2 else 0][0:50]

                self.ignoreList = ['',"Windows Default Lock Screen","Task Switching","Task Switching","",None]

                if (application != self.app or context != self.context):
                    self.changed()

                self.app = application
                self.context = context
                
                if self.time - self.lap >300:
                    self.changed()  
                    db.refreshDate()

                self.time = int(time.time())
                time.sleep(1)

    def changed(self):
        if self.app not in self.ignoreList:
            difference = self.time-self.lap
            self.lap = self.time
            # print(self.app,self.context, self.time)
            if difference >3:
                x,exist = db.exists(self.app,self.context)
                if exist:
                    db.updateTime(x,difference)
                else:
                    db.addEntry(self.app,self.context,difference)