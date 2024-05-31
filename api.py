from flask import Flask, jsonify, abort, render_template
from local_simple_database import LocalDictDatabase

# Setup database
LDD = LocalDictDatabase(str_path_database_dir=".", default_value=None)

db = LDD["dict_balances"]
notifications_db = LDD["dict_notifcations"]
transactions_db = LDD["dict_transactions"]

# Flask stuff
app = Flask(__name__)

# Main route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/balance/<username>')
def balance(username):
    try:
        balance = db[username]
        return jsonify({'success': True, 'username': username, 'balance': balance})
    except KeyError:
        return jsonify({'success': False, 'message': 'User not found'})

if __name__ == '__main__':
    app.run()