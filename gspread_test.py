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
sh = gc.open('CL17 AP LIST - 17th Jan 2017')
ws_list = sh.worksheets()

worksheet = sh.worksheet('3802e')
table = worksheet.get_all_values()




# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1LsooTZ92sL47qjFB9hwcW2WxiHrregLMjf8YZnUvLKo/edit#gid=840924667')
# worksheet_list = sh.worksheets()