#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python3
import feedparser
import time
import urllib


class UpworkRSSfetcher():

    def __init__(self,rss_url = None):
        """
        constructor
        """
        self.rss_url = rss_url
    
    def update_feed(self, current_feed):
        updated_feed = feedparser.parse(self.rss_url )
        current_titles = []
        send_to_database = []
        if updated_feed.status != 200:
            print('response code: ' + str(updated_feed.status))
        for current_entries in current_feed:
            current_titles.append(current_entries['title'])
        for new_items in updated_feed.entries:
            if new_items.title not in current_titles:
                send_to_database.append(new_items)
        print('Received' + str(len(send_to_database)) + ' new jobs')
        for message in send_to_database:
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
        for every in send_to_database:
            current_feed.append(every)
        return current_feed

 
    
