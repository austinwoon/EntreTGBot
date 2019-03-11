# EntreTGBot
Telegram Bot made for an entrepreneurship module for market validation of functionalities.

Key Functionalities included are:
1) For tertiary students to ask questions regarding overseas exchange on the bot
2) (Admin Action) For students living overseas/have gone exchange overseas before to answer the queries above
3) (Admin Action) For students to blast messages to everyone subscribed to this bot service


The final deployed bots(Deployed with Heroku) are 
@Traverse_Australia_Bot
@Traverse_Canada_Bot
@Traverse_Korea_Bot

# APIs Used

## Telegram API
To use the Telegram API, I imported an external library (API Wrapper) called pyTelegramBotAPI

Link to wrapper here: https://github.com/eternnoir/pyTelegramBotAPI

## Google Spreadsheet API

In addition, I also needed to use Google's Spreadsheet API which can be found on Google Cloud Platform.

I used the spreadsheet API as my database for users instead of a database schema in Heroku due to time constraints (I had to get this Bot runnig in one day)

Here is a picture of a sample "database" for my users I used in the spreadsheet:

![SpreadsheetDatabase](https://i.imgur.com/qmRz8JN.png "SpreadsheetDatabase" =200x)

# In-depth view of functionalities 

## Function 1: Registering for service

Upon typing the "/start" command, users will be prompted to type their email for registration purposes.

Then, the Telegram Bot will access the Google Sheets API and enter the email and the unique chat id of the message

## Function 2: Asking Questions

Upon typing the "/ask_qn" command, users will be prompted to ask a question.

The Telegram Bot will then access the Google Sheets API and insert the datetime, question contents, chat_id and first name of the users

## Function 3: Replying Questions (Admin Action)
Keying in /ambas_action will prompt a markdown menu with two options, to send a message to an individual user or to blast message.

Admins can reply questions by keying in the chat_id of the students they wish to reply 

The chat_id will be crossed checked with the spreadsheet's user worksheet. If the user exists, the message contents will be delivered.

## Function 4: Blasting Message

Admins can blast a message to everyone subscribed to the service. 

After keying in message contents, the bot will access the google sheets and loop through the user_ids to send a message to each and every user ID.








