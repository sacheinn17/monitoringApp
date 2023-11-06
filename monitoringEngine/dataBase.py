from schema import AppUsage,Base,rules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import json


engine = create_engine('sqlite:///monitoring.db',connect_args={"check_same_thread": False})
Session = sessionmaker(bind = engine)
session = Session()

rulesQuery = session.query(rules)
appUsageQuery = session.query(AppUsage)
class Database():
    def __init__(self):
        Base.metadata.create_all(engine)
        self.date = str(datetime.datetime.today().date())

    def exists(self,appName,Context):
        t = appUsageQuery
        
        t = t.filter_by(appName = appName).filter_by(context = Context).filter_by(date=self.date)
        u = t.filter_by(appName = Context).filter_by(context = appName).filter_by(date=self.date)
        if t.first() is not None:
            return (t,True)
        elif u.first() is not None:
            return(u,True)
        else:
            return(-1,False)
    def getCatAndSubCatAndSwap(self,name,context):
        flip = False
        temp = rulesQuery.filter_by(name = name)
        temp2 = rulesQuery.filter_by(name = context)
        
        catogary = "UnCatogarized"
        subCatogary = "UnCatogarized"

        if temp.first() is not None:
            tempCatogary = temp.filter_by(context = context)

            if tempCatogary.first() is not None:
                catogary = tempCatogary.first().catogary
                subCatogary = tempCatogary.first().subCatogary
                flip = tempCatogary.first().flip
            else:
                tempGeneral = temp.filter_by(context = "General")
                if tempGeneral.first() is not None:
                    catogary = tempGeneral.first().catogary
                    subCatogary = tempGeneral.first().subCatogary
                    flip = tempGeneral.first().flip

        if temp2.first() is not None:
            tempCatogary = temp.filter_by(context = name)
            if tempCatogary.first() is not None:
                catogary = tempCatogary.first().catogary
                subCatogary = tempCatogary.first().subCatogary
                flip = tempCatogary.first().flip
            else:
                tempGeneral = temp2.filter_by(context = "General")
                if tempGeneral.first() is not None:
                    catogary = tempGeneral.first().catogary
                    subCatogary = tempGeneral.first().subCatogary
                    flip = tempGeneral.first().flip
        
        return (catogary,subCatogary,flip)
    def addEntry(self,name,context,time):
        catogary,subCatogary,flip = self.getCatAndSubCatAndSwap(name,context)
        c = None
        if not flip:
            c = AppUsage(appName = name,context = context,date = self.date,usageTime = time,catogary = catogary,subCatogary = subCatogary)
        else:
            c = AppUsage(appName = context,context = name,date = self.date,usageTime = time,catogary = catogary,subCatogary = subCatogary)

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
    def refreshDate(self):
        self.date = str(datetime.datetime.today().date())
    
    def getTimeByName(self,name,filter = "all"):
        t = appUsageQuery.filter_by(appName=name)
        if filter != "all":
            if filter == "today":
                t =  t.filter_by(date = self.date)
                
            elif '-' in filter:
                t =  t.filter_by(date = filter)
            
            elif filter == "yesterDay":
                y = self.yesterDayDate()
                t = t.filter_by(date = y)
            
        time = 0
        for v in t:
            time += v.usageTime
        return time/60
    def getTimeByNameAndContext(self,name,context):
        t = appUsageQuery.filter_by(appName=name).filter_by(context= context)
        time = 0
        for v in t:
            time += v.usageTime
        return time/60.0
    def getContextByName(self,name):
        t = appUsageQuery.filter_by(appName=name)
        context = []
        for v in t:
            context.append(t.context)
        return context
    def getContextAndTimeByName(self,name):
        t = appUsageQuery.filter_by(appName=name)
        contextAndTime = {}
        for i in t:
            contextAndTime[i.context] = self.getTimeByNameAndCotext(name = name,context = i.context)
        return json.dumps(contextAndTime)
    def getAppUsageTime(self,day):
        date = self.date if day =="today" else day
        temp = appUsageQuery.filter_by(date = date)
        names = []
        retVal = []

        for i in temp:
            names.append(i.appName)
        names = list(set(names))
        print(names)

        for i in names:
            x = temp.filter_by(appName = i)
            time = 0
            for j in x:
                time += j.usageTime
            retVal.append({"name":i,
                           "time":time})
        print(retVal)
        return json.dumps(retVal)

    def getTotalTime(self,day = "today"):
        date = self.date if day == "today" else day
        t = appUsageQuery.filter_by(date = date)
        time = 0
        for i in t:
            time += i.usageTime
        return time
    def updateLabel(self,name,context,catogary,subCatogary):
        # return name
        x = rulesQuery.filter_by(name = name).filter_by(context=context)
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
        rulesdb = rulesQuery
        appUsagedb = appUsageQuery

        for i in rulesdb:
            temp = appUsagedb.filter_by(appName=i.name)
            if i.context != "General":
                temp = appUsagedb.filter_by(context = i.context)
            temp.update({"catogary":i.catogary})
            temp.update({"subCatogary":i.subCatogary})
            session.commit()
        return True
    def getAll(self,date):
        temp = appUsageQuery
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
    def getNameAndContext(self):

        temp = appUsageQuery
        names = []
        retVal = []

        for i in temp:
            names.append(i.appName)
        names = list(set(names))
        print(names)

        for i in names:
            x = temp.filter_by(appName = i)
            temp_2 = []
            for j in x:
                temp_2.append(j.context)
            retVal.append({i:temp_2})      

        return json.dumps(retVal)
    def getTimeByCatogaries(self,day):
        date = self.date if day =="today" else day
        temp = appUsageQuery.filter_by(date = date)
        names = []
        retVal = []

        for i in temp:
            names.append(i.appName)
        names = list(set(names))

        for i in names:
            x = temp.filter_by(i)
            temp_2 = []
            for j in x:
                temp_2.append(j.context)
            retVal.append({i:temp_2})      
        return json.dumps(retVal)  
    def getCatogariesAndTime(self,day):
        date = self.date if day =="today" else day
        temp = appUsageQuery.filter_by(date = date)
        catogaries = []
        retVal = []

        for i in temp:
            catogaries.append(i.catogary)
        catogaries = list(set(catogaries))
        print(catogaries)

        for i in catogaries:
            x = temp.filter_by(catogary = i)
            time = 0
            for j in x:
                time += j.usageTime
            retVal.append({"name":i,
                           "time":time})
        print(retVal)
        return json.dumps(retVal)