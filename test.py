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

    output = '''\
show ap summary
Number of APs.................................... 21
Global AP User Name.............................. Not Configured
Global AP Dot1x User Name........................ Not Configured
AP Name             Slots  AP Model              Ethernet MAC       Location          Country     IP Address       Clients   DSE Location
------------------  -----  --------------------  -----------------  ----------------  ----------  ---------------  --------  --------------
AP1231-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:61:86  2143 MEO-Arena    DE          10.130.0.33        0       [0 ,0 ,0 ]
AP1283-3702e         2     AIR-CAP3702E-E-K9     bc:16:65:09:18:64  2143 MEO-Arena    DE          10.130.0.36        0       [0 ,0 ,0 ]
AP1239-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:62:c2  2143 Meo Arena    DE          10.130.0.24        0       [0 ,0 ,0 ]
AP1240-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:67:ce  Registration      DE          10.130.0.21        0       [0 ,0 ,0 ]
AP1281-3702e         2     AIR-CAP3702E-E-K9     bc:16:65:09:18:10  2143 MEO-Arena    DE          10.130.0.32        0       [0 ,0 ,0 ]
AP1602-3702p         2     AIR-CAP3702P-E-K9     e8:65:49:77:59:90  3061 FIL          DE          10.130.0.52        0       [0 ,0 ,0 ]
AP1611-3702p         2     AIR-CAP3702P-E-K9     e8:65:49:83:18:2c  3061 FIL          DE          10.130.0.53        0       [0 ,0 ,0 ]
AP1609-3702p         2     AIR-CAP3702P-E-K9     e8:65:49:77:59:08  2143 MEO-Arena    DE          10.130.0.54        0       [0 ,0 ,0 ]
AP1601-3702p         2     AIR-CAP3702P-E-K9     e8:65:49:8a:67:50  3061 FIL          DE          10.130.0.55        0       [0 ,0 ,0 ]
AP1604-3702p         2     AIR-CAP3702P-E-K9     e8:65:49:77:59:28  3061 FIL          DE          10.130.0.56        0       [0 ,0 ,0 ]
AP1242-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:6a:d2  3061 FIL          DE          10.130.0.58        0       [0 ,0 ,0 ]
AP1238-3702e         2     AIR-CAP3702E-E-K9     3c:08:f6:6c:f7:a0  default location  DE          10.130.0.57        0       [0 ,0 ,0 ]
AP1233-3702e         2     AIR-CAP3702E-E-K9     a8:0c:0d:ff:ef:28  2143 MEO-Arena    DE          10.130.0.59        0       [0 ,0 ,0 ]
AP1280-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:62:6e  2143 MEO-Arena    DE          10.130.0.60        0       [0 ,0 ,0 ]
AP1227-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:62:2e  3061 FIL          DE          10.130.0.61        0       [0 ,0 ,0 ]
AP1220-3702e         2     AIR-CAP3702E-E-K9     bc:16:65:09:3f:9c  2143 MEO-Arena    DE          10.130.0.62        0       [0 ,0 ,0 ]
AP1229-3702e         2     AIR-CAP3702E-E-K9     bc:16:65:09:3a:40  3061 FIL          DE          10.130.0.63        0       [0 ,0 ,0 ]
AP1244-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:63:92  2143 MEO-Arena    DE          10.130.0.64        0       [0 ,0 ,0 ]
AP1222-3702e         2     AIR-CAP3702E-E-K9     bc:16:65:09:3a:e0  2143 MEO-Arena    DE          10.130.0.65        0       [0 ,0 ,0 ]
AP1202-3702e         2     AIR-CAP3702E-E-K9     7c:ad:74:ff:67:02  3061 FIL          DE          10.130.0.66        0       [0 ,0 ,0 ]
AP7cad.74ff.d6fa     2     AIR-CAP3702E-E-K9     7c:ad:74:ff:d6:fa  default location  DE          10.130.0.68        0       [0 ,0 ,0 ]
(Cisco Controller) >'''

def read_ap(output):
    '''
    Grab all ap from "show ap summary"
    :param output:
    :return:
    '''
    ap_list = {}
    preamble=True
    for line in output.splitlines()[:-1]:
        if preamble:
            # before line '----- --- -----' etc
            row = line.split()
            if len(row) > 0:
                if len(row[0]) == row[0].count('-'):
                    # if the first cell is '-------'
                    # this builds a list that tells how many fields in a cell
                    row_format = [len(cell) for cell in row]
                    preamble=False
            continue
        # processing the table
        if len(line) == 0:
            # empty line means end of table
            break
        index = 0
        row = ['' for x in row_format]
        # iterates the line and grab cell by cell based on the row_format describer
        for cell_id, cell_len in enumerate(row_format):
            row[cell_id] = line[index:index+cell_len]
            index += 2 + cell_len
        ap_name = row[0]
        mac = row[3]
        ap_list[mac] = {'mac' : mac, 'ap_name' : ap_name}
    return ap_list

def clear_ap(ap_list):
    '''
    Build output to reset all APs
    :param ap_list:
    :return:
    '''
    commands = []
    for mac,ap in ap_list.items():
        ap = ap_list[mac]
        command = 'clear ap config {}'.format(ap['ap_name'])
        commands.append(command)
    return commands


if __name__ == '__main__':
    WlcSshShell.DEBUG = True
    wlc_session = WlcSshShell(**wlc)
    output = wlc_session.send_command('show ap summary')
    ap_list = read_ap(output)
    print(ap_list)
    commands = clear_ap(ap_list)
    wlc_session.send_commands(commands,delay=0.01,pattern=r'clear ap config will clear ap config and reboot the AP, Are you sure you want continue\? \(y/n\) ')




