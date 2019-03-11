import telebot 
from telebot import types
from config import australia_api_key, ssid
import datetime
import csv
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request
import os

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('SSID Project-4f65cc1e7dfe.json', scope)
gc = gspread.authorize(credentials)

ss = gc.open_by_key(ssid)
wks = ss.get_worksheet(4)
users = ss.get_worksheet(5)
server = Flask(__name__)
bot = telebot.TeleBot(token=australia_api_key)

error_sheet = ss.get_worksheet(6)
bot_region = "Australia"

TOKEN = australia_api_key

#What users see on start command
@bot.message_handler(commands=['start'])
def register(message):
    try: 
        msg = bot.reply_to(message, "Hello! Please enter your email address below:")
        chat_id = msg.chat.id
        print(users.col_values(2))
        if str(chat_id) not in set(users.col_values(2)[1:]):
            bot.register_next_step_handler(msg, insert_into_db)
        else:
            bot.reply_to(message, "You have already registered for this bot! Type /ask_qn now to ask a question regarding exchange. \n For extra help, please type /help")
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start command has failed!", bot_region])

def insert_into_db(message):
    try: 
        chat_id = message.chat.id
        user_id = message.text

        if '@' in user_id in user_id and len(user_id) > 6:
            users.append_row([user_id,chat_id])
            bot.reply_to(message, "You have succesfully registered for this service! Type /ask_qn now to ask a question regarding exchange. \n For extra help, please type /help")
        else:
            bot.reply_to(message, "You have entered an invalid email, please type /start to register again!")
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Start command has failed!", bot_region])
#Help command
@bot.message_handler(commands=['help'])
def help_msg(message):
    try:
        msg = bot.reply_to(message, "1) /ask_qn to ask a question regarding exchange on telegram \n2) Contact our Bot Admins on Telegram at: @Austinwqy @LucasEthanTiong @ZiaZiaa @sammmfoo for more info! \n3) Type /unsubscribe to unsubscribe from this service! ")
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Help command has failed!", bot_region])                          


#list of ambassadors actions allowed
@bot.message_handler(commands=['ambas_action'])
def markup_menu(message):
    try: 
        markup = types.ReplyKeyboardMarkup()
        global options
        options = {
            'option_1' : 'Reply Individual User',
            'option_2' : 'Blast Message to all Users'
        }
        markup.row(options['option_1'], options['option_2'])
        msg = bot.reply_to(message, "Choose one option:", reply_markup=markup)
        bot.register_next_step_handler(msg, admin_options)
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   

def admin_options(message):
    try: 
        #option_1 is to reply to user
        if message.text == options['option_1']:
            msg = bot.reply_to(message, "Hi! Please enter the user_id of the user you'd like to reply to", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, reply_question)

        #option_2 is to mass send a message
        if message.text == options['option_2']:
            msg = bot.reply_to(message, "Enter Message to blast to all users", reply_markup = types.ReplyKeyboardRemove())
            bot.register_next_step_handler(msg, confirmation)
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   

#Option_1: Reply User
def reply_question(message):
    try: 
        global reply_user_id
        reply_user_id = message.text

        if reply_user_id not in set(users.col_values(2)[1:]):
            bot.reply_to(message, "You have entered an invalid user! Please type /ambas_action try again")

        else:
            msg = bot.reply_to(message, "Please enter the contents of your message:")
            bot.register_next_step_handler(msg, reply_contents)
    
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   

def reply_contents(message):
    try: 
        reply = message.text
        bot.send_message(reply_user_id,reply, parse_mode = 'Markdown')
        bot.reply_to(message, "Message succesfully sent!")
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   

#Option_2: Blast message to everyone
def confirmation(message):
    try: 
        blast_markup = types.ReplyKeyboardMarkup()
        blast_markup.row("Yes", "No")
        global blast_contents 
        blast_contents = message.text
        msg = bot.reply_to(message, "Are you sure you want to send this message to everyone? \n\n Message Contents:\n" + blast_contents, reply_markup=blast_markup)
        bot.register_next_step_handler(msg, blast_message)
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   

def blast_message(message):
    try: 
        confirmation = message.text
        if confirmation.lower() == "yes":
            bot.reply_to(message, "Succesfully sent to everyone! \n\nMessage Contents:\n" + blast_contents,reply_markup = types.ReplyKeyboardRemove())
            for chat_id in set(users.col_values(2)[1:]):
                bot.send_message(chat_id, blast_contents, parse_mode = 'Markdown')
        else: 
            bot.reply_to(message, "Please type /ambas_action to try blasting again" ,reply_markup = types.ReplyKeyboardRemove())
            
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ambas_action command has failed!", bot_region])   



#for normal users to ask question
@bot.message_handler(commands=['ask_qn'])
def reply_qn(message):
    try: 
        msg = bot.reply_to(message, "Hi! Please enter the question you'd like to ask regarding exchange")
        bot.register_next_step_handler(msg, enter_to_ss)
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ask_Qn command has failed!!", bot_region])   

def enter_to_ss(message):
    try: 
        qn = message.text
        if (len(qn)<10):
            bot.reply_to(message, "Invalid message! Please type /ask_qn and try again.")
        else:
            wks.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message.chat.id, message.chat.username, qn, message.chat.first_name])
            bot.reply_to(message, "Thank you for your question, our ambassador will get back to you asap!")
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ask_Qn command has failed!!", bot_region])   



#deregister for service
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    try:
        msg = bot.reply_to(message, "Are you sure you want to unsubscribe from this service? (Please type 'Yes' or 'No')")
        bot.register_next_step_handler(msg, unsub_confirm)
    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "unsub command has failed!!", bot_region])

def unsub_confirm(message):
    try:
        user_list = users.col_values(2)
        chat_id = str(message.chat.id)
        if chat_id not in user_list:
            bot.reply_to(message, "You are not in our subscription list! Please enter /start to subscribe if you'd like to join us")
            return
        index = user_list.index(str(chat_id))
        if message.text.lower() == "yes":
            users.delete_row(index+1)
            bot.reply_to(message, "Officially unsubscribed! Thank you for using our service. We wish you all the best for your exchange!")
        else: 
            bot.reply_to(message, "Thank you for not unsubscribing for our service, we hope to serve you to the best of our abilities")

    except Exception as e:
        print("Error has occured")
        error_sheet.append_row([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "unsub command has failed!", bot_region])
        

#server stuff

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://stark-caverns-33411.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

































