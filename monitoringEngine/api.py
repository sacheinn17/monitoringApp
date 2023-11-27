from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataBase import Database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()

@app.get("/time/total")
async def getTotalTime(day="today"):
   return db.getTotalTime(day)

@app.get("/time/{name}/")
async def getTimeByName(name,day = "all"):

   if day == "today":
      return db.getTimeByName(name,"today")
   
   elif day == "yesterday":
      return f"Yesterday's Usage Time is {db.getTimeByName(name,"yesterday")}"
   
   return db.getTimeByName(name,"all")

@app.get("/time/{name}/{context}/")
async def getTimeByContext(name,context):
   if context == "all":
      return db.getContextAndTimeByName(name = name)
   elif '-' in context:
      return db.getTimeByName(name,context)
   else:
      return {"The usage time of app in current context is ",db.getTimeByNameAndContext(name,context)}

@app.get("/time/{name}/{context}/today/")
async def getTimeAndNameByContext(name,context):
   return {"The usage time of app in current context is ",db.getTimeByNameandContextToday(name,context)}

@app.get("/updateLabel")
async def updateLabel(name:str="Brave",catogary:str="None",subCatogary:str = "UnSpecified",context:str="General"):
   return db.updateLabel(name,context,catogary,subCatogary)

@app.get("/refreshLabels/")
async def val():
   return db.refreshLabels()

@app.get("/getAll/")
async def val(date:str = "all"):
   return db.getAll(date)

@app.get("/namesAndContext")
async def getNamesAndContext():
    return db.getNameAndContext()

@app.get("/catogariesAndTime/")
async def getCatogariesAndTime(day:str = "today"):
   return db.getCatogariesAndTime(day) 

@app.get("/getAppUsageTime/")
async def getAppUsageTime(day="today"):
   return db.getAppUsageTime(day)

@app.get("/getCatNames/")
async def getCatNames():
   return db.getCatNames()