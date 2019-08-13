#!/usr/bin/python3
#
#Install:
#pip3 install ipapi psycopg2 configparser psycopg2-binary
#
#PSQL:
#create database isp_detect;
#create table ips(ip text PRIMARY KEY, hit_count int, received int,  org text, region text, country text, country_name text, city text, asn text, log_date DATE NOT NULL DEFAULT CURRENT_DATE);
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

filename="/home/r0mk/Downloads/error.log"

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
    #sql = """INSERT INTO ips(ip, hit_count) VALUES (%s, %s) RETURNING ip;"""
    sql = """INSERT INTO ips(ip, hit_count) VALUES (%s, %s) ON CONFLICT (ip) DO UPDATE SET hit_count = EXCLUDED.hit_count, log_date = CURRENT_DATE RETURNING ip ;"""
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
            try:
                cur.execute(sql,(ip,ip_list[ip]))
            except:
                pass
                #print("Alredy in DB " + ip )
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
    sql = """SELECT ip FROM ips WHERE received IS NULL;"""
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
        if counter < 100:
            print("ip: " + ip[0])
            data = ipapi.location(ip[0]) 
            try:
                conn = None
                params = config()
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                if not data.get('reserved') is None:
                    print('IF reserver')
                    sql = """UPDATE ips SET received = 1 where ip = %s RETURNING ip;"""
                    cur.execute(sql,(ip[0],))
                else:
                    print('ELSE reserver')
                    sql = """UPDATE ips SET received = 1, org = %s, region = %s, country = %s, country_name = %s, city = %s, asn = %s where ip = %s RETURNING ip;"""
                    cur.execute(sql,(data['org'], data['region'], data['country'], data['country_name'], data['city'], data['asn'], ip[0],))
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            counter = counter + 1
            print(data)
        else:
            print("limit reached sleeping one minute")
            time.sleep(timer - datetime.datetime.timestamp(datetime.datetime.now()) + 60)
            timer = datetime.datetime.timestamp(datetime.datetime.now())
            counter = 0

fill_database(empty_ip)
print('done')


