from schema import AppUsage,Base,rules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import json


engine = create_engine('sqlite:///monitoring.db',connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
session = Session()

class Database():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.date = str(datetime.datetime.today().date())

    def exists(self,appName,Context):
        t = session.query(AppUsage)
        
        t = t.filter_by(appName = appName).filter_by(context = Context).filter_by(date=self.date)
        exist = t.first() is not None
        return (t if exist else -1,exist)
    
    def addEntry(self,name,context,time):
        temp = session.query(rules).filter_by(name = name)
        
        catogary = "UnCatogarized"
        subCatogary = "UnCatogarized"

        if temp.first() is not None:
            tempCatogary = temp.filter_by(context = context)
            if tempCatogary.first() is not None:
                catogary = tempCatogary.first().catogary
                subCatogary = tempCatogary.first().subCatogary    
            else:            
                catogary = temp.first().catogary
                subCatogary = temp.first().subCatogary


        c = AppUsage(appName = name,context = context,date = self.date,usageTime = time,catogary = catogary,subCatogary = subCatogary)
        session.add(c)
        session.commit()
    
    def updateTime(self,val,time):
        try:
            val.update({"usageTime":val.first().usageTime+(time)})
            session.commit()
        except Exception as e:
            print(e)
    def yesterDayDate(self):
            x = list(map(int,self.date.split('-')))
            x[-1] = x[-1] -1
            y = f"{x[0]}-{x[1]}-{x[2]}"
            print(y)

            return y
    
    def getTimeByName(self,name,filter = "total"):
        t = session.query(AppUsage).filter_by(appName=name)
        if filter != "total":
            if filter == "today":
                t =  t.filter_by(date = self.date)
            
            elif filter == "yesterDay":
                y = self.yesterDayDate()
                t = t.filter_by(date = y)
            
            elif '-' in filter:
                t =  t.filter_by(date = filter)

        time = 0
        for v in t:
            time += v.usageTime
        return time/60
    def getTimeByNameAndContext(self,name,context):
        t = session.query(AppUsage).filter_by(appName=name).filter_by(context= context)
        time = 0
        for v in t:
            time += v.usageTime
        return time/60.0
    def getContextByName(self,name):
        t = session.query(AppUsage).filter_by(appName=name)
        context = []
        for v in t:
            context.append(t.context)
        return context
    def getContextAndTimeByName(self,name):
        t = session.query(AppUsage).filter_by(appName=name)
        contextAndTime = {}
        for i in t:
            contextAndTime[i.context] = self.getTimeByNameAndCotext(name = name,context = i.context)
        return contextAndTime
    def getTotalTime(self,day = "Today"):
        t = session.query(AppUsage).filter_by(date = self.date)
        time = 0
        for i in t:
            time += i.usageTime
        return time
    def updateLabel(self,name,context,catogary,subCatogary):
        # return name
        x = session.query(rules).filter_by(name = name).filter_by(context=context)
        if x is None:
            print(name)
            return catogary
        for i in x:
            print(i.catogary)
        # x = x.first()
        print(str(name))
        if x.first() is not None:
            x.update({"catogary":catogary})
            x.update({"subCatogary":subCatogary})
            session.commit()
            
            return f"Value Updated {x}"
        else:
            temp = rules(name = name,context = context,catogary = catogary,subCatogary=subCatogary)
            session.add(temp)
            session.commit()
            return "New value added"
    def refreshLabels(self):
        rulesdb = session.query(rules)
        appUsagedb = session.query(AppUsage)

        for i in rulesdb:
            temp = appUsagedb.filter_by(appName=i.name)
            if i.context != "General":
                temp = appUsagedb.filter_by(context = i.context)
            temp.update({"catogary":i.catogary})
            temp.update({"subCatogary":i.subCatogary})
            session.commit()
        return "Labels refreshed"
    def getAll(self,date):
        temp = session.query(AppUsage)
        retVal = []
        if date != "all":
            if date == "today":
                temp = temp.filter_by(date = self.date)
            elif date == "yesterday":
                temp = temp.filter_by(date = self.yesterDayDate)
            else:
                temp = temp.filter_by(date = date)
        for i in temp:
            retVal.append([i.appName,i.context,i.date,i.usageTime,i.catogary,i.subCatogary])
        return(retVal)

    def getAllNames(self):
        temp = session.query(AppUsage)
        retVal = []

        for i in temp:
            retVal.append({"appName":i.appName,"context":i.context})
        return json.dumps(retVal)