APs = '''\
AP2094-3802i
AP2085-3802i
AP2086-3802i
AP2087-3802i
AP2064-3802i
AP2074-3802i
AP2072-3802i
AP2067-3802i
AP2070-3802i
AP2065-3802i
AP2071-3802i
AP2068-3802i
AP2073-3802i
AP2066-3802i
AP2089-3802i
AP2090-3802i
AP2069-3802i
AP2063-3802i
AP2080-3802i'''

APs = 'AP2080-3802i'

for ap in APs.splitlines():
    print('config ap led-state flash 300 {}'.format(ap))