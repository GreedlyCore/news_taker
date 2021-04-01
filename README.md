# news_taker
## based on PyTelegramBotAPI by etnoir
telegram bot for who want to know more

requires mySQL
requires log folder
### Setting up 

To start the setup, you must do the following:

1. **Install all the needed stuff**:</br>
```$ pip install PyTelegramBotAPI --upgrade```</br>
```$ pip install tinydb --upgrade```
2. Open [const.py]
  - Change the value of ```TOKEN``` to the token given for you by [@BotFather](https://telegram.me/botfather)
  - Change the value of ```BOT_ID``` to your own bot ID, without the "@". _NOTE: IF YOU PUT THE "@", THE BOT MIGHT NOT WORK PROPERLY_
  - Change the value of ```BOT_NAME``` to the name you want your bot to have - Yes, you can rename your bot easily with it
  - Change the value of ```MASTER_ID``` to your own chat id.
  
Now you're all set! run ```Bot.py``` !


# Changelog
**V1:**
  Version 1, stable. This bot will be soon upgraded to a new code base, 2.x.

**Beta-7:**
  Version 0.9.x! (Beta 7)
  0.9x is here!

  * Complete change in the API
  * New Server API (Gelbooru)
  * Working inline mode

and much more! See all the changes [here](https://github.com/halkliff/EmaProject/releases/tag/0.9.1-Beta-7)

**Beta-6:**
  * Bug Fixes

**Beta-5:**
  * Fixed some issues and mispellings
  * Added /admin command to know the status
  * Register users in a database
  * Users now have multiple language choices and changeability of it's language in database
  * Inline mode deactivated until the real database is ready
  * Delete DE.py
  * Delete ES.py
  * Delete PT.py
  * Delete RU.py
  * Delete EN.txt

**Beta-4:**
  * Workout in inline mode
  * API now have a function that will search for tags
  * Correction of some mispelling

**Beta-3:**
  * Major changes in the [/API/Img.py](https://github.com/halkliff/EmaProject/blob/Beta-2/API/IMG.py)
  * New strings added for the answers in [/lang/EN.py](https://github.com/halkliff/EmaProject/blob/Beta-2/lang/EN.py)
  * Major changes into [Bot.py](https://github.com/halkliff/EmaProject/blob/Beta-2/Bot.py) to work with the new API

# Future Plans

- [x] Finish up the inline mode (Finally!!!)
- [ ] Update with the final version 1.x.x

