'''
This will load all the AP list and import them in memory
'''
'''
IMPORTANT
The credential file has to be the google service account json file pulled from the google API
the spreadsheet must be shared with the email in the json file
in my case:
cat ../google_service_account.json  | grep @
"client_email": "399823741343-compute@developer.gserviceaccount.com",
'''

YAML_FILE = 'ap.yml'
SHEET_NAME = 'CL17 AP LIST - 17th Jan 2017'
GOOGLE_CREDENTIALS_FILE = '../google_service_account.json'
location = 'CL17'

import gspread, os, yaml, time
import csv, sys
from oauth2client.service_account import ServiceAccountCredentials

class Ap_Lookup():
    '''
    Used to import AP from google sheets / yaml.
    '''
    SCOPE = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive.file'
    ]
    SHEET_NAME = SHEET_NAME
    GOOGLE_CREDENTIALS_FILE = GOOGLE_CREDENTIALS_FILE
    AP_ATTRIBUTES = [
        'ap_name',
        'ap_mac',
        'ap_sn',
        'ap_model'
    ]

    def __init__(self):
        # dictionary with all ap_lookup
        self.ap_lookup = {}
        self.ap_list = []
        self.quantity = 0
        # google credentials
        self.google_credentials = None
        self.sheet = None

    def __len__(self):
        return self.quantity

    def add_ap(self, ap):
        '''
        Add AP in the lookup
        :param ap: dictionary item with AP details
        e.g. ap = {'ap_mac': 'aa:bb:cc:dd:ee:ff', 'ap_name': 'The_Name' , 'ap_sn': 'FNQRPFSE'}
        :return:
        '''
        self.quantity += 1
        ap_mac = ap['ap_mac']
        ap_name = ap['ap_name']
        self.ap_list.append(ap)
        self.ap_lookup[ap_mac] = ap
        self.ap_lookup[ap_name] = ap

    def del_ap(self, ap_key):
        '''
        Remove AP from the lookup
        :param ap: dictionary item with AP details
        e.g. ap = {'ap_mac': 'aa:bb:cc:dd:ee:ff', 'ap_name': 'The_Name' , 'ap_sn': 'FNQRPFSE'}
        :return:
        '''
        if ap_key in self.ap_lookup.keys():
            ap = self.ap_lookup[ap_key]
        ap_mac = ap['ap_mac']
        ap_name = ap['ap_name']
        try:
            self.ap_list.remove(ap)
            del self.ap_lookup[ap_mac]
            del self.ap_lookup[ap_name]
            self.quantity -= 1
        except:
            pass

    def open_sheets(self,spreadsheet_name=None,credentials_file=None ):
        '''
        Opens google spreadsheets
        :param spreadsheet_name:
        :param credentials_file:
        :return:
        '''
        if spreadsheet_name == None:
            spreadsheet_name = self.SHEET_NAME
        if credentials_file == None:
            credentials_file = self.GOOGLE_CREDENTIALS_FILE
        '''
        The credential file has to be the google service account json file pulled from the google API
        the spreadsheet must be shared with the email in the json file
        in my case:
        cat ../google_service_account.json  | grep @
        "client_email": "399823741343-compute@developer.gserviceaccount.com",
        '''
        # connect to the google spreadsheet
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, self.SCOPE)
        self.google_credentials = gspread.authorize(credentials)
        self.sheet = self.google_credentials.open(spreadsheet_name)


    def worksheets(self):
        '''
        List all worksheet tabs
        :return:
        '''
        if self.sheet is None:
            print('Openning default Ap_Lookup.SHEET_NAME worksheet')
            self.open_sheets()
        return self.sheet.worksheets()



    def read_worksheet(self, id, col_mac='h', col_name='i', col_process ='j', col_sn='b'):
        '''
        :param id: ordinal id of the spreadheet, e.g sencond tab = 1; fifth tab = 4
        :param mac_addr: column where the mac address is
        :param ap_name: colum with ap_names
        :param process: column that instructs to process the line, e.g. 'CL 2017 Audit'
        :return: dictionary with all APs
        '''
        if self.sheet is None:
            print('Openning default Ap_Lookup.SHEET_NAME worksheet')
            self.open_sheets()
        worksheet = self.sheet.get_worksheet(id)
        table = worksheet.get_all_values()
        col = lambda x: ord(x) - ord('a')
        col_mac = col(col_mac)
        col_name = col(col_name)
        col_process = col(col_process)
        col_sn = col(col_sn)
        #
        mac = lambda mac : ':'.join([mac.lower()[i:i+2] for i in range(0, len(mac), 2)])

        for row in table:
            # if the AP is in the inventory
            if row[col_process] == '1':
                # get mac address
                ap_mac = mac(row[col_mac])
                ap_name = row[col_name]
                ap_sn = row[col_sn]
                # config ap name <name> <MAC>
                ap = {'ap_mac': ap_mac, 'ap_name': ap_name, 'ap_sn': ap_sn}
                self.add_ap(ap)

    def read_worksheets(self,sheets):
        '''
        Import multiple sheets
        :param sheets: list of sheets id (ord number from 0 to n)
        :return:
        '''
        for id in sheets:
            self.read_worksheet(id)

    def save(self,file=YAML_FILE):
        '''

        :param file:
        :return:
        '''
        with open(file,'w+') as f:
            f.write(yaml.dump(self.ap_lookup,default_flow_style=False))

    def load(self,file=YAML_FILE):
        '''
        Load APs from yaml file
        :param file:
        :return:
        '''
        with open(YAML_FILE) as f:
            self.ap_lookup = yaml.load(f)

    def save_to_gsheets(self,spreadsheet_name=None,credentials_file=None,worksheet_name=None ):
        '''
        Opens google spreadsheets
        :param spreadsheet_name:
        :param credentials_file:
        :return:
        '''
        if spreadsheet_name == None:
            spreadsheet_name = self.SHEET_NAME
        if credentials_file == None:
            credentials_file = self.GOOGLE_CREDENTIALS_FILE
        if worksheet_name == None:
            # time.strftime prints the time with the time formatter, in this case
            # year-month-day_hour-minute
            worksheet_name = 'CL17-{}'.format(time.strftime('%Y-%m-%d_%H-%M-'))
            # add_worksheet needs rows and colums as strings
            cols = '{}'.format(len(self.AP_ATTRIBUTES))
        worksheet = self.sheet.add_worksheet(title=worksheet_name, rows='1', cols=cols)
        worksheet.insert_row(self.AP_ATTRIBUTES)
        for ap in self.ap_list:
            ap_repr = []
            for attribute in self.AP_ATTRIBUTES:
                try:
                    ap_repr.append(ap[attribute])
                except:
                    ap_repr.append('')
            worksheet.insert_row(ap_repr,2)


if __name__ == '__main__':
    aps = Ap_Lookup()
    # print(sheet.worksheets())
    aps.open_sheets()
    aps.read_worksheets(range(1,9))
    aps.save()
    aps.save_to_gsheets()




