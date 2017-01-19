'''
TO start ftp server
sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist
to stop it use the unload version
sudo -s launchctl unload -w /System/Library/LaunchDaemons/ftp.plist

transfer download filename AIR-CT5500-K9-8-2-141-0.aes
transfer download mode ftp
transfer download username rmartini
transfer download password (RmaCL17)
transfer download serverip 10.100.253.13
transfer download path /usr/home/rmartini
transfer download datatype code
transfer download start
y
'''

from paramiko_wlc import WlcSSH

controllers = [

]

wlc = {
    'ip': ip,
    'username': username,
    'password': password,
}

ftp_settings = {
    'filename' : 'AIR-CT5520-K9-8-2-141-0.aes',
    'username' : 'ftpuser',
    'password' : 'C!sco123',
    'serverip' : '192.168.4.100',
    'path' : '/Users/ftpuser/tftpboot'
}


credentials = {
    'ip': ip,
    'username': username,
    'password': password,
}

if __name__ == '__main__':
    WlcSSH.DEBUG = True
    wlc_session = WlcSSH(**credentials)
    # output = wlc_session.send_command('show sysinfo')
    commands = '''\
transfer download filename AIR-CT5520-K9-8-2-141-0.aes
transfer download mode ftp
transfer download username rmartini
transfer download password (Rma07cisco)
transfer download serverip 10.127.247.104
transfer download path /Users/rmartini/tftpboot
transfer download datatype code
transfer download start
'''.splitlines()
    output = wlc_session.send_commands(commands)
    output = wlc_session.send_command('y')
