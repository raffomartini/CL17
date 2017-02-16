from wlcsshshell import WlcSshShell
import time
import keyring
import yaml
from threading import Thread, Lock

commands = '''\
config wlan delete 1
config snmp v3user create CLEUR rw hmacsha des C1tyCu6eB3rl1n C1tyCu6eB3rl1n
'''.splitlines()


WlcSshShell.DEBUG = False
WLC_FILE = 'wlc.yml'
REMOTE = False
CONFIG_FILE = '{}-ciscowlc-confg'
CONFIG_FILE_PATH = 'cl17/CFG/'

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
    '''
    This is a decorator, it is used to process inclusion list and exclusion before calling any method that will precess multiple controllers
    :param func: doesn't matter too much, this is how a decorator works
    :return:
    '''
    def _check_include_exclude(self, include_list=None, *args, exclude_list=None, **kwargs):
        '''
        Inner function of the decorator, this is where magic happens
        Note the order of the paramenters: first mandatory ones, then unnamed args, then named parameters and finally kwargs.
        :param self: because this will decorate a method, the first parameter is the self paramater, aka the object the method is called on
        :param include_list: list of wlc names to include
        :param *args: to make is as generic as possible
        :param exclude_list: list of wlc names to include
        :param kwargs: to make it as generic as possible
        :return: doesn't matter, this is how decorators work
        '''
        if include_list is None:
            include_list = list(self.wlcs.keys())
        else:
            include_list = [wlc for wlc in include_list if wlc in self.wlcs]
        if exclude_list is not None:
            include_list = [wlc_name for wlc_name in include_list if wlc_name not in exclude_list]
        # all methods are defined with include_list only, the decorator process both include and exclude list
        return func(self, include_list, *args, **kwargs)
    return _check_include_exclude

