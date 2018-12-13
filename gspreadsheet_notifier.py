#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
#import time
import datetime
import requests

NOTIFY_INTERVAL = 5 
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = '1VZzVmCfK9nyRGLoAQwlyeTLJaVPRzOmPQ2BU5-rqJKs' #Nails
SAMPLE_RANGE_NAME = 'Sheet!A2:G'

proxies = {
#    'socks': 'http://127.0.0.1:9050',
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
    }


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    #print(sheet[u'values'])
    #result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    #print(sheet)
    date_to_check = datetime.date.today() - datetime.timedelta(days=NOTIFY_INTERVAL)
    message = ''
    for clients in sheet[u'values']:
        try:
            last_visit_day_notify = datetime.datetime.strptime(clients[2], '%d.%m.%Y')
        except:
            print("Also, wrong date format " + clients[2] + " for " + clients[0] + '\n')
            message = message + "Also, wrong date format '" + clients[2] + "' for " + clients[0] + '\n'
            continue 
        if date_to_check.day == last_visit_day_notify.day:
            print('Its time to call ' + clients[0] + ' ' + clients[5] + '. Last visit was ' + clients[2] + '\n')
            message = message + 'Its time to call ' + clients[0] + ' ' + clients[5] + '. Last visit was ' + clients[2] + '\n'
    TOKEN = '347895109:AAGb4ylwivdHJr6SYkAX6JLLxC8Drpkz3wo'
    chatid = 213833037
    url = "https://api.telegram.org/bot"
    message_data = {
    'chat_id': chatid, 
    'text': message, 
    'parse_mode': 'HTML', 
    'disable_notification': ''
    }
    resp = requests.post(url + TOKEN + '/sendMessage', data=message_data, proxies=proxies) 
    # print (resp.json())
    if not resp.status_code == 200: 
        return False
    if resp.json()['ok'] == 'false': 
        send_message(myid, 'Чет не отправляется сообщение. Смотри что отвечает: \n' + '<code>' + str(resp.json()) + '</code>\n' + 'А вот что хотел отправить: \n' + '<code>' + str(message_data) + '</code>')

    #values = result.get('values', [])

    #sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    #print(sheet_metadata.get(spreadsheetId=SAMPLE_SPREADSHEET_ID))
    #print(dir(sheet_metadata.sheets()))
    #sheets = sheet_metadata.get('sheets', '')
    #print(sheets)
    #title = sheets[0].get("properties", {}).get("title", "Sheet1")
    #print(title)
    #sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
if __name__ == '__main__':
    main()
