from dataBase import dbPath 
from monitoring import monitor
import uvicorn
from multiprocessing import freeze_support
import sys

d = monitor()
sys.stdin = open(dbPath + '\logs.txt','w')
sys.stdout = open(dbPath + '\logs.txt', 'w')

if __name__  == "__main__":
    freeze_support()

    d.startThread()
    uvicorn.run("api:app", port=1421, reload=False, workers = 2)
