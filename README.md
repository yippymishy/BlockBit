# BlockBit
All the server and API code for [BlockBit](https://scratch.mit.edu/projects/669020072/), a currency on Scratch!

# API Docs ([blockbit.yippymishy.com](https://blockbit.yippymishy.com))
**/balance/\<user>** - returns the specified user's balance [[Example](https://blockbit.yippymishy.com/balance/yippymishy)]

# Files
**main.py** - Creates a thread for the API and a thread for the server.\
**server.py** - All of the main server code is in this file. It handles transactions, saving and returning peoples' balances, and anything else related to the Scratch project. There are a decent number of comments there to help you understand it.\
**api.py** - All of the code for the API (a Flask app) is here.

### templates
**index.html** - The main page of the API

### secrets
**session_id.txt** - Put your Scratch session ID here

# Changelog (used to be on Scratch but got too long)
4/17/25 - 5.3 - it’s back after months of cloud variables not working! Updated server code to use scratchattach 2.0. Also reset everybody's bits because it all got deleted somehow - but that's just a minor change :P

11/5/24 - 5.2 - added a /transactions route to the API, so you can see any user's transaction history.

6/29/24 - 5.1 - fixed an exploit that allowed you to get infinite bits.

6/6/24 - 5.0.1 - Fixed some bugs.

5/15/24 - 5.0 - Huge update! Remade the entire project from scratch (no pun intended), which allowed for lots of cool new features like notifications/transaction history!

1/19/24 - 4.5.6 - Cloud vars are back, so no more verification codes! Basically just back to how it was before 4.6, so the version is named accordingly.

1/15/24 - 4.6 - Added comment verification to prevent exploits, so now you'll have to comment a 6-digit verification code (given to you by the project) to give bits to a user, and the comment will be automatically deleted. Also added some admin features.

12/13/23 - 4.5.5 - Added a new winter theme and snow!

12/12/23 - 4.5.4 - Finally fixed after being down for a couple months!

9/12/23 - 4.5.3 - Added cool new purple theme by @jokeyguy!

6/8/23 - 4.5.2 - Made the server auto-restart every hour, hopefully this will stop people from losing bits.

5/10/23 - 4.5.1 - Fixed some lag issues and made it so your balance is rounded by default (so no more annoying people giving 0.001 bits). (suggested by @Helm-)

4/13/23 - 4.5 - Added search button and leaderboard button! The search button lets you see another user's balance, and the leaderboard button shows the 5 users with the most bits.

4/8/23 - Back to 4.4.1 - Changed it back to normal (also fixed a bug with the API but nobody really cares)

4/1/23 - April Fools 5.0 - Changed it to BIT and made it incredibly oversimplified!

2/7/23 - 4.4.1 - Added transaction IDs, you'll be able to look them up in the new API when it's finished.

2/1/23 - 4.4 - Added notifications and the Energy theme.

1/28/23 - 4.3.2 - Admins can now see other users' balances using the sidebar (nothing else works). I also added music.

1/25/23 - 4.3.1 - Fixed a bug in the server that was causing crashes when people try to hack the project.

1/20/23 - 4.3 - Added themes and redesign by @Scratch_173035.

12/21/22 - 4.2 - Fixed the problem that was keeping the server (my laptop) from staying online - no longer reverted to 2.5.

8/7/22 - 4.0 - Rewrote the ENTIRE Python server for minimal downtime and quicker response. Also changed the loading screen.

6/12/22 - 3.1 - Added screen that appears when the server is down.

6/6/22 - 3.0 - Reshared for Cloud update, goodbye save codes (and exploits)!

5/23/22 - 2.5 - Sped it up a ton and reworked some internal stuff.

5/17/22 - 2.4 - Added animations by @YandeMC.

5/16/22 - 2.3.5 - Now works again (I think) - merged @seanqint's remix into this project, it was from before this broke.

5/11/22 - 2.3 - Fixed several bugs found by @FunStudioGames and added some clearer instructions in the project.

5/10/22 - 2.2.5 - Bugfix, now works again.

5/8/22 - 2.2 - You no longer need to have your account activated manually.

5/3/22 - 2.1 - Reshared and added various security features.

4/1/22 - 2.0 - Project Shared.