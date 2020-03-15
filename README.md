# TotahBot

    $ pip3 install python-telegram-bot --upgrade
    $ export BOT_TOKEN=<BotToken>
    $ python3 totahbot.py
    To run with autourestarting watchdog:
    $ python3 watchdog.py totahbot.py .botupdate
    
For Bot commands to work, the following conditions must be met:
1. The group must be a supergroup which means that **at least one** the following conditions must be met:
   - Changing group type to public
   - Changing group chat history visibility
   - Restricting a group member
   - Changing default administrators permissions
   - Number of group members exceeded 196
2. The Bot must be an admin in the group
3. */setprivacy* must be disabled for the Bot with the help of BotFather
4. The Bot must be promoted to have "Ban Users" permissions in the group   
