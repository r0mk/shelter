#!/usr/bin/python3
import sys
import telnetlib 
import os

#Check input arguments
if len(sys.argv) < 3:
    print "Syntax:\n ./script login pass ip"
    sys.exit()

user = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]

#Check if host available
response = os.system("ping -c 1 " + host + " > /dev/null 2>&1")
if response == 0:
    #host available
    pass
else:
    print("ERROR: host " + host + " is unreachable") 
    sys.exit()

#Open Connection
tn = telnetlib.Telnet(host)


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
    version=(tn.expect(['>','#'])[2]).split(' ')
    #Uncomment next line to debug
    #print(tn.expect(['>','#'])[2]).split(' ')
    if version.__contains__('HUAWEI'):
        model='ITS HUAWEI'
    else:
        tn.write("sh ver\n")
        #Uncomment next line to debug
        #print(tn.expect(['>','#'])[2].split(' '))
        version=tn.expect(['>','#'])[2].split(' ')
        if version.__contains__('ISCOM2128EA-MA-AC'):
            model='ITS RAISECOM ISCOM2128EA-MA-AC'
        if version.__contains__('QSW-2800-28T-AC'):
           model='ITS QTECH QSW-2800-28T-AC'
        if version.__contains__('QSW-2850-28T-AC,'):
            model='ITS New Qtech QSW-2850-28T-AC'
    if model == 0:
        tn.write("quit\n")
        tn.close()
        sys.exit("Unknown device model")
    else:
        return model


model=(model_guess(host))
print(model)

#close connection
tn.write("quit\n")
tn.close()
