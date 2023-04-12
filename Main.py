# Imports
import scratchattach as scratch3
from scratchattach import Encoding
from local_simple_database import LocalDictDatabase
import time
import os
import threading
import math

def api():
    os.system("python API.py")


t = threading.Thread(target=api, args=())
t.start()

# Initialize DBs
LDD = LocalDictDatabase(
    str_path_database_dir=".",
    default_value=None,
)

db = LDD["dict_balances"]
transactions = LDD['dict_transactions']


def actions():
    total = 0
    for i in db.get_value():
        # total += db[i]
        '''if db[i] > 1000:
            print('a lot: ' + i + ' // ' + str(db[i]))'''
        db[i] = float(math.ceil(db[i]))
    print(total)


'''t2 = threading.Thread(target=actions(), args=())
t2.start()'''


# Connect to Scratch
session = scratch3.Session(os.environ["SESSION"], username="yippymishy")
conn = session.connect_cloud(project_id="669020072")
events = scratch3.CloudEvents("669020072")


# Definitions
# Fix name
def fixName(inp):
    return inp.replace(" ", "").replace("@", "").lower()


def createID(inp):
    mybytes = 'yippymishy'[0:3].encode('utf-8')
    myint = int.from_bytes(mybytes, 'little')
    currentTime = int(time.time())
    return (myint + currentTime)


def leaderboard(amount, offset):
    info = db.get_value()
    info = {key: val for key, val in sorted(info.items(), key = lambda ele: ele[1], reverse=True)}
    res = dict(list(info.items())[offset: offset+amount])
    return res


def sendTop():
    top = leaderboard(5, 0)
    top = [f"{i}#{round(top[i])}" for i in top]
    top = str(top)
    top = top.replace("['", "").replace("', '", "&").replace("']", "")
    print(top)
    print(len(Encoding.encode(top)))
    return top

# The cloud var's name (has zero width space at the end)
varName = "cloud​"

# On_set event


@events.event
def on_set(event):
    # Get timestamp for logs, and initialize log
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    workingInt = str(event.value).replace('-', '').replace('.', '')
    if len(workingInt) == 0:
        workingInt = 0
    logFile = open("log.txt", "a")
    logFile.write(
        f"{timestamp} || @{event.user} set the variable '{event.var}' to {event.value} [{Encoding.decode(event.value)}]\n")
    logFile.close()
    log = ""
    # If it wasn't the bot account
    if True:
        # Decode the var
        cloud = Encoding.decode(int(workingInt))
        # If the user is requesting their balance, return it from the db
        if cloud == 'bal':
            try:
                bal = db[event.user.lower()]
            except KeyError:
                db[event.user.lower()] = 100.0
                bal = db[event.user.lower()]
            conn.set_var(varName, Encoding.encode(f'{event.user}${str(bal)}'))
            log = f"Returned @{event.user}'s balance of {str(bal)}"
        # If it's something else (an admin request or a gift request)
        elif cloud == 'board':
            conn.set_var(varName, Encoding.encode(sendTop()))

        else:
            # Parse it because all requests except "bal" have args
            c = cloud.split('&')
            # If it's a gift request
            if c[0] == 'give' and len(c) == 3:
                # If a user is trying to hack the system by sending gift using API with a Scratch account that
                # doesn't have an account in BlockBit, make one to prevent
                # crashes.
                try:
                    randomVariable = db[event.user.lower()]
                except KeyError:
                    db[event.user.lower()] = 100.0
                # Verify the amount is allowed (not more than their balance)
                rec = fixName(c[1])
                try:
                    if float(c[2]) <= db[event.user.lower()] and float(
                            c[2]) > 0:
                        # Subtract the gift amount from the user's balance
                        db[event.user.lower(
                        )] = db[event.user.lower()] - float(c[2])
                        # Give the giftee the gift amount, creating a new
                        # account for them if necessary
                        try:
                            db[rec] = db[rec] + float(c[2])
                        except KeyError:
                            db[rec] = 100.0
                            db[rec] = db[rec] + float(c[2])
                    giftID = createID(event.user)
                    giftInfo = {"timestamp": int(time.time()), "id": giftID, "from": event.user, "to": rec, "amount": float(c[2])}

                    conn.set_var(varName, Encoding.encode(
                            f'notif${rec}${float(c[2])}${fixName(event.user)}${giftID}'))
                    log = f"{event.user} gave {str(float(c[2]))} bits to {rec}"
                    transactions[giftID] = giftInfo
                except ValueError or IndexError:
                    try:
                        bal = db[event.user.lower()]
                    except KeyError:
                        db[event.user.lower()] = 100.0
                        bal = db[event.user.lower()]
                    conn.set_var(varName, Encoding.encode(
                        f'notif${rec}${float(c[2])}${fixName(event.user)}${giftID}'))
                    transactions[giftID] = giftInfo
                    log = f"Gift request invalid - returned @{event.user}'s balance of {str(bal)}"
            if c[0] == 'see':
                try:
                    seeName = fixName(c[1])
                except BaseException:
                    c.append(fixName(event.user))
                    seeName = fixName(c[1])
                try:
                    conn.set_var('admin',
                                 Encoding.encode(f'seebal${db[seeName]}'))
                except KeyError:
                    db[seeName] = 100.0
                    conn.set_var('admin',
                                 Encoding.encode(f'seebal${db[seeName]}'))
                print(f"ADMIN - got {c[1]}'s balance of {db[seeName]}")

    if not log == "":
        print(f"{timestamp} - {log}")


# On_ready event
@events.event
def on_ready():
    print("Event listener ready!")


# Start events
events.start()
