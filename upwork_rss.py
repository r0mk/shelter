#!/usr/bin/python3
import feedparser
import time
import urllib

import socket
import socks 
#import python_postgresql.insert_jobs_list
from python_postgresql import  insert_jobs_list

#pip install feedparser
#pip install pysocks


r = urllib.request.urlopen('http://icanhazip.com')
print(r.read()) # check ips

rss_url = "https://www.upwork.com/ab/feed/topics/rss?securityToken=f95b63738835bc9997ec12f0401d48a82ebfebfc80616ce6bde4c1f3069dacc76c1b023b0fa37a4fe44262caae43bfbf8d35c9a8f60340545eef40dddf551148&userUid=454220209633980416&orgUid=454220209642369025"

send_to_telegram = []
current_feed = [{'title':'value'}]
def update_feed(current_feed):

    updated_feed = feedparser.parse( rss_url )
    current_titles = []
    if updated_feed.status != 200:
        print('response code: ' + str(updated_feed.status))
    for current_entries in current_feed:
        current_titles.append(current_entries['title'])
    for new_items in updated_feed.entries:
        if new_items.title not in current_titles:
            send_to_telegram.append(new_items)
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
        job_list=(message['title'], details, 'add tags')
        insert_jobs_list(job_list)

    for every in send_to_telegram:
        current_feed.append(every)
    return current_feed
    
while True:
    if len(current_feed) > 50:
        to_remove = len(current_feed) - 50
        while to_remove != 0:
            current_feed.pop(to_remove - 1)
            to_remove-=1 
    print('after cleanting:')
    print(len(current_feed))
    current_feed = update_feed(current_feed)
    time.sleep(10)
