#!/usr/bin/python2
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
bot_id = ''
#ID from @MyTelegramID_bot
#send_to_id = '213833037' #r0mk
# Set how often you want to check in seconds
SLEEP_TIME = 30
FFPROBE = "/usr/bin/ffprobe"

with open('/root/streams.list','r') as f:
    stream_list = f.read().splitlines()
f.close
stream_dict = dict.fromkeys(stream_list,1)
print(stream_list)
print(stream_dict)


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
    logging.info("Checking " + stream)
    probeproc = run(probeq, FFPROBE + " " + stream, "probethread")
    # Need to read from the queue until the queue is empty and process has exited
    while (True):
        #print "Queue not empty"
#        print probeq.join()
        try:
            line = probeq.get_nowait()
            logging.info(line)
            '''
            Possible error responses:
            Server error: Failed to play stream
            Input/output error
            
            Need a regex to match for video found!
            Sample: Stream #0:0: Video: h264 (Baseline), yuv420p, 640x360 [SAR 1:1 DAR 16:9], 655 kb/s, 25 tbr, 1k tbn, 50 tbc
            Should also look for audio
            '''
           
            if ("Stream #0:0: Video" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                return True
            if ("Stream #0:1: Video" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                return True
            if ("Stream #0:0: Audio" in line):
                logging.info("Found stream " + stream)
                logging.info(line)
                return False
            elif ("error" in line):
                return False
            elif (probeproc.poll() > 0):
                return False
            
            # Stream #0:0: Audio: aac
            # Make sure we don't spin out of control
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
        if (probe(stream)):
	    if stream_dict[stream] == 0:
                #idata = urllib.urlencode({ 'chat_id': send_to_id, 'text': '<b>' + 'Stream restored: \n' +  '</b>' + str(stream), 'parse_mode': 'HTML', 'disable_web_page_preview': 1})
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'

                try:
                    time.sleep(1)
                    command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=Stream restored\n"  + str(stream) + "'"
                    os.system(command)
                    #f = urllib.urlopen(url, idata)
                    #print(f.read())
                except:
                    print('cant send')
                    pass
                
            stream_dict[stream] = 1

        else:
            logging.info("Error with " + stream + " sending alert")
            '''
            This needs to check if there has already been an error message sent
            If so it shouldn't send another one for x mins
            Also needs to send a message when the problem is cleared
            '''
            #send_message(stream)
            #idata = idata.encode('ascii')
            #req = urllib.request.Request('https://api.telegram.org/bot' + bot_id + '/sendMessage' )

	    if stream_dict[stream] == 1:
                #idata = urllib.urlencode({ 'chat_id': send_to_id, 'text': '<b>' + 'problem with stream: \n' +  '</b>' + str(stream), 'parse_mode': 'HTML', 'disable_web_page_preview': 1})
                url = 'https://api.telegram.org/bot' + bot_id + '/sendMessage'

                try:
                    time.sleep(1)
                    command = "curl -s -X POST " + url + " -d chat_id=" + send_to_id + " -d 'text=problem with stream\n"  + str(stream) + "'"
                    print(command)
                    #f = os.system("curl -s -X POST" + url + "-d chat_id=" + send_to_id + "-d text=" + idata + "")
                    os.system(command)
                    #print(f)
                    #f = urllib2.urlopen(url, idata)
                    #print(f.read())
                except:
                    print('cant send')
                    pass

            stream_dict[stream] = 0
    time.sleep(SLEEP_TIME)
