import os
import threading

def start_server():
    os.system("python server.py")

def start_api():
    os.system("python api.py")

server = threading.Thread(target=start_server)
api = threading.Thread(target=start_api)

server.start()
api.start()