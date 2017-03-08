'''
SSH connection to WLC controller
'''
import paramiko
import time
import re

if __name__ == '__main__':
    import keyring
    import time
    ip = '192.168.4.100'
    port = 22
    username = 'admin'
    password = 'C1sc0123'

    '''CL17'''
    username = 'rmartini'
    password = keyring.get_password('cl17ftp', 'rmartini')
    # in band
    ip = '10.130.0.1'
    port = 22
    # out of band
    ip = '10.50.140.124'
    port = 11022
    '''end of CL17'''


    credentials = {
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }

    ftp_settings = {
        'filename' : 'AIR-CT5520-K9-8-2-141-0.aes',
        'username' : 'ftpuser',
        'password' : 'C!sco123',
        'serverip' : '192.168.4.100',
        'path' : '/Users/ftpuser/tftpboot'
    }

    '''CL17'''
    ftp_settings = {
        'filename': 'WlcSshTest-{}.txt'.format(time.strftime('%Y-%m-%d_%H-%M')),
        'username': 'rmartini',
        'password': keyring.get_password('cl17ftp', 'rmartini'),
        'serverip': '10.100.253.13',
        'path': '/usr/home/rmartini/'
    }


class WlcSshShell(object):
    '''
    Class to handle WLC ssh connections
    '''
    DEBUG = False

    def check_prompt(self, output):
        '''
        Check whether the prompt is ready
        :param output:
        :return:
        '''
        pattern = '>'
        try:
            if output[-1] == pattern:
                return True
            else:
                return False
        except IndexError:
            # When the output is empty
            return False

    def __init__(self, ip, username, password, port=22, logfile=None):
        '''
		Opens SSH connection and logins to the WLC
		@:param ip: ip address, as a string
		@:param username: username
		@:param password: password
		@:param port: tcp port the WLC is listening to, default is 22
		@:param logfile: log file, warning it will override if exsisting, default is no log file
		'''
        self.logging = False
        if logfile is not None:
            # if
            self.logging = True
            # 0 means unbuffered: aka the file is updated every time I write - doesn't work because of a bug
            # 1 means line buffered: aka file updated every line
            #
            self.f = open(logfile, 'w+',1)
        self.ip = ip
        self.username = username
        self.password = password
        self.session_log = ''
        self.port = port
        connect_param = {
            'username': username,
            'password': password,
            'port' : port,
            'look_for_keys': False,
            'allow_agent': False,
        }
        # create ssh connection
        self.remote_conn = paramiko.SSHClient()
        # add remote keys (maybe not super safe, but will do for my use)
        self.remote_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.DEBUG:
            print('Opening SSH connection')
            # Opens ssh connection
        self.remote_conn.connect(self.ip, **connect_param)
        # invoke a shell session
        self.shell_session = self.remote_conn.invoke_shell()
        time.sleep(1)
        if self.DEBUG:
            print('SSH connection opened successfully')
        self.login()
        if self.DEBUG:
            print('Login successful')

    def is_alive(self):
        '''
        Check whether ssh connection is alive
        :return:
        '''
        try:
            transport = self.remote_conn.get_transport()
            transport.send_ignore()
        except EOFError as e:
            return False
        return True

    # connection is closed

    def read(self, verbose=False):
        '''
        Read output from the ssh session
        :return: output as UTF string
        '''
        output = b''
        while self.shell_session.recv_ready():
            buffer = self.shell_session.recv(10000)
            if self.DEBUG:
                print('RECEIVED: {}'.format(buffer.decode("utf-8", "ignore")))
            elif verbose:
                print(buffer.decode("utf-8", "ignore"))
            # time.sleep(0.1)
            output += buffer
            if self.logging:
                self.f.write(buffer.decode("utf-8", "ignore"))
        return output.decode("utf-8", "ignore")

    def write(self, command):
        '''
        Write a command to the WLC ssh session
        It clears the input and add a trailing newline if not present
        An empty string input will send a newline
        '''
        if self.DEBUG:
            print('SENT: {}'.format(command))
        # clean the input:
        # appends a newline if is not there and removes empty strings
        try:
            if command[-1] != '\n':
                command = '{}\n'.format(command)
        except IndexError:
            "If empty string sends a newline"
            command = '\n'
        # converts to bytes and send
        command_b = command.encode()
        self.shell_session.send(command_b)
        # time.sleep(0.1)

    def expected_prompt(self, output, expected='>'):
        '''
        Check whether the output is matching the expected prompt
        :param expected: expected pattern, default if '>'
        :param output: output to parse
        :return:
        E.g. Use this to check wether I am getting "User:" in the prompt
        '''
        pattern = r'{}\s*$'.format(expected)
        # look for pattern trailing the the output
        # breaks the output in lines and only look in the latest
        try:
            if re.search(pattern, output.splitlines()[-1], re.IGNORECASE) is not None:
                return True
            else:
                return False
        except IndexError:
            return False

    def login(self):
        '''
        logs in the WLC
        '''
        # output = ''
        while True:
            # read output
            buffer = self.read()
            # output += buffer
            # If the prompt is "User:" will send the username
            if self.expected_prompt(buffer, 'User:'):
                self.write(self.username)
            # If the prompt is "Password:" will send the pw
            if self.expected_prompt(buffer, 'Password:'):
                self.write(self.password)
            # once I have a prompt, the login is successful
            # (PROMPT)>
            elif self.expected_prompt(buffer):
                break
        # disable paging
        self.disable_paging()

    def send_command(self, command, interactive_io=[('\(y/N\)','y')], verbose=False, delay=None):
        '''
        send a command and displays the output
        :param command: command to send to the WLC, as a string
        :param interactive_io: use this to get around interactive input, this is a list of tuples expected output / input, e.g. ('\(y/N\)', 'y') to clear the "Continue? (y/N)"
        :param delay: to introduce delay, not in use
        :param verbose: prints everything, only for debug purposes
        :return: ssh session output
        '''
        command_log = ''
        # If the channel is not ready, read it
        if not (self.shell_session.send_ready()):
            command_log = self.read(verbose)
        self.write(command)
        if delay is not None:
            time.sleep(delay)
        while True:
            output = self.read(verbose)
            command_log += output
            # Checks if prompt has returned
            if self.expected_prompt(output):
                break
            # Take care of 'Press Enter to continue'
            elif self.expected_prompt(output, 'Press Enter to continue.*'):
                # if Press Enter to continue found, send newline
                self.write('\n')
            for io in interactive_io:
                # e.g. io = (r'(y/N)', 'y')
                if self.expected_prompt(output, io[0]):
                    self.write(io[1])
        self.session_log += command_log
        return command_log

    def send_commands(self, command_list, verbose=False, delay=None):
        '''
        Send a sequence of commands, one by one
        :param command_list: list of commands
        :param verbose: only for debugging, default is False
        :param delay: introduces delay, not needed
        :return:
        '''
        command_log = []
        if type(command_list) is str:
            command_list = command_list.splitlines()
        for command in command_list:
            output = self.send_command(command, verbose=verbose, delay=delay)
            command_log.append(output)
        return command_log

    def disable_paging(self):
        '''
        Disable paging on the WLC
        :return:
        '''
        self.send_command('config paging disable')

    def load_image(self, username, password, filename, serverip, path, transfer_proto='ftp', datatype='code'):
        '''
        Download an image on the controller
        :param transfer_proto:
        :param username:
        :param password:
        :return:
        '''
        if transfer_proto not in ('ftp', 'tftp', 'sftp'):
            raise AttributeError('transfer_proto has to be ftp, tftp, sftp')
        commands = '''\
transfer download filename {filename}
transfer download mode {transfer_proto}
transfer download username {username}
transfer download password {password}
transfer download serverip {serverip}
transfer download path {path}
transfer download datatype {datatype}
transfer download start\
'''.format(filename=filename,
           transfer_proto=transfer_proto,
           username=username,
           password=password,
           serverip=serverip,
           path=path,
           datatype=datatype).splitlines()
        if TROUBLESHOOT:
            commands = ['transfer download start']
        output = self.send_commands(commands)

    def export_config(self, username, password, filename, serverip, path, transfer_proto='ftp', datatype='config'):
        '''
        Save config to the ftp server
        :param transfer_proto:
        :param username:
        :param password:
        :return:
        '''
        if transfer_proto not in ('ftp', 'tftp', 'sftp'):
            raise AttributeError('transfer_proto has to be ftp, tftp, sftp')
        commands = '''\
transfer upload filename {filename}
transfer upload mode {transfer_proto}
transfer upload username {username}
transfer upload password {password}
transfer upload serverip {serverip}
transfer upload path {path}
transfer upload datatype {datatype}
transfer upload start\
'''.format(filename=filename,
           transfer_proto=transfer_proto,
           username=username,
           password=password,
           serverip=serverip,
           path=path,
           datatype=datatype).splitlines()
        output = self.send_commands(commands)

    def show_run(self, file=None):
        '''
        Returns running-config and saves it to a file(optional)
        :return:
        '''
        output = self.send_command('show run-config')
        if file is not None:
            with open(file, 'w') as f:
                f.write(output)
        return output

    def show_run_commands(self, file=None):
        '''
        Returns running-config and saves it to a file(optional)
        :return:
        '''
        output = self.send_command('show run-config commands')
        if file is not None:
            with open(file, 'w') as f:
                f.write(output)
        return output

    def show_run_startup(self, file=None):
        '''
        Returns running-config and saves it to a file(optional)
        :return:
        '''
        output = self.send_command('show run-config startup-commands')
        if file is not None:
            with open(file, 'w') as f:
                f.write(output)
        return output

    def save_config(self):
        '''
        Save controller config
        :return:
        '''
        self.send_command('save config')

    def close(self):
        '''
        Terminate the shell session
        :return:
        '''
        self.remote_conn.close()


if __name__ == '__main__':
    WlcSshShell.DEBUG = True

    wlc_session = WlcSshShell(**credentials, logfile='test_logging')
    # output = wlc_session.send_command('show run-config')
    # wlc_session.close()
    # output = wlc_session.show_run_commands('/Users/rmartini/Desktop/wlc01-c')
    # wlc_session.load_image(**ftp_settings)
    #output = wlc_session.show_run_startup('/Users/rmartini/Desktop/startup_config')
    # output = wlc_session.show_run_commands('/Users/rmartini/Desktop/wlc01-c')
    # output = wlc_session.send_command('show sysinfo')
    # output = wlc_session.send_command('show sysinfo')
    # output = wlc_session.show_run('show-run.txt')

#
# if DEBUG:
# 	print ('End of show run')
# else:
# 	exit(0)
#
#
