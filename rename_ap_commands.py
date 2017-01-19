'''
config ap name <name> <MAC>
'''

import csv, sys
filename = 'ap_list.csv'
location = 'CL17'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    commands = []
    try:
        for row in reader:
            # if CL 2017 Audit is ticked
            if row[9] == '1':
                # get mac address
                mac = row[2].lower()
                # convert mac address
                newmac = '{}:{}:{}:{}:{}:{}'.format(mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])
                # config ap name <name> <MAC>
                commands.append('config ap name {} {}\n'.format(row[8],newmac))
                commands.append('config ap location {} {}\n'.format(location, newmac))
        spreadsheet = list(reader)
        with open('commands','a+') as f:
            f.writelines(commands)
    except csv.Error as e:
        print('Some bs error')
