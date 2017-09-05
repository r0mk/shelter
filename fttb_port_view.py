#!/usr/bin/python2
import sys
import telnetlib 
import os

#Check input arguments
if len(sys.argv) < 4:
    print("Syntax:\n ./script login pass ip")
    sys.exit()

user = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]
port = sys.argv[4]

#Check if host available
response = os.system("ping -c 1 " + host + " > /dev/null 2>&1")
if response == 0:
    #host available
    pass
else:
    print("ERROR: host " + host + " is unreachable") 
    sys.exit()

#Open Connection 
try:
    tn = telnetlib.Telnet(host,timeout=3)
except:
    sys.exit('Cant telnet')

#Try to guess commutator model by 'sh ver' output
def model_guess(ip):
    #tn = telnetlib.Telnet(ip)
    model = 0
    tn.expect(['Username:', 'login', 'Login:'],3)
    tn.write(user + "\n")
    tn.expect(['Password:'],3)
    tn.write(password + "\n")
    tn.expect(['>','#'])[2]
    tn.write("disp ver\n")
    version=(tn.expect(['>','#'])[2]).split()
    #Uncomment next line and comment previous to debug
    #print(tn.expect(['>','#'])[2]).split(' ')
    if version.__contains__('V100R005C01SPC100)'):
        model='HUAWEI V100R005C01SPC100'
    elif version.__contains__('V100R006C05)'):
        model='HUAWEI V100R006C05'
    else:
        tn.write("sh ver\n")
        #Uncomment next line to debug
        #print(tn.expect(['>','#'])[2].split(' '))
        version=tn.expect(['>','#'])[2].split(' ')
        if version.__contains__('ISCOM2128EA-MA-AC.'):
            model='Raisecom'
        if version.__contains__('QSW-2800-28T-AC'):
           model='Qtech QSW-2800-28T-AC'
        if version.__contains__('QSW-2850-28T-AC,'):
            model='Qtech QSW-2850-28T-AC'
        if version.__contains__('QSW-3470-28T-AC'):
            model='Qtech QSW-3470-28T-AC'
        if version.__contains__('Marvell'):
            model='Edge Core'
    if model == 0:
        tn.write("quit\n")
        tn.close()
        sys.exit("Unknown device model")
    else:
        return model


model=(model_guess(host))
print(model)

#Get ethernet port info
#Huawei
def huawei_get_info(port):
    huawei_raw_output = []
    tn.write('screen-length 0 temporary\n')
    tn.expect(['>'])[2]
    tn.write('disp interface Ethernet 0/0/' + port + '\n')
    huawei_raw_output.extend((tn.expect(['>'])[2]).split('\n'))
    tn.write('disp cur int Ethernet 0/0/' + port + '\n')
    huawei_raw_output.extend((tn.expect(['>'])[2]).split('\n'))
    if model == 'HUAWEI V100R006C05':
        tn.write('disp mac-address security Ethernet 0/0/' + port + '\n')
    elif model == 'HUAWEI V100R005C01SPC100':
        tn.write('disp mac-address secure-dynamic Ethernet 0/0/' + port + '\n')
    else:
        print("HUAWEI Submodel(version) detection problem")
        sys.exit()
    huawei_raw_output.extend((tn.expect(['>'])[2]).split('\n'))
    return (huawei_raw_output)

