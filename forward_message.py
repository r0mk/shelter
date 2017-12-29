#!/usr/bin/python3
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.functions.messages import GetChatsRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.users import GetFullUserRequest 
from telethon.tl.types import InputChannel
from telethon.tl.types import InputUser
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerUser
from telethon.tl.types import UpdateNewChannelMessage
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon.utils import get_input_peer
import re
import time
import sys

api_id = 130513
api_hash = 'a5be1e0fb675956ff16e5309d5a2fd49'
phone_number = '+79501744583'
client = TelegramClient('r0mkTelephone', api_id, api_hash,  update_workers=0)
channel_from  = sys.argv[1]
channel_to_send = sys.argv[2]

if client.connect():
    print('Connected')
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    myself = client.sign_in(phone_number, input('Enter code: '))

client.updates.polling = True

channel_manual = client.get_entity('t.me/' + channel_from)
print("Channel to: " + str(channel_manual.title))
print("Channel to ID: " + str(channel_manual.id))
print("Channel to Hash: " + str(channel_manual.access_hash))
channel_from_input_peer = InputPeerChannel(channel_manual.id, channel_manual.access_hash)

channel_to = client.get_entity('t.me/' + channel_to_send)
print("Channel to: " + str(channel_to.title))
print("Channel to ID: " + str(channel_to.id))
print("Channel to Hash: " + str(channel_to.access_hash))
channel_to_input_peer = InputPeerChannel(channel_to.id, channel_to.access_hash)

#try:
#    channel_from_input_peer = client(SearchRequest(q=channel_manual, limit=1))
#except:
#    pass
#    #sys.exit('Channel not found')

#shelter2 = InputPeerChannel(channel_manual.id, channel_manual.access_hash)

#print("Channel from: " + str(channel_from_input_peer.chats[0].title))
#print("Channel from  ID: " + str(channel_from_input_peer.chats[0].id))
#print("Channel from Hash: " + str(channel_from_input_peer.chats[0].access_hash))

#try:
#    channel_to_input_peer = client(SearchRequest(q=channel_to_send, limit=1))
#except:
#    pass
#    sys.exit('Channel not found')

#print("Channel to: " + str(channel_to_input_peer.chats[0].title))
#print("Channel to ID: " + str(channel_to_input_peer.chats[0].id))
#print("Channel to Hash: " + str(channel_to_input_peer.chats[0].access_hash))


#my_channel_from = InputPeerChannel(channel_id=channel_from_input_peer.chats[0].id, access_hash=channel_from_input_peer.chats[0].access_hash)
#my_channel_to = InputPeerChannel(channel_id=channel_to_input_peer.chats[0].id, access_hash=channel_to_input_peer.chats[0].access_hash)
#my_channel_to = InputPeerChannel(channel_id=channel_manual.id, access_hash=channel_manual.access_hash)
#my_channel_from = InputPeerChannel(channel_id=channel_from_input_peer.chats[0].id, access_hash=channel_from_input_peer.chats[0].access_hash)

#total_count, messages, senders = client.get_message_history(shelter2, limit=1)
#for msg in reversed(messages):
#     print ("msg:   ", msg.id, msg)
#     client.invoke(ForwardMessagesRequest(from_peer=shelter2, id=[msg.id], to_peer=shelter2))

while True:
    update = client.updates.poll()
    if type(update) == UpdateNewChannelMessage and update.message.to_id.channel_id == channel_manual.id:
        print('message id ' + str(update.message.id))
        print('channel id ' + str(update.message.to_id.channel_id))
        #print(update)
        #print(dir(update))
        client.invoke(ForwardMessagesRequest(from_peer=channel_from_input_peer, id=[update.message.id], to_peer=channel_to_input_peer))

#    print('UPDATE_MESSAGE')
 
        #print(client.invoke(GetMessagesRequest(channel=my_channel_to, id=[update.message.id])))
        #client.invoke(ForwardMessagesRequest(from_peer=my_channel_from, id=[update.message.id], to_peer=my_channel_to))
    else:
        continue


#def forward(update):
    #if isinstance(update, UpdateShortMessage) and not update.out:
    #total_count, messages, senders = client.get_message_history(channel_from_input_peer.chats[0], limit=1)
#    print('UPDATE_MESSAGE')
#    print(update.message)
#    print('FULL_MESSAGE')
#    print(update)
    #client.invoke(ForwardMessagesRequest(from_peer=my_channel_from, id=[msg.id], to_peer=my_channel_to))


client.add_update_handler(forward)
#input('Press enter to stop this!')
#client.disconnect()
