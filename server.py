# Import the necessary modules
import scratchattach as sa
from local_simple_database import LocalDictDatabase
import ast
import time
from datetime import datetime
import threading

# Read the session ID from a file for login
with open('secrets/session_id.txt', 'r') as session_id_txt:
    session_id = str(session_id_txt.read())

# Read the admins list
with open("admins.txt", "r") as admins_txt:
    admins_list = admins_txt.readlines()
    admins_list = [i.replace("\n", "").replace(" ", "").lower() for i in admins_list]

# Connect to Scratch
project_id = 669020072

session = sa.login_by_id(session_id, username="BlockBit-server") #replace with your session_id and username
cloud = session.connect_cloud(project_id) #replace with your project id
client = cloud.requests(used_cloud_vars=["1‎", "2‎", "3‎", "4‎"])
# Setup database
LDD = LocalDictDatabase(str_path_database_dir=".", default_value=None)

# "db" is the database for balances (dict_balances.txt)
db = LDD["dict_balances"]
notifications_db = LDD["dict_notifications"]
transactions_db = LDD["dict_transactions"]
preferences_db = LDD["dict_preferences"]

# Set the default values for some databases
#LDD["dict_balances"].change_default_value(False)
LDD["dict_notifications"].change_default_value([])
LDD["dict_preferences"].change_default_value(
    {"theme": "blue", "mute": "False"}
)

# Define a function to clean and standardize user names
def fix_name(name):
    return name.replace(" ", "").replace("@", "").lower()

# Functions to set and get user balances
def set_balance(user, amount):
    db[fix_name(user)] = float(amount)

def get_balance(user):
    return round(db[fix_name(user)])

# Function to get the top balances in a leaderboard
def get_leaderboard(amount, offset):
    info = db.get_value()
    info = {key: val for key, val in sorted(info.items(), key=lambda ele: ele[1], reverse=True)}
    res = dict(list(info.items())[offset: offset + amount])
    return res

# Function to create a formatted leaderboard
def create_leaderboard():
    top = get_leaderboard(10, 0)
    top = [f"{i}: {round(top[i])}" for i in top]
    return top

# Create a transaction ID
def create_id(inp):
    mybytes = inp[0:3].encode('utf-8')
    myint = int.from_bytes(mybytes, 'little')
    currentTime = int(time.time())
    return (myint + currentTime)

# Create a dict with info on a transaction
def save_transaction(sender, receiver, amount):
    id = create_id(sender)
    transactions_db[id] = {
        "timestamp": int(time.time()),
        "id": id,
        "from": sender,
        "to": receiver,
        "amount": amount
    }

def generate_readable_timestamp():
    current_datetime = datetime.now()
    return current_datetime.strftime("%H:%M on %m/%d/%y")


# Client request handler definitions
@client.request
def balance():
    requester = client.get_requester()
    user = fix_name(requester)
    try:
        get_balance(user)
        balance = get_balance(user)
    except KeyError:
        set_balance(user, 100.0)

    balance = get_balance(user)
    print(f"Returning {user}'s balance of {balance}")

    try:
        notifs_list = list(notifications_db[user])
    except KeyError:
        notifs_list = []
    notifications_db[user] = notifs_list

    return balance

@client.request
def get_preferences():
    requester = fix_name(client.get_requester())
    return [preferences_db[requester][i] for i in preferences_db[requester]]

@client.request
def set_preferences(theme, mute):
    preferences_db[fix_name(client.get_requester())] = {
        "theme": theme,
        "mute": mute
    }
    return "updated preferences"

@client.request
def give(amount, user):
    amount = float(amount)
    user = fix_name(user)
    sender = fix_name(client.get_requester())
    print(f"gift - subtracted {amount} from {sender} and gave to {user}")

    notif_timestamp = generate_readable_timestamp()

    try:
        notifs_list = list(notifications_db[user])
    except Exception:
        notifs_list = []
    notifs_list.append(f"{notif_timestamp} - {sender} gave you {amount} bits!")
    notifications_db[user] = notifs_list

    try:
        notifs_list = list(notifications_db[sender])
    except Exception:
        notifs_list = []
    notifs_list.append(f"{notif_timestamp} - You gave {amount} bits to {user}!")
    notifications_db[sender] = notifs_list

    try:
        get_balance(user)
    except KeyError:
        set_balance(user, 100.0)

    if get_balance(sender) >= amount and amount > 0:
        set_balance(sender, get_balance(sender) - amount)
        set_balance(user, get_balance(user) + amount)

    save_transaction(sender, user, amount)

    return get_balance(sender)

@client.request
def search(user):
    user = fix_name(user)
    if get_balance(user):
        message = f"{user} has {get_balance(user)} bits!"
    else:
        message = f"{user}'s balance couldn't be found. Did you spell it right?"

    return message

@client.request
def leaderboard():
    return create_leaderboard()

@client.request
def notifications():
    requester = fix_name(client.get_requester())
    if str(notifications_db[requester]) == '[]':
        return "No notifications!"
    try:
        notifs = notifications_db[requester]
        return notifs
    except KeyError:
        notifications_db[requester] = []
        return "No notifications!"
    
@client.request
def change_balance(user, amount):
    requester = fix_name(client.get_requester())
    if requester in admins_list:
        set_balance(user, amount)
        print(f"Admin '{requester}' set balance of {user} to {amount}")
        return "success!"
    else:
        print(f"Unauthorised user '{requester}' tried to change the balance of {user} to {amount}")
        return "only admins are authorised to change balances"

# Event handling
@client.event
def on_ready():
    print("Request handler is running")

client.start(thread=True)
