#!/usr/bin/env python
from WlcInventory import WlcInventory

if __name__ == '__main__':
    wlcs = WlcInventory()
    wlcs.connect_to_many()
    wlcs.save_all()
    print('all saved')
    wlcs.send_command_to_many(save_config_ftp=True)
    print('all uplodaded')
    wlcs.close_all()


