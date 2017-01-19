from paramiko_wlc import WlcSSH

DEBUG = True

## Change these
ip = '192.168.4.100'
username = 'admin'
password = 'C1sc0123'
config_file = 'show-run.txt'

credentials = {
	'ip': ip,
	'username': username,
	'password': password,
}

DEBUG = False

wlc_session = WlcSSH(**credentials)
print(
	'''SSH session opened, I am now collecting the configuration,
	 this might take a while..'''
      )
output = wlc_session.send_command('show run-config',True)

with open(config_file, 'w') as f:
	f.write(output)

print('Config saved successfully')
exit(0)
