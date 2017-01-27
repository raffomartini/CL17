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

class WlcInventory():
    '''
    Class to manage multiple WLC
    '''
    REMOTE = True

    def __init__(self, file=WLC_FILE):
        self.output_print_lock = Lock()
        self.threads = []
        self.wlcs = None
        self.ftp_settings = {}
        self.load(file)

    def load(self,file=WLC_FILE):
        '''
        Load WLC settings from yml file
        :return:
        '''
        with open(file) as f:
            data = yaml.load(f)
        self.wlcs = data['wlcs']
        ftp = data['ftp']
        '''
        {'ip': '10.100.253.13',
         'keyring_service_name': 'cl17ftp',
         'path': '/usr/home/rmartini/',
         'username': 'rmartini'}
        '''
        #---
        '''
        ftp_settings = {
                'filename': '{}-{}.txt'.format(name,time.strftime('%Y-%m-%d_%H-%M')),
                'username': 'rmartini',
                'password': keyring.get_password('cl17ftp', 'rmartini'),
                'serverip': '10.100.253.13',
                'path': '/usr/home/rmartini/'
            }
        '''
        self.ftp_settings['serverip'] = ftp['ip']
        self.ftp_settings['username'] = ftp['username']
        if 'password' in ftp:
            # not recommended
            self.ftp_settings['password'] = ftp['password']
        else:
            self.ftp_settings['password'] = keyring.get_password(ftp['keyring_service_name'],
                                                                 ftp['username'])
        self.ftp_settings['path'] = ftp['path']

    def lock_and_print(self,*args,**kwargs):
        '''
        Synchronizy threads before printing
        :param args:
        :param kwargs:
        :return:
        '''
        self.output_print_lock.acquire()
        print(*args,**kwargs,sep='\n')
        self.output_print_lock.release()

    def connect(self, wlc_name):
        '''
        :param wlc_name: name of the wlc to connect to
        :param func: dictionary for 1 wlc out of the yml file (see wlc.yml)
        :param commands: list of commands to execute
        :return:
        '''
        wlc = self.wlcs[wlc_name]
        if self.REMOTE:
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
        self.lock_and_print('-'*66, 'Connecting to {}'.format(wlc_name))
        wlc['session'] = WlcSshShell(**session_parameters)
        self.lock_and_print('-'*66, '{} connected'.format(wlc_name))


    def send_instruction(self, wlc_name, wlcsshshell_method, *args, **kwargs):
        '''

        :param wlc_name: name of the WLC
        :param wlcsshshell_method: this HAS to be called as a WlcSshShell.method
        :return:
        '''
        # used for (s|t)ftp transfer
        wlc = self.wlcs[wlc_name]
        wlc_session = wlc['session']
        self.ftp_settings['filename'] = '{}-{}.txt'.format(wlc_name,time.strftime('%Y-%m-%d_%H-%M'))
        try:
            output = wlcsshshell_method(wlc_session,*args,**kwargs)
        except TypeError:
            raise AttributeError('wlcsshshell_method must be a WlcSshShell method')
        self.lock_and_print('{}{}{}'.format(20*'-', wlc_name, 20*'-'), output)

    def close(self,wlc_name):
        '''
        Close the session on a controller
        :param wlc_name: name of the wlc
        :return:
        '''
        wlc = self.wlcs[wlc_name]
        wlc['session'].close()
        self.lock_and_print('{} session closed'.format(wlc_name), '-' * 66)

if __name__ == '__main__':
    wlcs = WlcInventory()
    wlcs.connect('WLC1')
    wlcs.send_instruction('WLC1',WlcSshShell.send_command, 'show interface summary')
    wlcs.close('WLC1')

#     for name,wlc in wlcs.items():
#         worker = Thread(target=connect_and_save, args=(name,))
#         threads.append(worker)
#         worker.setDaemon(True)
#         worker.start()
#
# for thread in threads:
#     thread.join()
# print('All Done')
#
#


