#!/usr/bin/python3
import telnetlib

user = ''
password = ''
host = ''

try:
        tn = telnetlib.Telnet(timeout=3)
except:
        sys.exit('Cannot telnet')

tn.open(host)

tn.read_until('gin:'.encode('ascii'))[2]
tn.write(user.encode('ascii') + b"\r")
tn.read_until(b"ssword:")[2]
tn.write(password.encode('ascii') + b"\n\r")
tn.expect(['#'.encode('ascii')],timeout=2)
tn.write(b"show version\n\r")
print(tn.expect([b'#'],timeout=2)[2])
tn.write(b"exit\n")
tn.close()

