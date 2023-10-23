import threading
import os
import subprocess
import time


def kill_process_by_name(name):
    subprocess.call(['pkill', '-f', name])


def api():
    os.system("python API.py")


def server():
    os.system("python server.py")


# Once per hour, restart the server and API
while True:
    t = threading.Thread(target=api, args=())
    t2 = threading.Thread(target=server, args=())
    t.start()
    t2.start()

    time.sleep(3600)

    kill_process_by_name('API.py')
    kill_process_by_name('server.py')
