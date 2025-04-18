import os
import threading

def start_server():
    os.system("python server.py")

def start_api():
    os.system("python api.py")

def cloudflare_tunnel():
    os.system("cloudflared tunnel run blockbit-tunnel")

server = threading.Thread(target=start_server)
api = threading.Thread(target=start_api)
cloudflare = threading.Thread(target=cloudflare_tunnel)

server.start()
api.start()
cloudflare.start()