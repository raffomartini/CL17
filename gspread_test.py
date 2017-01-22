import gspread, os
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive.file'
]
credendiatls = '../google_service_account.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(credendiatls, SCOPE)
gc = gspread.authorize(credentials)

#note: you have to share this with the email in the json file
# in my case
'''
cat ../google_service_account.json  | grep @
  "client_email": "399823741343-compute@developer.gserviceaccount.com",
'''
# sh = gc.open('CL17 AP LIST - 17th Jan 2017')
# ws_list = sh.worksheets()
#
# worksheet = sh.worksheet('3802e')
# table = worksheet.get_all_values()

def save_table_to_worksheet(worksheet, table):
    '''
    Function to save a table to a worksheet
    :param worksheet: open worksheet
    :param table:
    :return:
    '''
    num_rows = len(table)
    num_cols = len(table[0])
    # this returns the whorksheet coordinates give the nomeric coordinates, e.g 1,1 -> A1
    last_cell = gspread.utils.rowcol_to_a1(num_rows,num_cols)
    range = 'A1:{}'.format(last_cell)
    cell_list = worksheet.range(range)
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




sh = gc.open('Test')
ws_list = sh.worksheets()
worksheet = sh.add_worksheet(title="Another worksheet", rows='100', cols='100')
table = [[ i+j*10 for i in range(10)] for j in range(5)]
save_table_to_worksheet(worksheet,table)




# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1LsooTZ92sL47qjFB9hwcW2WxiHrregLMjf8YZnUvLKo/edit#gid=840924667')
# worksheet_list = sh.worksheets()