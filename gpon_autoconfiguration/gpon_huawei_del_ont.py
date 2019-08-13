#!/usr/bin/python2
import sys
import telnetlib 
import os
import re

#Check input arguments
if len(sys.argv) < 2:
    print("Syntax:\n ./script port ont_id")
    sys.exit()

user = ''
password = ''
host = ''
port = int(sys.argv[1])
ont_id = int(sys.argv[2])

#Check if host available
response = os.system("ping -c 1 " + host + " > /dev/null 2>&1")
if response == 0:
    #host available
    pass
else:
    print("ERROR: host " + str(host) + " is unreachable") 
    sys.exit()

#Open Connection 
try:
    tn = telnetlib.Telnet(host,timeout=3)
except:
    sys.exit('Cant telnet')

#searching free ont_id
def delete_ont(port,ont_id):
    olt_row_output = []
    tn.expect(['>>User name:'],3)
    tn.write(user + "\n")
    tn.expect(['>>User password:'],3)
    tn.write(password + "\n")
    olt_row_output.extend((tn.expect(['>'])[2]).split('\n'))
    tn.write("enable\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("scroll 512\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("config\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("btv\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("igmp user delete service-port " + str(10000 + port * 200 + ont_id) + "\n")
    tn.expect([':'])
    tn.write('y\n')
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("undo service-port " + str(20000 + port * 200 + ont_id) + "\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("undo service-port " + str(10000 + port * 200 + ont_id) + "\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("undo service-port " + str(port * 200 + ont_id) + "\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("interface gpon 0/0\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont delete " + str(port) + " " + str(ont_id) + "\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    tn.expect([':'])
    tn.write('y\n')
    return(olt_row_output)

    
#Main. Get data from switch and decorate
output_result = delete_ont(port,ont_id)
for lines in output_result:
    print(lines)


#close connection
#tn.write("quit\n")
tn.close()