class WlcInventory():
    '''
    Class to manage multiple WLC
    '''
    REMOTE = REMOTE

    def __init__(self, file=WLC_FILE):
        '''
        Initialise a bunch of data structures, some I am not even using.
        :param file: yaml file containing all WLCs, example below
        cat << EOF
wlcs:
  WLC1:
    ip: 10.130.0.1
    name: WLC1
    port: 11022

  WLC3:
    ip: 10.130.0.3
    name: WLCn
    port: 13022

ftp:
  ip: 10.100.253.13
  path: /usr/home/rmartini/
  username: rmartini
  keyring_service_name: cl17ftp
        '''
        # lock used to printout without making a mess
        self.output_print_lock = Lock()
        # list of threads
        self.threads = []
        # dict with all WLCs, loaded from the yaml file
        self.wlcs = {}
        # dict with the ftp parameters, loaded form yaml file
        self.ftp_settings = {}
        # load stuff from the yaml file
        self.load(file)
        # list of wlc with an open session
        self.open_list = []

    def load(self,file=WLC_FILE):
        '''
        Load WLC settings from yaml file
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
        Synchronizy threads before printing, used to avoid multiple thread to write together on the output and make a mess
        :param args:
        :param kwargs:
        :return:
        '''
        self.output_print_lock.acquire()
        print(*args,**kwargs,sep='\n')
        self.output_print_lock.release()

    def connect(self, wlc_name, logging=True):
        '''
        Opens a connection to a wlc
        :param wlc_name: name of the wlc to connect to
        :return:
        '''
        wlc = self.wlcs[wlc_name]
        # this is a specific switch for the OOO band connection used during staging
        if self.REMOTE:
            ip = remote_ip
            port = wlc['port']
        else:
            ip = wlc['ip']
            port = 22
        session_parameters = {
            'ip': ip,
            'username': wlc_username,
            'password': wlc_password,
            'port': port
        }
        self.lock_and_print('-'*66, 'Connecting to {}'.format(wlc_name))
        if logging:
            # adds the log file to the session parameters, and add timestamp
            session_parameters['logfile'] = 'logs/{}-{}.txt'.format(time.strftime('%Y-%m-%d_%H-%M-%S'),wlc_name)
        try:
            wlc['session'] = WlcSshShell(**session_parameters)
            tail = None
            if logging:
                tail = 'To see live logs, tail -f {}'.format(session_parameters['logfile'])
            self.lock_and_print('-'*66, '{} connected'.format(wlc_name),tail)
            self.open_list.append(wlc_name)
        except TimeoutError:
            self.lock_and_print('{} connection timed out, it is probably not available...'.format(wlc_name))

    def read_config(self,wlc_name):
        '''
        Method that loads the config to be sent form a file.
        :param wlc_name:
        :return:
        '''
        # improvement: add the config_file definition in yaml file on a global / per WLC basis
        # improvement: add the config_path definition in yaml
        config_file = CONFIG_FILE_PATH + CONFIG_FILE.format(wlc_name)
        with open(config_file) as f:
            # return the commands as a list, 1 command per item
            return f.readlines()

    def send_instruction(self, wlc_name, *args, wlcsshshell_method=WlcSshShell.send_commands, commands_from_file=False, **kwargs ):
        '''
        Send an instruction to wlc_name, the intruction is a method defined in WlcSshShell
        :param wlc_name: name of the WLC
        :param wlcsshshell_method: this HAS to be called as a WlcSshShell.method
        :param commands_from_file: If true, it will load the config from file and send the commands
        :return:
        '''
        # used for (s|t)ftp transfer
        if commands_from_file is True:
            # flag to load the config from a file
            commands = self.read_config(wlc_name)
            # add command_list to head of args
            args = [commands] + list(args)
        wlc = self.wlcs[wlc_name]
        try:
            wlc_session = wlc['session']
        except KeyError:
            return
        self.ftp_settings['filename'] = '{}-{}.txt'.format(wlc_name,time.strftime('%Y-%m-%d_%H-%M'))
        try:
            output = wlcsshshell_method(wlc_session,*args,**kwargs)
        except TypeError:
            raise AttributeError('wlcsshshell_method must be a WlcSshShell method')
        if type(output) is tuple:
            # case single command being sent using send_commands
            self.lock_and_print('{}{}{}'.format(20*'-', wlc_name, 20*'-'), output[1])
        elif type(output) is list:
            # case multiple commands being sent using send_commands
            self.lock_and_print('{}{}{}'.format(20*'-', wlc_name, 20*'-'), *[line[1] for line in output])
        elif type(output) is str:
            # case send_command in use
            self.lock_and_print('{}{}{}'.format(20 * '-', wlc_name, 20 * '-'), output)
        return output

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

    def close_all(self):
        '''
        Close all open connections
        :return:
        '''
        for wlc_name in self.open_list:
            self.close(wlc_name)
            print('{} session closed'.format(wlc_name))

    def spawn_threads(self, target, run_list, *args, **kwargs):
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
            worker = Thread(target=target, args=(wlc_name, *args), kwargs=kwargs, daemon=True)
            self.threads.append(worker)
            # worker.setDaemon(True)
            worker.start()

        for thread in self.threads:
            thread.join()

    @check_include_exclude
    def connect_to_many(self, include_list, logging=True):
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
        self.spawn_threads(self.connect, include_list, logging)

    @check_include_exclude
    def send_command_to_many(self, include_list, *args):
        '''
        Use WlcSshShell.send_commands to send multiple commands to 1 or more WLC in parallel
        :param include_list: list of wlc names to connect to
        :param commands: list of commands to send, if no command is passed, the command is going to be loaded from file
        '''
        load_commands = False
        if len(args) == 0:
            # no commands passed
            load_commands = True
        # this will call the method to send_instructions as threaded
        self.spawn_threads(self.send_instruction, include_list, *args, commands_from_file=load_commands )

    def save_all(self):
        '''
        Save all controller config
        :return:
        '''
        self.spawn_threads(self.send_instruction, self.open_list, wlcsshshell_method=WlcSshShell.save_config)


if __name__ == '__main__':
    wlcs = WlcInventory()
    # wlcs.connect('WLC9')
    wlcs.connect_to_many()
    # wlcs.save_all()
    # wlcs.connect_to_many(exclude_list=['WLC9'])
    # wlcs.close_all()
    # wlcs.connect_to_many(['WLC1'])
    # wlcs.send_instruction('WLC1','show interface summary', wlcsshshell_method=WlcSshShell.send_command)
    # wlcs.send_instruction('WLC1', ['show interface summary', 'show sysinfo'])
    # wlcs.send_instruction('WLC1', commands)
    # working
    # wlcs.send_instruction('WLC1',commands_from_file=True)
    # wlcs.send_command_to_many(['WLC1'])
    # wlcs.send_command_to_many(['WLC1'])
    wlcs.send_command_to_many(None, ['config ap mgmtuser add username ramon password wZUb3W6mwUXrEgbR secret wZUb3W6mwUXrEgbR all'])
    wlcs.save_all()
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


