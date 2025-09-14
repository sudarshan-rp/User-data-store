import webbrowser
import threading
import time
import uvicorn

def open_browser():
    # Wait a short time to let the server start
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8083/docs")


if __name__ == "__main__":
    #This runs open_browser concurrently so it won’t block the main thread.
    threading.Thread(target=open_browser).start()
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8083, reload=True)
