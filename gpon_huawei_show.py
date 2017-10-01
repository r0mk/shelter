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
port = sys.argv[1]
ont_id = sys.argv[2]

#Check if host available
response = os.system("ping -c 1 " + host + " > /dev/null 2>&1")
if response == 0:
    #host available
    pass
else:
    print("ERROR: host " + str(host) + " is unreachable") 
    sys.exit()

#Setting commands to OLT
if port == 'all':
    display_command = "display ont info 0 0 all\n"
else:
    display_command =  "display ont info 0 0 " + str(port) + ' ' + str(ont_id) + '\n'

#Open Connection 
try:
    tn = telnetlib.Telnet(host,timeout=3)
except:
    sys.exit('Cant telnet')

#Try to guess commutator model by 'sh ver' output
def get_info_ont():
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
    tn.write(display_command)
    #print(tn.expect(['#']))
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('quit\n')
    tn.expect([':'])
    tn.write('y\n')
    #print(olt_row_output)
    return(olt_row_output)

def ont_list(olt_raw_output):
    print('Port ont_id  serial  login')
    for lines in olt_raw_output:
        serial = re.search('(^ *0/ 0/\d) *(\S*) *(.{16}) *active', lines)
        if serial:
            port = serial.group(1)
            ont_id = serial.group(2)
            serial = serial.group(3)
        if serial:
            for logins in olt_raw_output:
                login = re.search(port + ' *' + ont_id + ' *(.{10})\r', logins)
                if login:
                    if serial:
                        print_port = re.search('^ *0/ 0/(\d)', logins)
                        print(print_port.group(1) + ' ' + ont_id + ' ' + serial + ' ' + login.group(1))

#Decorate switch output
def huawei_output_decoration(huawei_raw_output):
    result = []
    word_list = ['current', 'Description', 'Speed', 'Duplex', 'packets', 'Total Error', ' security ', 'circuit-id']
    for s in huawei_raw_output:
        for word in word_list: 
            if word in s:
                s = s.replace('DOWN', 'Down <img src="status_red.gif">')
                s = s.replace('UP', 'Up <img src="status_green.gif">')
                s = s.replace('Administratively', '<b>Administratively</b>')
                s = s.replace('Loopback: NONE', '')
                s = s.replace('Loopback: NONE', '')
                s = s.replace('Speed', '<b>Speed</b>')
                s = s.replace('Duplex', '<b>Duplex</b>')
                s = s.replace('Negotiation: ENABLE', '')
                s = s.replace('Discard        :                   0,', '')
                s = s.replace(' dhcp option82 circuit-id format user-defined ', '<b>Login</b>')
                result.append(s)
    #for idx, item in enumerate(result):
    #    if 'Line protocol current state : DOWN' in item:
    #            item = replace_all(item, 'r0mk')
    #            list[idx] = item
    return result


#Main. Get data from switch and decorate
olt_raw_output = get_info_ont()
if port == 'all':
    ont_list(olt_raw_output)
else:
    for items in olt_raw_output:
        print(items)

#def ont_list(olt_raw_output):
#    print('Port ont_id  serial  login')
#    for lines in olt_raw_output:
#        serial = re.search('(^ *0/ 0/\d) *(\S*) *(.{16}) *active', lines)
#        if serial:
#            port = serial.group(1)
#            ont_id = serial.group(2)
#            serial = serial.group(3)
#        if port and serial:
#            for logins in olt_raw_output:
#                login = re.search(port + ' *' + ont_id + ' *(.{10})\r', logins)
#                if login:
#                    if serial:
#                        print_port = re.search('^ *0/ 0/(\d)', logins)
#                        print(print_port.group(1) + ' ' + ont_id + ' ' + serial + ' ' + login.group(1))

#close connection
#tn.write("quit\n")
tn.close()
