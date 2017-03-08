#!/usr/bin/env python
from WlcInventory import WlcInventory

commands = '''\
config ap led-state flash indefinite AP1604-3702p
config ap led-state flash indefinite AP1654-3702p
config ap led-state flash indefinite AP1243-3702e
config ap led-state flash indefinite AP1660-3702p
config ap led-state flash indefinite AP1635-3702p
'''.splitlines()

# commands = '''\
# show snmpv3user
# show switchconfig
# '''.splitlines()

if __name__ == '__main__':
    wlcs = WlcInventory()
    wlcs.connect_to_many(['WLC3'])
    input("Press Enter to partee...")
    output = wlcs.send_instruction('WLC3', commands)
    wlcs.close_all()
    print('It\'s a parteeeeee')


