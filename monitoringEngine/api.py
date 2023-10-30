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

@app.get("/")
async def getAllNames():
   return db.getAllNames()

@app.get("/time/{name}")
async def getTimeByName(name):
   return db.getTimeByName(name,"total")

@app.get("/time/{name}/{context}/")
async def getTimeByDay(name,context):
   if context == "today":
      return db.getTimeByName(name,"today")
   
   elif context == "yesterday":
      return f"Yesterday's Usage Time is {db.getTimeByName(name,"yesterday")}"
   
   elif context == "all":
      return db.getContextAndTimeByName(name = name)
   elif '-' in context:
      return db.getTimeByName(name,context)
   else:
      return {"The usage time of app in current context is ",db.getTimeByNameAndContext(name,context)}

@app.get("/time/{name}/{context}/today/")
async def val(name,context):
   return {"The usage time of app in current context is ",db.getTimeByNameandContextToday(name,context)}

@app.get("/updateLabel")
async def val(name:str="Brave",catogary:str="None",subCatogary:str = "UnSpecified",context:str="General"):
   return db.updateLabel(name,context,catogary,subCatogary)

@app.get("/refreshLabels/")
async def val():
   return db.refreshLabels()

@app.get("/getAll/")
async def val(date:str = "all"):
   return db.getAll(date)