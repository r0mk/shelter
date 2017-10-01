from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import TelegramClient
import re
import time
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputChannel
from time import sleep

#Where get varibles. Step by step manual https://github.com/LonamiWebs/Telethon/wiki/Creating-a-Client
#Need to create app at https://my.telegram.org/
api_id = 
api_hash = ''
phone_number = ''
client = TelegramClient('Telephone', api_id, api_hash)

if client.connect(): print('Connected')
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    myself = client.sign_in(phone_number, input('Enter code: '))

client.updates.polling = True

offset = 0
limit = 100
all_participants = []
#can be only parsed from API output
#This example for @icocountdown
channel = InputChannel(channel_id = 1076428128, access_hash = -7996179277697111727)

while True:
        participants = client.invoke(GetParticipantsRequest(channel, ChannelParticipantsSearch(''), offset, limit))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        time.sleep(1)  # This line seems to be optional, no guarantees!
        for user in all_participants:
            user_id = re.search('(id: \S*),.*',str(user))
            first_name = re.search('(first_name: \S*),.*',str(user))
            last_name = re.search('(last_name: \S*),.*',str(user))
            username = re.search('(username: \S*),.*',str(user))
            if first_name:
                first_name = first_name.group(1)
            else:
                first_name = 'None'
            if last_name:
                last_name = last_name.group(1)
            else:
                last_name = 'None' 
            if username:
                username = username.group(1)
            else:
                username = 'None'
            if user_id:
                with open('workfile', 'a') as f: f.write(str(user_id.group(1)) + ' ; ' + str(first_name) + ' ; ' + str(last_name) + ' ; ' +  str(username) + '\n')
                print(str(user_id.group(1)) + ' ; ' + str(first_name) + ' ; ' + str(last_name) + ' ; ' +  str(username))
            else:
                print('none')
#for every in all_participants:
#    print(every)
