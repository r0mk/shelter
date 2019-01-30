#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import system
from datetime import datetime
import sys
import re
import telnetlib

def ping(host):
    response = system("ping -c 1 " + host + " > /dev/null 2>&1")
    if response == 0:
        return True
    else:   
        return False

def start_telnet(host, user, password):
    telnet = telnetlib.Telnet(host)
    telnet.expect([b'Username:', b'login', b'User name:', b'Login:'], 3)
    telnet.write(user.encode('utf-8') + b"\r\n")
    telnet.expect([b'Password:'], 5)
    telnet.write(password.encode('utf-8') + b"\r\n")
    success_login = telnet.expect([b'>', b'#'], 10)
    if success_login.__contains__(None):
        return False
    else:
        pass
    telnet.write(b'terminal length 0\r\n')
    telnet.expect([b'#'])
    return telnet

def get_showarp(telnet):
    check = False
    telnet.write(b'show arp\r\n')
    return telnet.expect([b'#'])[2].decode('utf-8').split('\r\n')

def to_file(host, text):
    with open(sys.argv[0] + '.log', 'a') as f:
        f.write('{:^15}| {:^20}| {}\n'.format(host, datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"), text))

def parsing(host, arplist, mask):
    check = False
    for lines in arplist:
        if '.' in lines:
            l = [s for s in lines.split(' ') if not s == '']
            to_file(host, '{} {}'.format(l[1], l[3]))
            for s in l:
                if re.findall(mask, s):
                    check = True
                    # dict_out = {'ip': l[1], 'mac': l[3]}
                    print('{} {}'.format(l[1], l[3]))
        else:
            pass
    return check

def main(host, search, user, password):
    if ping(host) is True:
        telnet = start_telnet(host, user, password)
        if telnet is False:
            print('Error: host {} authentication failed'.format(host))
            to_file(host, 'Error: authentication failed')
            raise SystemExit(1)
        else:
            check = parsing(host, get_showarp(telnet), search)
            telnet.close()
            if check:
                raise SystemExit(0)
            else:
                raise SystemExit(1)
    else:
        print('Error: host {} is unreachable'.format(host))
        to_file(host, 'Error: host is unreachable')
        raise SystemExit(1)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('./script.py cisco_ip search_mask login pass')
        raise SystemExit(...)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
