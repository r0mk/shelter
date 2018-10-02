#!/usr/bin/python3
# -*- coding: utf-8 -*-
#pip3 install pymongo

from ftplib import FTP
ftp = FTP('78.85.35.103')
ftp.login('ftppasha','9127453050')
ftp.cwd('out')
ftp.dir()
#ftp.retrbinary('RETR ' + 'ProdList.csv', open('/home/r0mk/shelter/ProdList.csv', 'wb').write)
ftp.quit()

from woocommerce import API
import json
wcapi = API(
url="http://theautomd.com/", # Your store URL
consumer_key="ck_a00ad9d6c10d9e8d8a251d5dcc9b5d1887f230c2", # Your consumer key
consumer_secret="cs_489fc080e4232a40ca616ec52341fb6a1467ba64", # Your consumer secret
wp_api=True, # Enable the WP REST API integration
timeout=20,
version="wc/v2" # WooCommerce WP REST API version
)
#print(wcapi.get("").json())
#Retrive one product
#
data = {
        'page': 1,
        'per_page': 1
        }
#
#resp = (wcapi.get("products?per_page=10").headers)
resp = wcapi.get("products?per_page=10")
resp_headers = resp.headers
resp_json = resp.json()
print(type(resp))
print("Total pages " + resp_headers['X-WP-TotalPages'])
print(resp_json[0]['name'])
#for every in resp:
#    print(every['id'])
    #print(every['name'])

from pymongo import MongoClient
client = MongoClient()

db = client.prodlist
insert_result = db.prodlist.insert_one(
        {"products" : {
            "name" : resp_json[0]['name'],
            "id" : resp_json[0]['id']
            }
        }
        )
print(insert_result.inserted_id)


#Retrive all products
#print(wcapi.get("products").json())

