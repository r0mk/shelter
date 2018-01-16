# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,  CallbackQueryHandler
#
#set token
#
updater = Updater(token='')
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
import time
from datetime import date
from pyzabbix import ZabbixAPI
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
z = ZabbixAPI('http://127.0.0.1/zabbix', user='Admin', password='password')

def last_issue(bot, update):
    z = ZabbixAPI('http://127.0.0.1/zabbix', user='Admin', password='password')
    hosts = z.trigger.get(only_true=1,
        skipDependent=1,
        monitored=1,
        active=1,
        filter={'value':1},
        output='extend',
        expandDescription=1,
        selectHosts=['host'],
        limit=10,
        sortfield = 'lastchange',
        sortorder = 'DESC')

    reply = 'Last 10 unsolved issues:\n\n' 
    for host in hosts:
        name = (host['hosts'])
        #reply.append(dict(name[0])['host'] + " " + host['description'] + "\n")
        #reply.append(host['description'] + "\n")
        reply=reply + ''.join(host['description'] + "\n\n")
    bot.sendMessage(chat_id=update.message.chat_id, text=reply)


def active_hosts(bot, update):
    z = ZabbixAPI('http://127.0.0.1/zabbix', user='Admin', password='password')
    hosts = z.host.get(
        filter={'value':1},
        output='extend',
        monitored_hosts=1,
        expandDescription=1,
        limit=100,
        sortorder = 'DESC')

    reply = 'Monitored:\n\n'
    for host in hosts:
        name = (host['host'])
        items = z.item.get(
        filter={'value':1},
        output='extend',
        hostids=host['hostid'],
        expandDescription=1,
        search={'key_': 'system.cpu.util[,idle]'},
        limit=100,
        sortorder = 'DESC')
        cpu_load = str(round(float(100 - float(items[0]['lastvalue'])),2))
        #reply.append(dict(name[0])['host'] + " " + host['description'] + "\n")
        #reply.append(host['description'] + "\n")
        if host['available'] == str(1):
            reply=reply + 'CPU load: ' + ''.join(cpu_load) + '  ' +''.join(host['name']) + ' status UP ' + "\n\n"
        else:
            reply=reply + ''.join(host['name']) + ' status not available' + "\n\n"
    bot.sendMessage(chat_id=update.message.chat_id, text=reply)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="/last_issue - last 10 acitive issues\n /active_hosts - Monitored hots")

def help(bot, update):
    update.message.reply_text("/last_issue - last 10 acitive issues\n /active_hosts - Monitored hots")


last_issue_handler = CommandHandler('last_issue', last_issue)
dispatcher.add_handler(last_issue_handler)

active_hosts_handler = CommandHandler('active_hosts', active_hosts)
dispatcher.add_handler(active_hosts_handler)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

updater.start_polling()

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command. Use /help")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

