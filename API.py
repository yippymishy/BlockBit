from flask import Flask, render_template
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
            out.append({'timestamp': t[i]['timestamp'], 'from': t[i]['from'], 'to': t[i]['to'], 'amount': t[i]['amount'], 'id': t[i]['id']})
    history = {'history': out}
    return history


app = Flask(__name__)


@app.route('/')
def home():
    return """
    This is the BlockBit API!<br>
    <b>/balance/[user]</b> returns the specified user's balance. [<a href='/balance/yippymishy'>example</a>]<br>
    <b>/transaction/[id]</b> returns info about the specified transaction. [<a href='/transaction/1683315285'>example</a>]<br>
    <b>/history/[user]</b> returns the specified user's transaction history. [<a href='/history/yippymishy'>example</a>]<br><br>
    """


@app.route('/home')
def main():
    stylesheet = open("templates/index.css", "r").read()
    return render_template('index.html', stylesheet=stylesheet)


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