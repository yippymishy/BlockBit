from flask import Flask
from local_simple_database import LocalDictDatabase
import ast

LDD = LocalDictDatabase(
    str_path_database_dir=".",
    default_value=None,
)

db = LDD["dict_balances"]
transactions = LDD['dict_transactions']


def history(inp):
    out = []
    t = str(transactions)
    t = ast.literal_eval(t)
    for i in t:
        if t[i]['from'] == inp or t[i]['to'] == inp:
            out.append({'timestamp': t[i]['timestamp'], 'from': inp, 'to': t[i]['to'], 'amount': t[i]['amount'], 'id': t[i]['id']})
    history = {'history': out}
    return history


app = Flask(__name__)


@app.route('/')
def home():
    return """
    This is the BlockBit API :D<br>
    <b>/balance/[user]</b> returns the specified user's balance.<br>
    <b>/transaction/[id]</b> returns info about the specified transaction.<br>
    <b>/history/[user]</b> returns the specified user's transaction history.
    """


@app.route('/balance/<user>')
def getBalance(user):
    try:
        out = {"balance": db[user.lower()]}
    except KeyError:
        out = {"message": "user not found"}
    return out


@app.route('/transaction/<id>')
def getByID(id):
    try:
        out = transactions[id]
    except KeyError:
        out = {}
    return out


@app.route('/history/<user>')
def getHistory(user):
    return history(user.lower())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)