#!/usr/bin/python3
# -*- coding: utf-8 -*-

#pip3 install python-telegram-bot
#pip3 install pymongo

from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from telegram.ext.filters import Filters
from pymongo import MongoClient

client = MongoClient()

db = client.feedbackdb

def hello(bot, update):
        update.message.reply_text(
                'Hello {}'.format(update.message.from_user.first_name))

updater = Updater('415897248:AAHjlBMSrlXmnEaDkdmlCxvjS-Ct6vOzDhE')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

cursor = (db.feedbackdb.find())

print(cursor[1])

def text_message(bot, update):
      bot.sendMessage(chat_id=update.message.chat_id, text="Ваше мнение очень важно для нас")
      print(update.message.date)
      #print(update.message.from_user)
      insert_result = db.feedbackdb.insert_one(
      { 
          "from_user" : {
              "username" : update.message.from_user.username,
              "first_name" : update.message.from_user.first_name,
              "last_name" : update.message.from_user.last_name,
              "id" : update.message.from_user.id},
      "date" : update.message.date,
      "message_text" : update.message.text
      }
      )
      print(insert_result.inserted_id)

updater.dispatcher.add_handler(MessageHandler(Filters.text, text_message))

updater.start_polling()
updater.idle()
