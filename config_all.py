from wlcsshshell import WlcSshShell
import time
import keyring
import yaml
from threading import Thread, Lock


WlcSshShell.DEBUG = True
WLC_FILE = 'wlc.yml'
REMOTE = True

ip = "10.50.140.124"
wlc_username = 'cisco'
wlc_password = 'C1sco123'
# wlc_username = 'rmartini'
# wlc_password = keyring.get_password('cl17ftp','rmartini')
remote_ip = "10.50.140.124"

# wlc3 = {
#     'ip': ip,
#     'username': username,
#     'password': wlc_password,
#     'port': port
# }

commands = '''\
config radius auth add 1 10.100.253.7 1812 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config radius acct add 1 10.100.253.7 1812 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs auth add 1 10.100.253.7 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs acct add 1 10.100.253.7 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs athr add 1 10.100.253.7 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config radius auth add 2 10.100.253.107 1812 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config radius acct add 2 10.100.253.107 1812 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs auth add 2 10.100.253.107 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs acct add 2 10.100.253.107 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config tacacs athr add 2 10.100.253.107 49 ascii Ksl33mJwfeFOZ4iPOGuYSPIz
config aaa auth mgmt  local tacacs
'''.splitlines()

output_print_lock = Lock()
threads = []


# def init()

with open(WLC_FILE) as f:
    wlcs = yaml.load(f)

def connect_and_send(wlc, commands):
    '''
    :param wlc: dictionary for 1 wlc out of the yml file (see wlc.yml)
    :param commands: list of commands to execute
    :return:
    '''
    name = wlc['name']
    if REMOTE:
        ip = remote_ip
        port = wlc['port']
    else:
        port = 22
    session_parameters = {
        'ip': ip,
        'username': wlc_username,
        'password': wlc_password,
        'port': port
    }
    # improvement: try to use decorators
    output_print_lock.acquire()
    print('-'*66)
    print('Connecting to {}'.format(name))
    output_print_lock.release()
    wlc_session = WlcSshShell(**session_parameters)
    wlc_session.send_commands(commands)
    wlc_session.close()
    output_print_lock.acquire()
    print('{} DONE'.format(name))
    print('-' * 66)
    output_print_lock.release()


if __name__ == '__main__':
    for name,wlc in wlcs.items():
        output_print_lock = Lock()
        threads = []
        worker = Thread(target=connect_and_send(), args=(wlc,commands))
        threads.append(worker)
        worker.setDaemon(True)
        worker.start()

for thread in threads:
    thread.join()
print('All Done')




