#!/usr/bin/python3
# -*- coding: utf-8 -*-
from rss_parser import UpworkRSSfetcher

upwork_url= "https://www.upwork.com/ab/feed/topics/rss?securityToken=f95b63738835bc9997ec12f0401d48a82ebfebfc80616ce6bde4c1f3069dacc76c1b023b0fa37a4fe44262caae43bfbf8d35c9a8f60340545eef40dddf551148&userUid=454220209633980416&orgUid=454220209642369025"

upwork_feed = UpworkRSSfetcher(upwork_url)

print(upwork_feed.update_feed([]))
