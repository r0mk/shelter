#!/usr/bin/python2
import sys
import telnetlib 
import os
import time

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
        if version.__contains__('QSW-2800-28T-DC'):
            model='Qtech QSW-2800-28T-DC'
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
    tn.write('system-view\n')
    tn.expect([']'])[2]
    tn.write('disp int eth 0/0/' + port + ' | inc state\n')
    port_state = tn.expect([']'])[2].split()
    if 'Administratively' in port_state:
        print("admin down, un sh berfor test")
        tn.write('interface Ethernet 0/0/' + port + '\n')
        tn.expect([']'])
        tn.write('un sh\n')
        tn.expect([']'])
        tn.write('virtual-cable-test\n')
        tn.expect([']'])
        tn.write('y\n')
        tn.expect([']'])
        time.sleep(3)
        tn.write('virtual-cable-test\n')
        tn.expect([']'])
        tn.write('y\n')
        tn.expect([']'])
        time.sleep(3)
        tn.write('virtual-cable-test\n')
        tn.expect([']'])
        tn.write('y\n')
        huawei_raw_output.extend((tn.expect([']'])[2]).split('\n'))
        tn.write('sh\n')
        tn.expect([']'])
        tn.write('quit\n')
        tn.expect([']'])
    else:
        tn.write('interface Ethernet 0/0/' + port + '\n')
        tn.expect([']'])
        tn.write('virtual-cable-test\n')
        tn.expect([']'])
        tn.write('y\n')
        tn.expect([']?'])
        time.sleep(3)
        tn.write('virtual-cable-test\n')
        tn.expect([']'])
        tn.write('y\n')
        tn.expect([']'])
        time.sleep(3)
        tn.write('virtual-cable-test\n')
        tn.expect([']?'])
        tn.write('y\n')
        huawei_raw_output.extend((tn.expect([']'])[2]).split('\n'))
        tn.write('quit\n')
        tn.expect([']'])
    return huawei_raw_output

#Qtech
def qtech_get_info(port):
    qtech_raw_output = []
    tn.write('terminal length 0\n')
    tn.expect(['#'])[2]
    if model == 'Qtech QSW-2800-28T-AC':
        tn.write('virt int ethernet 1/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    elif model == 'Qtech QSW-2850-28T-AC':
        tn.write('show interface ethernet 1/0/' + port + ' | inc protocol\n')
        port_state = tn.expect(['#'])[2].split()
        if 'administratively' in port_state:
            tn.write('config\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('interface ethernet 1/0/' + port + '\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('no sh\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('quit\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('quit\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('virt int ethernet 1/0/' + port + '\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('config\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('interface ethernet 1/0/' + port + '\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('shut\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('quit\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
            tn.write('quit\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        else:
            tn.write('virt int ethernet 1/0/' + port + '\n')
            qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    elif model == 'Qtech QSW-3470-28T-AC':
        tn.write('virt int ethernet 1/0/' + port + '\n')
        qtech_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    elif model == 'Qtech QSW-2800-28T-DC':
        tn.write('virt int ethernet 1/' + port + '\n')
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
    tn.write('test cable-diagnostics tdr interface ethernet 1/' + port + '\n')
    tn.expect(['#'])
    time.sleep(10)
    tn.write('show cable-diagnostics tdr interface ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    return edgecore_raw_output

#Raisecom
def raisecom_get_info(port):
    raisecom_raw_output=[]
    tn.write('terminal page-break disable\n')
    tn.expect(['#'])
    tn.write('sh interface port ' + port + '\n')
    port_state = tn.expect(['#'])[2].split()
    if 'disable' in port_state:
        tn.write('config\n')
        tn.expect(['#'])
        tn.write('int port ' + port + '\n')
        tn.expect(['#'])
        tn.write('no shut\n')
        tn.expect(['#'])
        tn.write('exit\n')
        tn.expect(['#'])
        tn.write('exit\n')
        tn.expect(['#'])
        tn.write('test cable-diagnostics port-list ' + port + '\n')
        tn.expect(['#'])[2]
        time.sleep(5)
        tn.write('show cable-diagnostics port-list ' + port + '\n')
        raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
        tn.write('config\n')
        tn.expect(['#'])[2]
        tn.write('int port ' + port + '\n')
        tn.expect(['#'])[2]
        tn.write('shut\n')
        tn.expect(['#'])[2]
        tn.write('exit\n')
        tn.expect(['#'])[2]
        tn.write('exit\n')
    else:
        tn.write('test cable-diagnostics port-list ' + port + '\n')
        time.sleep(5)
        tn.expect(['#'])[2]
        tn.write('show cable-diagnostics port-list ' + port + '\n')
        raisecom_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    return raisecom_raw_output

#Decorate switch output
def huawei_output_decoration(huawei_raw_output):
    result = []
    word_list = ['Pair']
    for s in huawei_raw_output:
        for word in word_list: 
            if word in s:
                s = s.replace('Short', 'Short <img src="icon_sad.gif">')
                result.append(s)
    return result

def edge_core_output_decoration(edgecore_raw_output):
    result = []
    word_list = ['Up', 'Down', 'Disable']
    for s in edgecore_raw_output:
        for word in word_list:
            if word in s:
                result.append(s)
    return result

def qtech_output_decoration(qtech_raw_output):
    result = []
    word_list = ['Pairs', 'NA', 'open', 'short', 'well' ]
    for s in qtech_raw_output:
        for word in word_list:
            if word in s:
                s = s.replace('short', 'short <img src="icon_sad.gif">')
                result.append(s)
    return result

def raisecom_output_decoration(raisecom_raw_output):
    result = []
    word_list = ['Issued', 'Port']
    for s in raisecom_raw_output:
        for word in word_list:
            if word in s:
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
