# Telegram NASA API bot
This program allows you to display photos from NASA's API

### How to install
Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### How to use this program?
First of all, you need to take a token from NASA on their website https://api.nasa.gov/ then, when you have a token, create a file called ```.env``` in the project folder and write this ```API_NASA=*your token*``` after that in telegram find the @BotFather bot and write to it /newbot then fill in what the bot asks for and it will give you a token, then in our ```.env``` file we write this ```TOKEN_TELEGRAM=*your token*```. In order for the bot to know where to write, we need the chat ID, in the ``` .env``` file we enter the ```CHAT_ID=*your_chat_id*``` and, having found *@username_to_id_bot* in the bot's telegram, we write the link of our chat to him, and enter what he gave in ```CHAT_ID=*your_chat_id*```. For one of the code functions, you need to specify the SpaceX launch number, to do this, in the ``` .env``` file, write ```LAUNCH_NUMBER=*launch_number*``` 

After setting up the bot, you must create a chat and add your bot there as an administrator, now you can write your own time for sending breaks, for this, write ```TIME_CODE=*time in seconds*``` in your ```.env``` file.

### How to run
To run the program itself, you need to write the following command on the command line:
```
python main.py
```
