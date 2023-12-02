from monitoring import monitor
import threading
import uvicorn
import api


d = monitor()
if __name__  == "__main__":
    d.startThread()
    uvicorn.run("api:app", port=1421, reload=False, access_log=False)