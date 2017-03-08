from apgroup_parser import *
import yaml
WLANS_FILE = 'wlans.yml'

with open(WLANS_FILE) as f:
    wlans = yaml.load(f)
with open(FILE) as f:
    apgroups = yaml.load(f)

wlan_id = list(wlans.keys())
col = [ wlans[x] for x in wlan_id ]

for apgroup in apgroups:
    apgroup_name = apgroup['name']
    wlan_list = [int(wlan['wlan_id']) for wlan in apgroup['wlans']]
    row = [ apgroup_name ] + []