# BlockBit
All the server and API code for [BlockBit](https://scratch.mit.edu/projects/669020072/), a currency on Scratch (created by me)!

# Files
**main.py** - Creates a thread for the API and a thread for the server.\
**server.py** - All of the main server code is in this file. It handles transactions, saving and returning peoples' balances, and anything else related to the Scratch project. There are a decent number of comments there to help you understand it.\
**api.py** - All of the code for the API (a Flask app) is here.
**admins.txt** - A list of all the admins, users who have extra permissions (one username per line)

### templates
**index.html** - The main page of the API

### secrets
**session_id.txt** - Put your Scratch session ID here

# API Docs
**/balance/\<user>** - returns the specified user's balance [[Example](https://blockbit.yippymishy.com/balance/yippymishy)]

**/query/\<user>** - returns transactions where user received or sent bits [[Example](https://blockbit.yippymishy.com/query/yippymishy)]
