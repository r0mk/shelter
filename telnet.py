#!/usr/bin/python3
import sys
import telnetlib 
import os

#Check input arguments
if len(sys.argv) < 4:
    print "Syntax:\n ./script login pass ip"
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
    tn.expect(['Username:','login'],3)
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
        if version.__contains__('ISCOM2128EA-MA-AC'):
            model='RAISECOM ISCOM2128EA-MA-AC'
        if version.__contains__('QSW-2800-28T-AC'):
           model='QTECH QSW-2800-28T-AC'
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
        print "HUAWEI Submodel(version) detection problem"
        sys.exit()
    huawei_raw_output.extend((tn.expect(['>'])[2]).split('\n'))
    return (huawei_raw_output)

#Edge core
def edge_core_get_info(port):
    edgecore_raw_output=[]
    tn.write('terminal length 0\n')
    tn.expect(['#'])[2]
    tn.write('show interfaces counters ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show interfaces status ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('sh running-config interface ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    tn.write('show mac-address-table interface ethernet 1/' + port + '\n')
    edgecore_raw_output.extend((tn.expect(['#'])[2]).split('\n'))
    return edgecore_raw_output


#Decorate switch output
def huawei_output_decoration(huawei_raw_output):
    word_list = ['current', 'Description', 'Speed', 'Duplex', 'packets', 'Total Error', ' security ']
    for s in huawei_raw_output:
        for word in word_list: 
            if word in s:
                print(s)
    #add DHCP decoration

def edge_core_output_decoration(edgecore_raw_output):
    word_list = ['Octets Input', 'Error Input', 'Port Admin', 'Link Status', 'Port Operation', 'Uptime','Learned-PSEC', 'Name', 'circuit-id', 'Speed-duplex' ]
    for s in edgecore_raw_output:
        for word in word_list:
            if word in s:
                print(s)

if 'HUAWEI' in model.split(' '):
    huawei_raw_output = huawei_get_info(port)
    huawei_output_decoration(huawei_raw_output)

if model == 'Edge Core':
    edgecore_raw_output = edge_core_get_info(port)
    edge_core_output_decoration(edgecore_raw_output)


    
#close connection
tn.write("quit\n")
tn.close()
