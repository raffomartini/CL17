from netmiko import *

DEBUG = True

wlc = {
        'device_type': 'cisco_wlc',
        'ip': '192.168.4.100',
        'username': 'admin',
        'password': 'C1sc0123',
        'secret': 'C1sc0123',
        'port': 22,
    }

print("Logging in to the WLC")
ssh_conn = ConnectHandler(**wlc)
output = ssh_conn.send_command_w_enter("show running-config")
print(output)
