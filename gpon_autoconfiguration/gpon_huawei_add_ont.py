#!/usr/bin/python2
import sys
import telnetlib 
import os
import re

#Check input arguments
if len(sys.argv) < 4:
    print("Syntax:\n ./script port serial login profile")
    sys.exit()

user = ''
password = ''
host = ''
port = int(sys.argv[1])
serial = sys.argv[2]
login = sys.argv[3]
profile = sys.argv[4]

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
def get_ont_list_on_port(port):
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
    tn.write("display ont info 0 0 " + str(port) + ' all\n')
    #print(tn.expect(['#']))
    olt_row_output.extend((tn.expect(['#'])[2]).split('\n'))
    #tn.write('quit\n')
    #tn.expect([':'])
    #tn.write('y\n')
    #print(olt_row_output)
    return(olt_row_output)

def search_empty_ont_id(ont_list_on_port):
    ids_list = []
    count = 0
    hole_found = 0
    for lines in ont_list_on_port:
        serial = re.search('(^ *0/ 0/\d) *(\S*) *(.{16}) *active', lines)
        if serial:
            ids_list.append(int(serial.group(2)))
    for every in ids_list:
        count = count + 1
        #print(str(ids_list[every]) + '     every')
        #print(str(ids_list[count]) + '     count')
        if ids_list[int(every) - 1] == count:
            pass
        else:
            hole_found = 1
            break
    if hole_found != 1:
        count = count + 1
    return(count)

def apply_config_to_olt(empty_ont_id):
    apply_config_output = []
    ont_id = int(empty_ont_id)
    tn.write("config\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("interface gpon 0/0\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('ont add ' + str(port) + ' ' + str(ont_id) + ' sn-auth "' + serial + '" omci ont-lineprofile-id 30 ont-srvprofile-id 30 desc "' + login + '"\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont port native-vlan " + str(port) + ' ' + str(ont_id) + ' eth 1 vlan 300 priority 0\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont port native-vlan " + str(port) + ' ' + str(ont_id) + ' eth 2 vlan 300 priority 0\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont port native-vlan " + str(port) + ' ' + str(ont_id) + ' eth 3 vlan 500 priority 4\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont port native-vlan " + str(port) + ' ' + str(ont_id) + ' eth 4 vlan 500 priority 4\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("ont port native-vlan " + str(port) + ' ' + str(ont_id) + ' iphost vlan 400 priority 5\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('service-port ' + str(port * 200 + ont_id) + ' vlan 3043 gpon 0/0/' + str(port) + ' ont ' + str(ont_id) + ' gemport 1 multi-service user-vlan 300 tag-transform translate-and-add inner-vlan 300 rx-cttr 31 tx-cttr 31\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("service-port " + str(10000 + port * 200 + ont_id) + ' vlan 3043 gpon 0/0/' + str(port) + ' ont ' + str(ont_id) + ' gemport 2 multi-service user-vlan 500 tag-transform translate-and-add inner-vlan 500 rx-cttr 32 tx-cttr 32\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("service-port " + str(20000 + port * 200 + ont_id) + ' vlan 3043 gpon 0/0/' + str(port) + ' ont ' + str(ont_id) + ' gemport 3 multi-service user-vlan 400 tag-transform translate-and-add inner-vlan 400 rx-cttr 33 tx-cttr 33\n')
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("btv\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("igmp user add service-port " + str(10000 + port * 200 + ont_id) + " no-auth\n")
    apply_config_output.extend((tn.expect([':'])[2]).split('\n'))
    tn.write("\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("multicast-vlan 1502\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("igmp multicast-vlan member service-port " + str(10000 + port * 200 +ont_id) + "\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    apply_config_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write("quit\n")
    tn.expect([':'])
    tn.write('y\n')
    return(apply_config_output)



    
#Main. Get data from switch and decorate
ont_list_on_port = get_ont_list_on_port(port)
empty_ont_id = search_empty_ont_id(ont_list_on_port)
output_result = apply_config_to_olt(empty_ont_id)
for lines in output_result:
    print(lines)


#close connection
#tn.write("quit\n")
tn.close()
