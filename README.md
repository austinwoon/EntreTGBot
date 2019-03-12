# EntreTGBot
Telegram Bot made for an entrepreneurship module for market validation of functionalities. Time spent programming this bot was a total of 2 days (20 hours).

Key Functionalities included are:
1) For tertiary students to ask questions regarding overseas exchange on the bot
2) (Admin Action) For students living overseas/have gone exchange overseas before to answer the queries above
3) (Admin Action) For students to blast messages to everyone subscribed to this bot service


The final deployed bots(Deployed with Heroku) are: 
@Traverse_Australia_Bot
@Traverse_Canada_Bot
@Traverse_Korea_Bot

# APIs Used

### Telegram API
To use the Telegram API, I imported an external library (API Wrapper) called pyTelegramBotAPI

Link to wrapper here: https://github.com/eternnoir/pyTelegramBotAPI

### Google Spreadsheet API

In addition, I also needed to use Google's Spreadsheet API which can be found on Google Cloud Platform.

The rationale for using the Spreadsheets API was so that admin users could access the spreadsheet and see what questions they had to answer at their convinience. 

At the time of programming the Bot, I found this way the easiest for consolidating of information as my administrative users were not tech-savvy but were comfortable with Google Spreadsheets. 

__Example of how admins would see information (questions) published by users__
![Imgur](https://i.imgur.com/ZX2BCMB.png "Imgur")

I used the spreadsheet API to mimic a database for users instead of a database schema in Heroku due to time constraints (I had to get this Bot running in two days time)

Here is a picture of a sample "database" for my users I used in the spreadsheet:

![ss_user](https://i.imgur.com/qmRz8JN.png?2 "ss_user")  

## In-depth view of functionalities 

### Basic Overview of Application Architecture (Not accurate for all use-cases, did one generic scenario for better understanding of how program works)

![diagram](https://i.imgur.com/pT2XHmt.png "diagram")

### Function 1: Registering for service

Upon typing the "/start" command, users will be prompted to type their email for registration purposes.

Then, the Telegram Bot will access the Google Sheets API and enter the email and the unique chat id of the message into the users spreadsheet database.

### Function 2: Asking Questions

Upon typing the "/ask_qn" command, users will be prompted to ask a question.

The Telegram Bot will then access the Google Sheets API and insert the datetime, question contents, chat_id and first name of the users

### Function 3: Replying Questions (Admin Action)
Keying in /ambas_action will prompt a markdown menu with two options, to send a message to an individual user or to blast message.

Admins can reply questions by keying in the chat_id of the students they wish to reply 

The chat_id will be crossed checked with the spreadsheet's user worksheet. If the user exists, the message contents will be delivered.

### Function 4: Blasting Message

Admins can blast a message to everyone subscribed to the service. 

After keying in message contents, the bot will access the google sheets and loop through the user_ids to send a message to each and every user ID.

### Function 5: Unsubscribing From Service

Users can unsubscribe from bot with the /unsubscribe command. 

The sheets api will remove the user_id by index.

### Function 6: Error Logging

I needed an easyway to know whether errors were happening in the Bot.

To prevent any error from crashing the whole application, I used try except method in every function of the bot. 

In my exception, I used an error logging method from the gspread library which would log an error into the spreadsheet "Errors Log" with the following details: __Datetime Error Occured, Function that failed, Bot that failed__

This enables me to easily check for errors in individual functions of a bot whenever I access the spreadsheet.

# Review

### Things I could have done differently:

1. Instead of using the Spreadsheets API to store users, I could use a database schema for each bot on my heroku app. 

2. Do not use the Wrapper to program my telegram bot and instead call the API directly. Initially, I did call the API directly but found it too tedious to do so in the span of two days. In the future, I will implement my own Telegram Bot class to ensure cleaner and more readable code. This will also give me the flexibility of implementing my own functions instead of relying purely on the Wrapper's Methods.

3. Use Asynchronus Messaging for notifications (for e.g "Succesfully Sent!") such that bot does not need to wait for previous update to be completed before serving other commands. This can help speed up application processes.
