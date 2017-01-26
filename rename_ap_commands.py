'''
config ap name <name> <MAC>
'''

filename = 'ap_list.csv'
location = 'CL17'
credendiatls = '../google_service_account.json'

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive.file'
]

import gspread, os
import csv, sys
from oauth2client.service_account import ServiceAccountCredentials


def rename_ap_commands(table):
    '''
    Builds the cli commands to rename the APs
    '''
    commands = []
    try:
        for row in table:
            # if CL 2017 Audit is ticked
            if row[9] == '1':
                # get mac address
                mac = row[2].lower()
                # convert mac address
                newmac = '{}:{}:{}:{}:{}:{}'.format(mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])
                # config ap name <name> <MAC>
                commands.append('config ap name {} {}\n'.format(row[8], newmac))
                commands.append('config ap location {} {}\n'.format(location, newmac))
    except:
        pass
    return commands


#connect to the google spreadsheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(credendiatls, SCOPE)
gc = gspread.authorize(credentials)

#note: you have to share this with the email in the json file
# in my case
'''
cat ../google_service_account.json  | grep @
  "client_email": "399823741343-compute@developer.gserviceaccount.com",
'''
sh = gc.open('CL17 AP LIST - 17th Jan 2017')
# list worksheets
# ws_list = sh.worksheets()

# interested in spreadsheets 1 to 7
commands = []
for id in range(8,9):
    worksheet = sh.get_worksheet(id)
    table = worksheet.get_all_values()
    commands += rename_ap_commands(table)

    with open('command_rename_ap','a+') as f:
        f.writelines(commands)

# with open(filename, newline='') as f:
#     table = csv.reader(f)
#     rename_ap_commands(table=)
#     with open('commands','a+') as f:
#         f.writelines(commands)
