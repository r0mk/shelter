#!/usr/bin/python3
import feedparser
import time
import urllib

#pip install feedparser

#Rss url from upwork
rss_url = ""
#Bot_id from @BotFather
bot_id = ''
#ID from @MyTelegramID_bot
send_to_id = 

current_feed = [{'title':'value'}]
def update_feed(current_feed):
    updated_feed = feedparser.parse( rss_url )
    send_to_telegram = []
    current_titles = []
    if updated_feed.status != 200:
        print(updated_feed.status)
    for current_entries in current_feed:
        current_titles.append(current_entries['title'])
    for new_items in updated_feed.entries:
        if new_items.title not in current_titles:
            send_to_telegram.append(new_items)
    print("TELEGRAM")
    print(len(send_to_telegram)) 
    for message in send_to_telegram:
        details = message['summary_detail']['value']
        details = details.replace('<br />', '')
        details = details.replace('&bull;', '')
        details = details.replace('&nbsp;', '')
        details = details.replace('&amp;', '')
        details = details.replace('&#039;', '')
        details = details.replace('<a href="','\n')
        details = details.replace('">click to apply</a>','')
        details = details.replace('<b>Budget</b>','\n**Budget**')
        details = details.replace('<b>Posted On</b>','\nPosted On')
        details = details.replace('<b>Category</b>','\nCategory')
        details = details.replace('<b>Country</b>','\nCountry')
        details = details.replace('<b>Skills</b>','\nSkills')
        idata = urllib.parse.urlencode({ 'chat_id': send_to_id, 'text': '<b>' + message['title'] + '</b>' + '\n' + details, 'parse_mode': 'HTML', 'disable_web_page_preview': 1})
        idata = idata.encode('ascii')
        #print(message['summary_detail']['value'])
        req = urllib.request.Request('https://api.telegram.org/bot' + bot_id + '/sendMessage' )
        try:
            urllib.request.urlopen(req, idata)
        except:
            pass
    print("TELEGRAM\n")
    for every in send_to_telegram:
        current_feed.append(every)
    return current_feed
    
while True:
    print("current!!!!!")
    print(len(current_feed))
    print("current!!!!!\n")
    if len(current_feed) > 50:
        to_remove = len(current_feed) - 50
        while to_remove != 0:
            current_feed.pop(to_remove - 1)
            to_remove-=1 
    print('after cleanting')
    print(len(current_feed))
    current_feed = update_feed(current_feed)
    time.sleep(10)
