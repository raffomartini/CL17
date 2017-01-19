'''
SSH connection to WLC controller
'''
import paramiko
import time
import re

TROUBLESHOOT = True

if __name__ == '__main__':
    # ip = '192.168.4.100'
    ip = "10.130.0.1"
    username = 'admin'
    password = 'C1sc0123'
    username = 'cisco'
    password = 'C1sco123'


    credentials = {
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


class WlcSSH(object):
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

    def __init__(self, ip, username, password):
        '''
		Opens SSH connection and logins to the WLC
		'''
        self.ip = ip
        self.username = username
        self.password = password
        self.session_log = ''
        connect_param = {
            'username': username,
            'password': password,
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
        self.channel = self.remote_conn.invoke_shell()
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
        while self.channel.recv_ready():
            buffer = self.channel.recv(10000)
            if self.DEBUG:
                print('RECEIVED: {}'.format(buffer.decode()))
            elif verbose:
                print(buffer.decode())
            # time.sleep(0.1)
            output += buffer
        return output.decode()

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
        self.channel.send(command_b)
        # time.sleep(0.1)

    def send_command(self, command, verbose=False, pattern=None, delay=None):
        '''
        send a command and displays the output
        :param command
        :return: ssh session output
        '''
        command_log = ''
        # If the channel is not ready, read it
        if not (self.channel.send_ready()):
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
            elif pattern is not None:
                try:
                    if self.expected_prompt(output.splitlines()[-1], pattern):
                    # print('Warning, I''m sending a command with a warning')
                        self.write('y')
                except:
                    pass
        self.session_log += command_log
        return command_log

    def send_commands(self, command_list, verbose=False, pattern=None, delay = None):
        '''
        Send a sequence of commands, one by one
        :param command_list:
        :param verbose:
        :return:
        '''
        command_log = []
        for command in command_list:
            output = self.send_command(command, verbose, pattern, delay)
            command_log.append((command,output))
        return command_log

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
            if re.search(pattern, output.splitlines()[-1]) is not None:
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

    # if self.DEBUG:
    # 	print(output)

    def disable_paging(self):
        '''
        Disable paging on the WLC
        :return:
        '''
        self.send_command('config paging disable')

    def load_image(self, username, password, filename, serverip, path, transfer_proto='ftp'):
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
transfer download datatype code
transfer download start\
'''.format(filename=filename,
           transfer_proto=transfer_proto,
           username=username,
           password=password,
           serverip=serverip,
           path=path).splitlines()
        if TROUBLESHOOT:
            commands = ['transfer download start']
        output = self.send_commands(commands, pattern=r'Are you sure you want to start\? \(y/N\)')

    def save_config(self, username, password, filename, serverip, path, transfer_proto='ftp'):
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
transfer download datatype code
transfer download start\
'''.format(filename=filename,
           transfer_proto=transfer_proto,
           username=username,
           password=password,
           serverip=serverip,
           path=path).splitlines()
        if TROUBLESHOOT:
            commands = ['transfer download start']
        output = self.send_commands(commands, pattern=r'Are you sure you want to start\? \(y/N\)')

    def show_run(self, file=None):
        '''
        Returns running-config and saves it to a file(optional)
        :return:
        '''
        output = self.send_command('show running-config')
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


if __name__ == '__main__':
    WlcSSH.DEBUG = True

    wlc_session = WlcSSH(**credentials)

    # wlc_session.load_image(**ftp_settings)
    output = wlc_session.show_run_startup('/Users/rmartini/Desktop/wlc01')
    output = wlc_session.show_run_commands('/Users/rmartini/Desktop/wlc01-c')
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
