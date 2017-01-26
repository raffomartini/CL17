#!/usr/bin/env python
'''building the clear_ap command'''

from wlcsshshell import WlcSshShell
import re

ip = '10.130.0.9'
username = 'cisco'
password = 'C1sco123'

wlc = {
    'ip': ip,
    'username': username,
    'password': password
}


if __name__ == '__main__':
    with open('command_rename_ap')as f:
        commands = f.read().splitlines()
    WlcSshShell.DEBUG = True
    wlc_session = WlcSshShell(**wlc)
    wlc_session.send_commands(commands)




