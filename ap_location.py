'''
This will load all the AP list and import them in memory
Example of use:

'''
import gspread, os, yaml, time
import csv, sys
from oauth2client.service_account import ServiceAccountCredentials
from WlcInventory import WlcInventory

YAML_FILE = 'ap_to_ap_group.yml'
SHEET_NAME = 'EMEAR Wireless Inventory'
GOOGLE_CREDENTIALS_FILE = '../google_service_account.json'
COL_NAM = 'a'
COL_LOCATION = 'b'
LOCATION_LOOKUP = 'location.yml'
LOCATION_LOOKUP_DIFF = 'location_diff.yml'
WS_NAME = 'Location of APs'
'''
locations = set([aps.ap_lookup[key]['ap_location'] for key in aps.ap_lookup.keys() ])
f = open('location_temp.yml','w')
yaml.dump(locations, f, default_flow_style=False)
'''

location = 'CL17'

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
        'ap_location',
        'ap_group'
    ]

    def __init__(self):
        # dictionary with all ap_lookup
        self.ap_lookup = {}
        self.ap_list = []
        self.quantity = 0
        # google credentials
        self.google_credentials = None
        self.sheet = None
        self.location_lookup = yaml.load(open(LOCATION_LOOKUP))
        self.missing_location = False

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
        ap_name = ap['ap_name']
        ap_location = ap['ap_location']
        self.ap_lookup[ap_name] = ap
        try:
            ap['ap_group'] = self.location_lookup[ap_location]
        except:
            self.missing_location = True


    def del_ap(self, ap_key):
        '''
        Remove AP from the lookup
        :param ap: dictionary item with AP details
        e.g. ap = {'ap_mac': 'aa:bb:cc:dd:ee:ff', 'ap_name': 'The_Name' , 'ap_sn': 'FNQRPFSE'}
        :return:
        '''
        if ap_key in self.ap_lookup.keys():
            ap = self.ap_lookup[ap_key]
        ap_name = ap['ap_name']
        try:
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

    def read_worksheet(self, ws_name=WS_NAME, col_name=COL_NAM, col_location=COL_LOCATION):
        '''
        :param id: ordinal id of the spreadheet, e.g sencond tab = 1; fifth tab = 4
        :param col_mac: column where the mac address is
        :param col_name: colum with ap_names
        :param col_inv: column that instructs to process the line, e.g. 'CL 2017 Audit'
        :return: dictionary with all APs
        '''
        if self.sheet is None:
            print('Openning default Ap_Lookup.SHEET_NAME worksheet')
            self.open_sheets()
        worksheet = self.sheet.worksheet(ws_name)
        table = worksheet.get_all_values()
        col = lambda x: ord(x) - ord('a')
        col_name = col(col_name)
        col_location = col(col_location)
        #
        for row in table[1:]:
            # if the AP is in the inventory
            # get mac address
            ap_name = row[col_name]
            ap_location = row[col_location]
            # config ap name <name> <MAC>
            ap = {'ap_name': ap_name, 'ap_location': ap_location}
            self.add_ap(ap)
        if self.missing_location:
            diff = self.lookup_diff()
            print('New locations added, fix {filename} lookip file: {diff}'.format(diff=diff, filename=LOCATION_LOOKUP))

    def read_worksheets(self,sheets, cols=None):
        """
        Import multiple sheets
        :param sheets: list of sheets id (ord number from 0 to n)
        :return:
        """
        if cols is None:
            cols = {
                'col_name' : COL_NAM,
                'col_location' : COL_LOCATION
            }
            
        for id in sheets:
            self.read_worksheet(id,**cols)

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

    def save_table_to_worksheet(self,worksheet, table):
        '''
        Function to save a table to a worksheet, missing method of gspread!!!
        :param worksheet: open worksheet
        :param table:
        :return:
        '''
        num_rows = len(table)
        num_cols = len(table[0])
        # this returns the whorksheet coordinates give the nomeric coordinates, e.g 1,1 -> A1
        last_cell = gspread.utils.rowcol_to_a1(num_rows, num_cols)
        cell_range = 'A1:{}'.format(last_cell)
        cell_list = worksheet.range(cell_range)
        '''
        Because the table is a list of lists and I have to put that into a list of cells,
        I am going through the table with a double loop and using an iterator to go through the list as I go.
        '''
        # iterator for the worksheet list of cells
        remote_iter = iter(cell_list)
        # nested loop to go through the table
        for row in table:
            for cell in row:
                next(remote_iter).value = cell
        worksheet.update_cells(cell_list)

    def ap_table(self):
        '''
        Creates a list of list representation of the AP in the lookup,
        ready for csv or gspread export
        :return: ap_table, list of list representation of the APs
        '''
        # header
        table = [self.AP_ATTRIBUTES]
        for ap in self.ap_list:
            ap_repr = []
            for attribute in self.AP_ATTRIBUTES:
                try:
                    ap_repr.append(ap[attribute])
                except:
                    ap_repr.append('')
            table.append(ap_repr)
        return table

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
        rows = '{}'.format(self.quantity + 1)
        worksheet = self.sheet.add_worksheet(title=worksheet_name, rows=rows, cols=cols)
        ap_table = self.ap_table()
        self.save_table_to_worksheet(worksheet,ap_table)

    def __repr__(self):
        return '<ap_lookup, {} aps in memory>'.format(self.quantity)

    def __getitem__(self, item):
        # ap_lookup['mac'] -> ap_dictionary
        return self.ap_lookup[item]

    # def __setitem__(self, key, value):
    #     self.add_ap(ap)
    def __delitem__(self, key):
        # del ap_lookup[key] -> delete ap from lookup
        self.del_ap(key)

    def lookup_diff(self):
        """
        Check locations not in lookup
        :return: diff
        """
        locations = set([self.ap_lookup[key]['ap_location'] for key in self.ap_lookup.keys()])
        f = open(LOCATION_LOOKUP_DIFF, 'w')
        diff = locations - set(self.location_lookup)
        yaml.dump(diff, f, default_flow_style=False)
        return diff

if __name__ == '__main__':
    aps = Ap_Lookup()
    aps.open_sheets()
    aps.read_worksheet()
    aps.save()
    wlcs = WlcInventory()
    wlcs.connect_to_many()




