# Change this!!
MAPPING_FILE = 'apgroup-mapping.csv'
COMMAND_FILE = 'apgroup-map-commands.txt'


def save_commands(commands_file, command_list):
    """
    Write config commands on a text file
    :param commands_file: file name
    :param command_list: list containing commands
    :return: nothing
    """
    file = open(commands_file, 'w')
    for command in command_list:
        file.write("{}\n".format(command))
    file.close()


# initialize variables
command_list = []

names = {
    'CL17': ('1', 'customer_clients'),
    'mgmt': ('22', 'noc_clients'),
    'IPV6': ('4', 'v6'),
    'CL17-24': ('21', 'customer_clients'),
    'demo': ('23', 'demo'),
}

# loads mapping list from the file, line by line
mapping_list = open(MAPPING_FILE).read().split('\n')

# go line by line through the list
for apgroup_line in mapping_list:
    # breaks the comma separated values
    apgroup_list = apgroup_line.split(',')
    # apgroup name on first column
    apgroup = apgroup_list[0]
    command_list.append('config wlan apgroup add {apgroup}'.format(apgroup=apgroup))  # go through all WLAN in the list
    for wlan in apgroup_list[1:]:
        try:
            command_list.append("config wlan apgroup interface-mapping add {apgroup} {wlan_id} {interface}".format(
                apgroup=apgroup,
                wlan_id=names[wlan][0],
                interface=names[wlan][1]))
        except KeyError:
            # empty cell
            pass

save_commands(COMMAND_FILE, command_list)

# for command in command_list:
# 	print(command)



# command_list.append()
