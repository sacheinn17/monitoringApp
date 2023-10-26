import win32gui,time
import threading
import datetime
from dataBase import Database

db = Database()

class monitor():
    def __init__(self) -> None:
        self.app = ''
        self.context = ''
        self.time = 0
        self.lap = 0
        self.lap2 = 0
        self.date = datetime.datetime.today()
        self.date = datetime.date(self.date.year,self.date.month,self.date.day)
        a = threading.Thread(target = self.mointoring)
        a.start()

    def mointoring(self):
        while True:
            hwnd = win32gui.GetForegroundWindow()
            name = win32gui.GetWindowText(hwnd)
            new_window_name = name.split(' - ')
            application = new_window_name[-1][0:30]
            context = new_window_name[1 if len(new_window_name)>2 else 0][0:50]

            if application != self.app or context != self.context and name != "Task Switching" and application != '':
                print(new_window_name)
                self.changed()
                self.lap = self.time
            
            if self.time - self.lap >240:
                self.changed()

            self.app = application
            self.context = context
            time.sleep(1)
            self.time +=1

    def changed(self):
        difference = self.time-self.lap
        # print(difference)
        if difference >3:
            # print("Entered loop")
            x,exist = db.exists(self.app,self.context)
            if exist:
                db.updateTime(x,difference)
            else:
                db.addEntry(self.app,self.context,difference)

d = monitor()
