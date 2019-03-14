#!/usr/bin/python3
#
#Install:
#pip3 install ipapi psycopg2 configparser psycopg2-binary
#
#PSQL:
#create database isp_detect;
#create table ips(ip SERIAL PRIMARY KEY, org text, region text, country text, country_name text, city text, asn text);
#create user detector with password 'YaeY1ut0no'
# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO detector;

import os
import re
import ipapi
import psycopg2
import datetime
import time
from collections import Counter
from configparser import ConfigParser

filename="/home/r0mk/shelter/access.log"

def config(filename='database.ini', section='isp_detect'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_ip_from_log(filename):
    """Method 1: read whole file and regex"""
    regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*'
    with open(filename, 'r') as f:
        txt = f.read()
    match = re.findall(regex, txt)
    #match = list(dict.fromkeys(match))
    match =  Counter(match)
    return match

def insert_to_db(ip_list):
    sql = """INSERT INTO ips(ip, hit_count) VALUES (%s, %s) RETURNING ip;"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        for ip in ip_list.keys():
            cur.execute(sql,(ip,ip_list[ip]))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

ip_list = get_ip_from_log(filename)

insert_to_db(ip_list)

def get_empty_ip():
    sql = """SELECT ip FROM ips WHERE org IS NULL;"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        empty_ip = cur.fetchall()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return empty_ip
  
empty_ip = get_empty_ip()
print(empty_ip)

def fill_database(empty_ip):
    timer = datetime.datetime.timestamp(datetime.datetime.now())
    counter = 0
    for ip in empty_ip:
        if counter < 149:
            print("less then minute")
            print("ip: " + ip[0])
            data = ipapi.location(ip[0]) 
            counter = counter + 1
            print(data)
        else:
            print("limit reached")
            time.sleep(timer - datetime.datetime.timestamp(datetime.datetime.now()) + 60)
            timer = datetime.datetime.timestamp(datetime.datetime.now())
            counter = 0

fill_database(empty_ip)