#Qtech
def qtech_get_info(port):
    qtech_raw_output = []
    tn.write('terminal length 0\n')
    tn.expect(['#'])[2]
    if model == 'Qtech QSW-2800-28T-AC':
        tn.write('sh int Ethernet 1/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh mac-address-t int ethernet1/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh ru int ethernet1/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    elif model == 'Qtech QSW-2850-28T-AC':
        tn.write('sh int Ethernet 1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh mac-address-t int ethernet1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh ru int ethernet1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    elif model == 'Qtech QSW-3470-28T-AC':
        tn.write('sh int Ethernet 1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh mac-address-t int ethernet1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('sh ru int ethernet1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    else:
        print("Qtech model detection problem")
        sys.exit()
    return qtech_raw_output


#Edge core
def edge_core_get_info(port):
    edgecore_raw_output=[]
    tn.write('terminal length 0\n')
    tn.expect(['#'])[2]
    tn.write('sh running-config int ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show interfaces status ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show interfaces counters ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show mac-address-table interface ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    return edgecore_raw_output

#Raisecom
def raisecom_get_info(port):
    raisecom_raw_output=[]
    tn.write('terminal page-break disable\n')
    tn.expect(['#'])[2]
    tn.write('show interface port ' + port + '\n')
    raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show interface port ' + port + ' statistics\n')
    raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show running-config interface port ' + port + '\n')
    raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show mac-address-table l2-address port ' + port + '\n')
    raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show ip dhcp snooping binding\n')
    raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    return raisecom_raw_output

#Decorate switch output
def huawei_output_decoration(huawei_raw_output):
    result = []
    word_list = ['current', 'Description', 'Speed', 'Duplex', 'packets', 'Total Error', ' security ', 'circuit-id']
    for s in huawei_raw_output:
        for word in word_list: 
            if word in s:
                s = s.replace('DOWN', ' <img src="status_red.gif">')
                s = s.replace('UP', ' <img src="status_green.gif">')
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

def edge_core_output_decoration(edgecore_raw_output):
    result = []
    word_list = ['Octets Input', 'Error Input', 'Port Admin', 'Link Status', 'Port Operation', 'Uptime','Learned-PSEC', 'Name', 'circuit-id', 'Speed-duplex' ]
    for s in edgecore_raw_output:
        for word in word_list:
            if word in s:
                s = s.replace(' Up', '<img src="status_green.gif">')
                s = s.replace(' Down', '<img src="status_red.gif">')
                s = s.replace('Operation Speed-duplex:', '<b>Speed</b>')
                s = s.replace('ip dhcp snooping information option circuit-id string', '<b>Login</b>')
                result.append(s)
    return result

def qtech_output_decoration(qtech_raw_output):
    result = []
    word_list = ['line protocol', 'last status change', 'input packet', 'input error', 'output packet', 'output error', 'DYNAMIC', 'SECURED', 'subscriber-id', 'description', 'Auto-duplex:' ]
    for s in qtech_raw_output:
        for word in word_list:
            if word in s:
                s = s.replace('ip dhcp snooping information option subscriber-id', '<b>Login</b>')
                s = s.replace('down,', '<img src="status_red.gif">')
                s = s.replace('down', '<img src="status_red.gif">')
                s = s.replace(' up', '<img src="status_green.gif">')
                s = s.replace('administratively', '<b>Administratively</b>')
                s = s.replace(', Auto-speed:', '<br>  <b>Speed</b>')
                s = s.replace('Auto-duplex:', '<b>Duplex:</b>')
                s = s.replace(', 0 frame alignment, 0 overrun, 0 ignored,', '')
                s = s.replace(', 0 collisions, 0 late collisions, 0 pause frame', '')
                s = s.replace(', 0 no buffer', '')
                s = s.replace(', 0 underruns', '')
                s = s.replace('description', '<b>description</b>')
                result.append(s)
    return result

def raisecom_output_decoration(raisecom_raw_output):
    result = []
    word_list = ['off/off', 'InOctets:', 'CRCAlignErrors', 'OutOctets:', 'OutputError(Pkts):', 'dhcp-snooping', 'Hit', 'description', 'circuit-id', 'Static']
    for s in raisecom_raw_output:
        for word in word_list:
            if word in s:
                s = s.replace('down', '<b>Operate</b><img src="status_red.gif">')
                s = s.replace('enableForward', '')
                s = s.replace('enable   Forward', '')
                s = s.replace('disable', '<b>Admin</b><img src="status_red.gif">')
                s = s.replace('enableup', '<b>Admin</b><img src="status_green.gif"><br><b>Operate</b><img src="status_green.gif"><br><b>Speed</b>')
                s = s.replace('enable', '<b>Admin</b><img src="status_green.gif"><br>')
                s = s.replace('description', '<b>description</b>')
                s = s.replace('lldp disable', '')
                s = s.replace('spanning-tree disable ', '')
                s = s.replace('pppoeagent enable', '')
                s = s.replace('ip dhcp information option circuit-id', '<b>Login</b>')
                result.append(s)

    return result



#Main. Get data from switch and decorate
if 'HUAWEI' in model.split(' '):
    huawei_raw_output = huawei_get_info(port)
    for lines in huawei_output_decoration(huawei_raw_output):
        print(lines)

if model == 'Edge Core':
    edgecore_raw_output = edge_core_get_info(port)
    for lines in edge_core_output_decoration(edgecore_raw_output):
        print(lines)

if 'Qtech'  in model.split(' '):
    qtech_raw_output = qtech_get_info(port)
    for lines in qtech_output_decoration(qtech_raw_output):
        print(lines)

if model == 'Raisecom':
    raisecom_raw_output = raisecom_get_info(port)
    for lines in raisecom_output_decoration(raisecom_raw_output):
        print(lines)


    
#close connection
tn.write("quit\n")
tn.close()
