from wlcsshshell import WlcSshShell
import time
import keyring

WlcSshShell.DEBUG = True

ip = "10.50.140.124"
username = 'cisco'
wlc_password = 'C1sco123'
port = 13022

wlc3 = {
    'ip': ip,
    'username': username,
    'password': wlc_password,
    'port': port
}

ftp_settings = {
    # add timestamp
    'filename' : 'wlc03-{}.txt'.format(time.strftime('%Y-%m-%d_%H-%M')),
    'username' : 'rmartini',
    # getting it from keychain
    'password' : keyring.get_password('cl17ftp','rmartini'),
    # 'serverip' : '192.168.4.100',
    'serverip' : '10.100.253.13',
    'path' : '/usr/home/rmartini/'
}

if __name__ == '__main__':
    wlc_session = WlcSshShell(**wlc3)
    wlc_session.save_config(**ftp_settings)

