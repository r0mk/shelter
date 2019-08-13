#!/usr/bin/python3
#tools needed to script working
#apt install python3-pip
#pip3 install mysql-connector-python-rf

import sys
import os
import mysql.connector
from mysql.connector import Error
import datetime
import random
#import subprocess
#import shlex
#from decimal import Decimal 


local_storage = "/root/local_store/"

today =  datetime.date.today() 
tomorrow =  datetime.date.today() + datetime.timedelta(days=1)
dayaftertomorrow = datetime.date.today() + datetime.timedelta(days=2)
today_unix = datetime.datetime.timestamp(datetime.datetime(today.year,today.month,today.day))
tomorrow_unix = datetime.datetime.timestamp(datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day))
dayaftertomorrow_unix = datetime.datetime.timestamp(datetime.datetime(dayaftertomorrow.year,dayaftertomorrow.month,dayaftertomorrow.day))

etime = datetime.datetime.fromtimestamp(dayaftertomorrow_unix)
end_date = "%04d" % dayaftertomorrow.year + "%02d" % dayaftertomorrow.month + "%02d" % dayaftertomorrow.day + "%02d" % etime.hour + "%02d" % etime.minute
time = round(tomorrow_unix)

print("Today " + str(today))
print("Tomorrow " + str(tomorrow))
print("Today unix " + str(today_unix))
print("Tomorrow unix " + str(tomorrow_unix))

try:
    category = sys.argv[1]
except:
    print("Usage: ./script.py category_name")
    sys.exit()


epg_path = "/root/" + category + "_epg.xml"
playlist_path =  "/root/" + category + "_playlist.xml"


def get_data_from_db(category):
    try:
        connection = mysql.connector.connect(host='144.217.77.180',
                             port='3307',
                             database='stalker_db',
                             user='apptsk',
                             password='appt55k')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ",db_Info)
            cursor = connection.cursor()
            query = ("SELECT id FROM media_category WHERE category_name LIKE '%" + category + "%';")
            #print(query)
            cursor.execute(query)
            category_id= cursor.fetchall()
            #print(str(list(category_id)))
            list_of_category_id = []
            for every in category_id:
                #result = result + list((every[0]))
                list_of_category_id.append(every[0])
            #print(list_of_category_id)
            #cursor.execute("select database();")
            #cursor.execute("select * from video limit 3;")
            #record = cursor.fetchone()
            #print ("Your connected to - ", record)
            #!Dont forget to add extra check
            query = ("SELECT DISTINCT(video.id),video.name,video.description,video_series_files.url,video.added FROM video\
                 join video_series_files on video.id=video_series_files.video_id\
                 WHERE category_id in (" + (",".join(str(num) for num in list_of_category_id)) + ")\
                 and is_series =0 ORDER BY video.added DESC\
                 limit 0,6")
            cursor.execute(query)
            movie_list = cursor.fetchall()
            for movie in movie_list:
                print(str(movie[1]))

    except Error as e :
        print ("Error while connecting to MySQL", e)
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return movie_list

movies_list = get_data_from_db(category)
#print(movies_list)

def download_movies(url):
    if url.split('/')[-1] == 'video.m3u8':
        #print("its  stream")
        filename = url.split('/')[-2] 
    else:
        filename = url.split('/')[-1] 
    #This command from my previous script, that possibly works=)
    #ffmpeg -i "$pathname" -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 192k -ac 2 /root/converted/$filename.mp4

    #Uncomment next line!!
    #os.system("/usr/bin/ffmpeg -y -i " + url + " -c copy  -bsf:a aac_adtstoasc " + local_storage + filename + ".mp4")

for every in range(0,len(movies_list)):
    download_movies(movies_list[every][3])    
   
def playlist_epg_generator(movies_list):
    #playlist_result = '<tv generator-info-name="WebGrab+Plus" generator-info-url="http://www.webgrabplus.com">\n <channel id="' + category + '">\n  <display-name lang="en">' + category + '</display-name>\n </channel>\n\n\n'
    playlist_result = ''
    epg_result = '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="WebGrab+Plus" generator-info-url="http://www.webgrabplus.com">\n <channel id="'+ category +'">\n  <display-name lang="en">'+ category + '</display-name>\n </channel>\n'
    counter = 0
    time = round(tomorrow_unix)
    while True:
        for movie in range(0,len(movies_list)):
            lenth= 'none'
            if movies_list[movie][3].split('/')[-1] == 'video.m3u8':
                filename = movies_list[movie][3].split('/')[-2]
            else:
                filename = movies_list[movie][3].split('/')[-1]
            cmd = ("/usr/bin/ffprobe -i " + local_storage + filename + ".mp4 -show_format -v quiet | /bin/sed -n 's/duration=//p'")
            #cmd = ("/usr/bin/ffprobe -i " + local_storage + filename + ".mp4 -show_format -v quiet")
            try:
                get_lenth = os.popen(cmd).read().rstrip()
                #lenth = subprocess.check_output(shlex.split(cmd), shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                #lenth = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
                #output = lenth.communicate()[1] 
                lenth = (int(float(get_lenth)))
            except:
                print("Cant get lenth for movie " + str(movies_list[movie][1]) + ' url: ' +  str(movies_list[movie][3]) + ' omitting..')
                counter = counter + 1
            if lenth == 'none':
                continue 
            #lenth = subprocess.run("ffprobe -i " + local_storage + filename + ".mp4 -show_format -v quiet | sed -n 's/duration=//p'")
            #print("ffprobe -i " + local_storage + filename + ".mp4 -show_format -v quiet | sed -n 's/duration=//p'")
            #print(movies_list[movie][1])
            #print(filename + " lenth  " +  str(lenth))
            counter = counter + 1
            #print(str(counter) + " counter")
            ctime = datetime.datetime.fromtimestamp(time)
            epg_time = "%04d" %ctime.year + "%02d" % ctime.month + "%02d" % ctime.day + "%02d" % ctime.hour + "%02d" % ctime.minute
            epg_result = epg_result + ' <programme start="' + epg_time + ' -0500" '
            playlist_result = playlist_result + "#EXT-X-UTC:" +  str(time) + "\n" + local_storage + filename + ".mp4\n"
            time = time + lenth
            ctime = datetime.datetime.fromtimestamp(time)
            epg_time = "%04d" % ctime.year + "%02d" % ctime.month + "%02d" % ctime.day + "%02d" % ctime.hour + "%02d" % ctime.minute
            if time > dayaftertomorrow_unix:
                epg_result = epg_result + 'stop=' + end_date + ' -0500" channel="' + category + '">\n' 
                break
            else:
                epg_result = epg_result + 'stop="' + epg_time + ' -0500" channel="' + category + '">\n'
                epg_result = epg_result +  ' <title lang=\"en\">' + movies_list[movie][1] + '</title>\n </programme>'

        if time > dayaftertomorrow_unix:
            print("Playlist for tomorrow generated.")
            print("EPG generated too.")
            break
        if counter > 160: break
        #return playlist_result, epg_result
    with open(epg_path, "w") as f:
        f.write(epg_result)

    with open(playlist_path, "w") as f:
        f.write(playlist_result)

playlist_epg_generator(movies_list)
