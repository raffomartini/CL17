from wlcsshshell import WlcSshShell
import time
import keyring
import yaml
from threading import Thread, Lock


WlcSshShell.DEBUG = False
WLC_FILE = 'wlc.yml'
REMOTE = True

ip = "10.50.140.124"
# wlc_username = 'cisco'
# wlc_password = 'C1sco123'
wlc_username = 'rmartini'
wlc_password = keyring.get_password('cl17ftp','rmartini')
remote_ip = "10.50.140.124"

# wlc3 = {
#     'ip': ip,
#     'username': username,
#     'password': wlc_password,
#     'port': port
# }

output_print_lock = Lock()
threads = []


# def init()

with open(WLC_FILE) as f:
    wlcs = yaml.load(f)

def connect_and_save(wlc):
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
    filename = 'config/{}-{}.txt'.format(name, time.strftime('%Y-%m-%d_%H-%M'))
    # improvement: try to use decorators
    output_print_lock.acquire()
    print('-'*66)
    print('Connecting to {}'.format(name))
    output_print_lock.release()
    wlc_session = WlcSshShell(**session_parameters)
    output = wlc_session.show_run_commands(filename)
    wlc_session.close()
    output_print_lock.acquire()
    print('{} DONE'.format(name))
    print('Config saved on {}'.format(filename))
    print('-' * 66)
    output_print_lock.release()

if __name__ == '__main__':
    for name,wlc in wlcs.items():
        worker = Thread(target=connect_and_save, args=(wlc,))
        threads.append(worker)
        worker.setDaemon(True)
        worker.start()

for thread in threads:
    thread.join()
print('All Done')




