# Import the necessary modules
import scratchattach as scratch3
from local_simple_database import LocalDictDatabase
import ast
import time
from datetime import datetime
import threading

# Read the session ID from a file for login
with open('secrets/session_id.txt', 'r') as session_id_txt:
    session_id = str(session_id_txt.read())

#read the admins list
with open("admins.txt", "r") as admins_txt:
    admins_list = admins_txt.readlines()
    admins_list = [i.replace("\n","") for i in admins_list]

# Connect to Scratch
project_id = 669020072

session = scratch3.Session(session_id=session_id, username='yippymishyTest')  # Update with your session ID and username
print('Logged in as ' + session.get_linked_user().username)
conn = session.connect_cloud(project_id)  # Update with your project ID
client = scratch3.CloudRequests(conn, used_cloud_vars=["1", "2", "3"])

# Setup database
LDD = LocalDictDatabase(str_path_database_dir=".", default_value=None)

# "db" is the database for balances (dict_balances.txt)
db = LDD["dict_balances"]
notifications_db = LDD["dict_notifcations"]
transactions_db = LDD["dict_transactions"]
preferences_db = LDD["dict_preferences"]

# Set the default values for some databases
LDD["dict_balances"].change_default_value(False)
LDD["dict_notifications"].change_default_value([])
LDD["dict_preferences"].change_default_value(
    {"theme": "blue", "mute": False}
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

#Create a dict with info on a transaction
def save_transaction(sender,receiver,amount):
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

#Admin commands in comments
def check_for_admin_comments():
    project = session.connect_project(project_id)
    comments = project.comments(limit=1, offset=0)
    comment = comments[0]
    commentor = comment['author']['username']
    content = comment['content']
    comment_id = comment['id']

    if commentor in admins_list:
        command = content.split(' ')

        if command[0] == '$set' and len(command) == 3:
            if (not commentor.lower() == str(command[1].lower())) or commentor.lower() == "yippymishy":
                try:
                    set_balance(str(command[1]).lower(), float(command[2]))
                except ValueError:
                    pass
        
            #project.delete_comment(comment_id=comment_id)

def admin_command_loop():
    while True:
        check_for_admin_comments()
        time.sleep(5)

admin_comments_thread = threading.Thread(target=admin_command_loop)
admin_comments_thread.start()

# Client request handler definitions
@client.request
def balance():
    requester = client.get_requester()
    user = fix_name(requester)
    if get_balance(user):
        balance = get_balance(user)
    else:
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
    return [preferences_db[fix_name(client.get_requester())][i] for i in preferences_db[fix_name(client.get_requester())]]

@client.request
def set_preferences(theme, mute):
    preferences_db[fix_name(client.get_requester())] = {
        "theme": theme,
        "mute": mute
    }
    return "updated preferences"

@client.request
def give(amount, user):  # Called when the client receives a request
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

    if get_balance(sender) >= amount and amount > 0:
        set_balance(sender, get_balance(sender) - amount)
        set_balance(user, get_balance(user) + amount)

    save_transaction(sender, user, amount)

    return get_balance(sender)

@client.request
def search(user):
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
    if str(notifications_db[fix_name(client.get_requester())]) == '[]':
        return "No notifications!"
    try:
        notifs = notifications_db[fix_name(client.get_requester())]
        return notifs
    except KeyError:
        notifications_db[fix_name(client.get_requester())] = []
        return "No notifications!"

# Event handling
@client.event
def on_ready():
    print("Request handler is running")

# Start the client
client.run()  # Make sure this is at the bottom of the file