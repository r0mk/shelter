#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''

Future:
 Black detect: ffmpeg -i out.mp4 -vf blackdetect -f null -
 Note the following doesn't seem to fully work without looking at the debug logs
 On live ffmpeg -y -i rtmp://cp30129.live.edgefcs.net/live/videoops-videoops@50541 -vf blackdetect -t 10 -loglevel debug -f null -

'''

import sys
import os
from subprocess import PIPE, Popen
from threading  import Thread
import time
import logging
import urllib
import urllib2
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x



logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("encoder.log"),
                              logging.StreamHandler()])
logging.info("Starting")

# You will need to register bot in @BotFather 
bot_id = '766315820:AAGCVu4lSJceBqAt9Pzi-3PD8HnpR0x7jJo'
#ID from @MyTelegramID_bot
send_to_id = '-287220904' #Group
#send_to_id = '213833037' #r0mk
#send_to_id = '266734807' #John
# Set how often you want to check in seconds
SLEEP_TIME = 10
FFPROBE = "/usr/bin/ffprobe"

with open('/root/streams.list','r') as f:
    stream_list = f.read().splitlines()
f.close
stream_dict = dict.fromkeys(stream_list,{'video_cur':1,'audio_cur':1, 'video_prev':1, 'audio_prev':1})
#print(stream_list)
#print(stream_dict)
# List of streams to check
#CHECK_STREAMS = ['http://192.99.149.103:8080/mtl_ca/108_CW_NewYork_3236_208/index.m3u8', 'http://54.39.106.158:80/kids/NICKJRUSA/index.m3u8', 'http://54.39.106.158:80/tamil/STARVIJAYHDUS/index.m3u8', 'http://54.39.106.158:80/tamil/SUNMUSICHDUS/index.m3u8', 'http://54.39.106.158:80/tamil/COLORSTAMILHDUS/index.m3u8', 'http://54.39.106.158:80/tamil/NATGEOWILDTAMILUS/index.m3u8']
#CHECK_STREAMS = ['http://54.39.106.158:80/caribban/POWER106FM/index.m3u8a']

ON_POSIX = 'posix' in sys.builtin_module_names

def process_line(std, q):
    partialLine = str("")
    tmpLines=[]
    end_of_message = False
    while (True):
        data = std.read(10)
        
        #print repr(data)
        
        #break when there is no more data
        if len(data) == 0:
            end_of_message = True

        #data needs to be added to previous line
        if ((not '\n' in data) and (not end_of_message)):
            partialLine += data
        #lines are terminated in this string
        else:
            tmpLines = []

            #split by \n
            split = data.split(b"\n")

            #add the rest of partial line to first item of array
            if partialLine != "":
                split[0] = partialLine + split[0]
                partialLine = ""

            #add every item apart from last to tmpLines array
            if len(split) > 1:
                for i in range(len(split)-1):
                    tmpLines.append(split[i])

            #last item is '' if data string ends in \r
            #last line is partial, save for temporary storage
            if split[-1] != "":
                partialLine = split[-1]
            #last line is terminated
            else:
                tmpLines.append(split[-1])
            
            #print split[0]
            q.put(split[0])
            if (end_of_message):
                #print partialLine
                break

def enqueue_output(stdout, queue):
    #for line in iter(stdout.readline, b''):
    #    queue.put(line)
    process_line(stdout, queue)  
    stdout.close()

def run(q, ffcmd, thread_name):
    logging.info("Running " + ffcmd)
    p = Popen(ffcmd,shell=True, stderr=PIPE, stdin=PIPE, bufsize=1, close_fds=ON_POSIX)
    #q = Queue()
    #t = Thread(target=enqueue_output, args=(p.stdout, q))
    #t.daemon = True # thread dies with the program
    #t.start()
    t = Thread(target=enqueue_output, name=thread_name, args=(p.stderr, q))
    t.daemon = True
    t.start()
    return p
         
def probe(stream):
    probeq = Queue()
    logging.info("\n\nChecking " + stream)
    probeproc = run(probeq, FFPROBE + " " + stream, "probethread")
    global stream_dict
    print(stream + '   probe vid_cur   ' + str(stream_dict[stream]['video_cur']))
    print(stream + '   probe vid_prev   ' + str(stream_dict[stream]['video_prev']))
    print(stream + '   probe aud_cur    ' + str(stream_dict[stream]['audio_cur']))
    print(stream + '   probe aud_prev   ' + str(stream_dict[stream]['audio_prev']))
    # Need to read from the queue until the queue is empty and process has exited
    close_time = time.time()+10
    while (True):
        #print('in loop ' + stream)
        #print "Queue not empty"
        if time.time() > close_time:
            return True
        #print probeq.join()
        try:
            line = probeq.get_nowait()
            #logging.info(line)
            #print(time.time())
            if ("Stream #0:0: Video" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                params = {}
                params = dict(stream_dict[stream].items())
                params['video_cur'] = '1'
                stream_dict.update({stream:params})
                #return True
            if ("Stream #0:1: Video" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                params = {}
                params = dict(stream_dict[stream].items())
                params['video_cur'] = '1'
                stream_dict.update({stream:params})
                #return True
            if ("Stream #0:0: Audio" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                params = {}
                params = dict(stream_dict[stream].items())
                params['audio_cur'] = '1'
                stream_dict.update({stream:params})
                #return True
            if ("Stream #0:1: Audio" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                params = {}
                params = dict(stream_dict[stream].items())
                params['audio_cur'] = '1'
                stream_dict.update({stream:params})
                #return True
            elif ("error" in line):
                #print('\n\nupdating stream to error ' + str(stream_dict[stream].items()))
                params = {}
                params = dict(stream_dict[stream].items())
                params['audio_cur'] = '0'
                params['video_cur'] = '0'
                stream_dict.update({stream:params})
                #stream_dict.update({stream:{'video_cur' : 'error', 'audio_cur' : 'error'}})
                #stream_dict[stream].update({'video_cur' : 'error', 'audio_cur' : 'error'})
                #stream_dict[stream]['audio_cur'] = 'error'
                #stream_dict[stream]['video_cur'] = 'error'
                #print('\n\n\nupdating D to error ' + str(di))
                return True
            elif (probeproc.poll() > 0):
                params = {}
                params = dict(stream_dict[stream].items())
                params['audio_cur'] = '0'
                params['video_cur'] = '0'
                stream_dict.update({stream:params})
                return True
            #time.sleep(1)
        except Empty:
            pass
    return False

def live_probe():
    pass

# Endless loop for monitoring

while(True):
    #for stream in CHECK_STREAMS:
    for stream in stream_dict.keys(): 
    #for stream in stream_dict: 
        if probe(stream):
            print(stream_dict)
            if int(stream_dict[stream]['video_cur']) > int(stream_dict[stream]['video_prev']): 
                print(stream + '   vid_cur   ' + str(stream_dict[stream]['video_cur']))
                print(stream + '   vid_prev   ' + str(stream_dict[stream]['video_prev']))
                print(stream + '   aud_cur    ' + str(stream_dict[stream]['audio_cur']))
                print(stream + '   aud_prev   ' + str(stream_dict[stream]['audio_prev']))
                stream_dict[stream]['video_prev'] = 1
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'
                command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=✅  Stream  🎬Video  Restored\n" + str(stream) + "'" 
                print(command)
                try:
                    #command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=✅  Stream  🎬Video  Restored\n" + str(stream) + "'" 
                    print(os.system(command))
                except:
                    print(command)
                    print('Cant send Stream Video Restored\n')
                    pass
            if int(stream_dict[stream]['video_cur']) < int(stream_dict[stream]['video_prev']): 
                print(stream + '   vid_cur   ' + str(stream_dict[stream]['video_cur']))
                print(stream + '   vid_prev   ' + str(stream_dict[stream]['video_prev']))
                print(stream + '   aud_cur    ' + str(stream_dict[stream]['audio_cur']))
                print(stream + '   aud_prev   ' + str(stream_dict[stream]['audio_prev']))
                stream_dict[stream]['video_prev'] = 0
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'
                try:
                    command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=📛Stream 🎬Video Lost\n" + str(stream) + "'" 
                    print(os.system(command))
                except:
                    print('Cant send Stream Video Lost\n')
                    pass
            if int(stream_dict[stream]['audio_cur']) < int(stream_dict[stream]['audio_prev']):
                print(stream + '   vid_cur   ' + str(stream_dict[stream]['video_cur']))
                print(stream + '   vid_prev   ' + str(stream_dict[stream]['video_prev']))
                print(stream + '   aud_cur    ' + str(stream_dict[stream]['audio_cur']))
                print(stream + '   aud_prev   ' + str(stream_dict[stream]['audio_prev']))
                stream_dict[stream]['audio_prev'] = 0
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'
                try:
                    command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=📛Stream 🎼Au  Audio Lost\n"  + str(stream) + "'"
                    os.system(command)
                except:
                    print('Cant send\n')
                    pass
            if int(stream_dict[stream]['audio_cur']) > int(stream_dict[stream]['audio_prev']):
                print(stream + '   vid_cur   ' + str(stream_dict[stream]['video_cur']))
                print(stream + '   vid_prev   ' + str(stream_dict[stream]['video_prev']))
                print(stream + '   aud_cur    ' + str(stream_dict[stream]['audio_cur']))
                print(stream + '   aud_prev   ' + str(stream_dict[stream]['audio_prev']))
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'
                try:
                    time.sleep(1)
                    command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=✅Stream  🎼   Audio Restored\n"  + str(stream) + "'"
                    os.system(command)
                except:
                    print('Cant send Stream Audio Restored\n' + os.read() )
                    pass
                stream_dict[stream]['audio_prev'] = 1
    print(stream + ' else  vid_cur   ' + str(stream_dict[stream]['video_cur']))
    print(stream + ' else  vid_prev   ' + str(stream_dict[stream]['video_prev']))
    print(stream + ' else  aud_cur    ' + str(stream_dict[stream]['audio_cur']))
    print(stream + ' else  aud_prev   ' + str(stream_dict[stream]['audio_prev']))
 
    print('\n\n')
    time.sleep(SLEEP_TIME)
