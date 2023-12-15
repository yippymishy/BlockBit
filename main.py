import threading
import os
import subprocess
import time

print('===== BlockBit Server =====')

def kill_process_by_name(name):
    subprocess.call(['pkill', '-f', name])


def api():
    os.system(" API.py")


def server():
    os.system("python server.py")


#t = threading.Thread(target=api, args=())
t2 = threading.Thread(target=server, args=())
#t.start()
t2.start()