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

def check_include_exclude(func):
    def _check_include_exclude(self, include_list=None, exclude_list=None, *args, **kwargs):
        if include_list is None:
            include_list = list(self.wlcs.keys())
        else:
            include_list = [wlc for wlc in include_list if wlc in self.wlcs]
        if exclude_list is not None:
            include_list = [wlc_name for wlc_name in include_list if wlc_name not in exclude_list]
        return func(self, include_list, *args, **kwargs)
    return _check_include_exclude

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
        self.threads = []
        self.open_list = []

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
        try:
            wlc['session'] = WlcSshShell(**session_parameters)
            self.lock_and_print('-'*66, '{} connected'.format(wlc_name))
            self.open_list.append(wlc_name)
        except TimeoutError:
            print('{} connection timed out, it is probably not available...'.format(wlc_name))

    def send_instruction(self, wlc_name, wlcsshshell_method=WlcSshShell.send_commands, *args, **kwargs):
        '''
        Send an instruction to wlc_name, the intruction is a method defined in WlcSshShell
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

    def close(self, wlc_name):
        '''
        Close the session on a controller
        :param wlc_name: name of the wlc
        :return:
        '''
        wlc = self.wlcs[wlc_name]
        wlc['session'].close()
        self.open_list.remove(wlc_name)
        self.lock_and_print('{} session closed'.format(wlc_name), '-' * 66)

    def spawn_threads(self, target, run_list, *args):
        '''
        Run a command (or set of commands) to multiple wlc
        :param run_list:
        :param *args: will be passed to the threaded method
        :param *kwargs: will be passed to the threaded method
        :return:
        '''
        for wlc_name in run_list:
            # this works:
            # worker = Thread(target=WlcInventory.connect, args=(wlcs, 'WLC1'), daemon=True)
            worker = Thread(target=target, args=(wlc_name, *args), daemon=True)
            self.threads.append(worker)
            # worker.setDaemon(True)
            worker.start()

        for thread in self.threads:
            thread.join()

    @check_include_exclude
    def connect_to_many(self, include_list):
        '''
        Open connections to more than one WLCs
        :param include_list: list of wlc_names to include
        :param exclude_list: list of wlc_names to exclude
        Note:
        If both include list and exclude list are present,
        -> it will remove the items in the exclude_list from the include list
        If include_list is None,
        -> it will include ALL WLC in the inventory
        :return:
        '''
        self.spawn_threads(self.connect, include_list)

    # def connect_to_many(self, run_list=None):
    #     '''
    #     Open connections to more than one WLCs
    #     :param include_list: list of wlc_names to include
    #     :param exclude_list: list of wlc_names to exclude
    #     Note:
    #     If both include list and exclude list are present,
    #     -> it will remove the items in the exclude_list from the include list
    #     If include_list is None,
    #     -> it will include ALL WLC in the inventory
    #     :return:
    #     '''
    #     run_list = []
    #     if include_list is not None:
    #         run_list = include_list
    #     else:
    #         run_list = list(self.wlcs.keys())
    #     if exclude_list is not None:
    #         run_list = [wlc_name for wlc_name in run_list if wlc_name not in exclude_list]
    #     self.spawn_threads(self.connect, run_list)


    @check_include_exclude
    def print_run_list(self,include_list=None, exclude_list=None):
        '''
        Dummy function to check parameters
        :param include_list:
        :param exclude_list:
        :return:
        '''
        print(include_list)

    # @self.include_eclude()
    # def send_command_to_many(self):




if __name__ == '__main__':
    wlcs = WlcInventory()
    # wlcs.print_run_list(include_list=['WLC1','WLC3'],exclude_list=['WLC3'] )
    wlcs.connect_to_many()
    # wlcs.send_command_to_many('config snmp v3user create CLEUR rw hmacsha des C1tyCu6eB3rl1n C1tyCu6eB3rl1n ')
    # wlcs.connect('WLC1')
    # wlcs.send_instruction('WLC1',WlcSshShell.send_command, 'show interface summary')
    # wlcs.close('WLC1')

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


