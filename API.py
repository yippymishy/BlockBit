from flask import Flask
from local_simple_database import LocalDictDatabase

LDD = LocalDictDatabase(
    str_path_database_dir=".",
    default_value=None,
)

db = LDD["dict_balances"]
transactions = LDD['dict_transactions']

app = Flask(__name__)


@app.route('/')
def home():
    return "This is the BlockBit API :D"


@app.route('/balance/<user>')
def getBalance(user):
    try:
        out = {"balance": db[user]}
    except KeyError:
        out = {"message": "user not found"}
    return out


@app.route('/transaction/<id>')
def getByID(id):
    try:
        out = transactions[id]
    except KeyError:
        out = {}
    return (str(out))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)