#!/usr/bin/env python
from WlcInventory import WlcInventory

if __name__ == '__main__':
    wlcs = WlcInventory()
    wlcs.connect_to_many()
    wlcs.save_all()
    wlcs.send_command_to_many(save_showrun_ftp=True)
    wlcs.close_all()
    print('Done')


