'''
script to parse the show wlan apgroups output
'''
import re
from pprint import pprint as pprint
import yaml
FILE = 'apgroups_output.yml'

raw_output = '''\
(WLC3) >show wlan apgroups

Total Number of AP Groups........................ 9


Site Name........................................ CL17-Backoffice
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... Standard_b
5 GHz band....................................... Standard_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 21              customer_clients     Disabled                          None
 22              noc_clients          Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------
H_001.1_AP_332       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:8c         Halle 1.1  LAG   DE       1
H_001.1_AP_167       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:88         Halle 1.1  LAG   DE       1
H_001.1_AP_48        2     AIR-CAP3702E-E-K9    58:ac:78:12:73:b8         Halle 1.1  LAG   DE       1
H_001.1_AP_218       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:f8         Halle 1.1  LAG   DE       1
H_001.1_AP_243       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:a0         Halle 1.1  LAG   DE       1
H_001.1_AP_268       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:a8         Halle 1.1  LAG   DE       1
H_001.1_AP_52        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:4c         Halle 1.1  LAG   DE       1
H_001.1_AP_51        2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:d4         Halle 1.1  LAG   DE       1
H_001.1_AP_143       2     AIR-CAP3702E-E-K9    58:ac:78:00:06:e8         Halle 1.1  LAG   DE       1
H_001.1_AP_47        2     AIR-CAP3702E-E-K9    58:ac:78:12:75:9c         Halle 1.1  LAG   DE       1
H_001.1_AP_66        2     AIR-CAP3702E-E-K9    58:ac:78:0f:3d:08         Halle 1.1  LAG   DE       1
H_001.1_AP_168       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:cc         Halle 1.1  LAG   DE       1
H_001.1_AP_67        2     AIR-CAP3702E-E-K9    58:ac:78:34:2f:94         Halle 1.1  LAG   DE       1
H_001.1_AP_244       2     AIR-CAP3702E-E-K9    58:ac:78:00:06:94         Halle 1.1  LAG   DE       1
H_001.1_AP_145       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:6c         Halle 1.1  LAG   DE       1
H_001.1_AP_49        2     AIR-CAP3702E-E-K9    58:ac:78:12:73:40         Halle 1.1  LAG   DE       1
H_001.1_AP_336       2     AIR-CAP3702E-E-K9    58:ac:78:0f:34:e8         Halle 1.1  LAG   DE       1
H_001.1_AP_63        2     AIR-CAP3702E-E-K9    58:ac:78:15:92:e4         Halle 1.1  LAG   DE       1
H_001.1_AP_219       3     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:f8         Halle 1.1  LAG   DE       1
H_001.1_AP_68        3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:0c         Halle 1.1  LAG   DE       1
H_001.1_AP_334       3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:20         Halle 1.1  LAG   DE       1
H_001.1_AP_64        3     AIR-CAP3702E-E-K9    58:ac:78:12:7f:1c         Halle 1.1  LAG   DE       1
H_001.1_AP_119       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:70         Halle 1.1  LAG   DE       1
H_001.1_AP_144       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:e4         Halle 1.1  LAG   DE       1



Site Name........................................ CL17-CAE
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... Keynote_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 21              customer_clients     Disabled                          None
 22              noc_clients          Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------



Site Name........................................ CL17-DevNet
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... Standard_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 22              noc_clients          Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------



Site Name........................................ CL17-General
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... Standard_b
5 GHz band....................................... Standard_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 21              customer_clients     Disabled                          None
 22              noc_clients          Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------
H_007.1c_AP_286      2     AIR-CAP3702E-E-K9    58:ac:78:12:73:b0        Halle 7.1c  LAG   DE       1
H_007.2b_AP_282      2     AIR-CAP3702E-E-K9    58:ac:78:15:92:d0        Halle 7.2b  LAG   DE       1
H_007.1a_AP_78       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:20        Halle 7.1a  LAG   DE       1
H_007.1a_AP_153      2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:54        Halle 7.1a  LAG   DE       1
H_007.1c_AP_291      2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:ec        Halle 7.1c  LAG   DE       1
H_007.1a_AP_140      2     AIR-CAP3702E-E-K9    58:ac:78:34:20:08        Halle 7.1a  LAG   DE       1
H_007.3_AP_179       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:64         Halle 7.3  LAG   DE       1
H_007.2a_AP_152      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:dc        Halle 7.2a  LAG   DE       1
H_007.3_AP_176       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:0c         Halle 7.3  LAG   DE       1
H_007.2b_AP_8        2     AIR-CAP3702E-E-K9    58:ac:78:00:11:b8        Halle 7.2b  LAG   DE       1
H_007.1c_AP_310      2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:74        Halle 7.1c  LAG   DE       1
H_007.3_AP_235       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:58         Halle 7.3  LAG   DE       1
H_007.2a_AP_238      2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:68        Halle 7.2a  LAG   DE       1
H_007.2b_AP_114      2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:e8        Halle 7.2b  LAG   DE       1
H_007.2a_AP_151      2     AIR-CAP3702E-E-K9    58:ac:78:12:73:7c        Halle 7.2a  LAG   DE       1
H_007.1c_AP_303      2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:a8        Halle 7.1c  LAG   DE       1
H_007.2a_AP_242      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:58        Halle 7.2a  LAG   DE       1
H_007.2a_AP_163      2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:74        Halle 7.2a  LAG   DE       1
H_007.3_AP_173       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:00         Halle 7.3  LAG   DE       1
H_007.2c_AP_146      2     AIR-CAP3702E-E-K9    58:ac:78:15:92:20        Halle 7.2c  LAG   DE       1
H_007.1c_AP_290      2     AIR-CAP3702E-E-K9    58:ac:78:15:92:34        Halle 7.1c  LAG   DE       1
H_007.3_AP_85        2     AIR-CAP3702E-E-K9    58:ac:78:34:20:48         Halle 7.3  LAG   DE       1
H_007.2a_FY_AP_903   2     AIR-CAP3702I-E-K9    00:81:c4:e9:91:48  Ebene2 Foyer 7.2  LAG   DE       1
H_007.1c_AP_311      2     AIR-CAP3702E-E-K9    58:ac:78:00:06:60        Halle 7.1c  LAG   DE       1
H_007.1c_AP_288      2     AIR-CAP3702E-E-K9    58:ac:78:00:07:20        Halle 7.1c  LAG   DE       1
H_007.1a_AP_139      2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:cc        Halle 7.1a  LAG   DE       1
H_007.3_AP_87        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:dc         Halle 7.3  LAG   DE       1
H_007.1c_AP_277      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:1c        Halle 7.1c  LAG   DE       1
H_007.3a_FY_AP_924   2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:74  Ebene3 Foyer101   LAG   DE       1
H_007.2c_AP_7        2     AIR-CAP3702E-E-K9    58:ac:78:34:2f:e8        Halle 7.2c  LAG   DE       1
H_007.2a_AP_225      2     AIR-CAP3702E-E-K9    58:ac:78:34:20:84        Halle 7.2a  LAG   DE       1
H_007.3_AP_160       2     AIR-CAP3702E-E-K9    58:ac:78:12:74:e8         Halle 7.3  LAG   DE       1
H_007.2c_AP_208      2     AIR-CAP3702E-E-K9    58:ac:78:34:30:60        Halle 7.2c  LAG   DE       1
H_007.2a_AP_228      2     AIR-CAP3702E-E-K9    58:ac:78:34:20:88        Halle 7.2a  LAG   DE       1
H_007.1b-007.1c_UG_AP_842  2     AIR-CAP3702I-E-K9    00:81:c4:c3:5a:e0  Übergang 7.1b/7  LAG   DE       1
H_007.2b_AP_285      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:fc        Halle 7.2b  LAG   DE       1
H_007.1a_AP_227      2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:d0        Halle 7.1a  LAG   DE       1
H_007.2c_AP_213      2     AIR-CAP3702E-E-K9    58:ac:78:34:20:e0        Halle 7.2c  LAG   DE       1
H_007.1a_AP_50       2     AIR-CAP3702E-E-K9    58:ac:78:15:94:48        Halle 7.1a  LAG   DE       1
H_007.1b-007.1c_UG_AP_843  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6e:b4  Übergang 7.1b/7  LAG   DE       1
H_007.2b_AP_217      2     AIR-CAP3702E-E-K9    58:ac:78:15:93:a8        Halle 7.2b  LAG   DE       1
H_007.2b_AP_187      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:34        Halle 7.2b  LAG   DE       1
H_007.2a_AP_170      2     AIR-CAP3702E-E-K9    58:ac:78:15:93:74        Halle 7.2a  LAG   DE       1
H_007.2c_AP_147      2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:e0        Halle 7.2c  LAG   DE       1
H_007.2c_AP_222      2     AIR-CAP3702E-E-K9    58:ac:78:15:92:f0        Halle 7.2c  LAG   DE       1
H_007.1a_AP_155      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:14        Halle 7.1a  LAG   DE       1
H_007.2a_FY_AP_904   2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:10  Ebene2 Foyer 7.2  LAG   DE       1
H_007.1a_AP_154      2     AIR-CAP3702E-E-K9    58:ac:78:34:21:28        Halle 7.1a  LAG   DE       1
H_007.2b_AP_289      2     AIR-CAP3702E-E-K9    58:ac:78:34:23:ec        Halle 7.2b  LAG   DE       1
H_007.1a_AP_80       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:44        Halle 7.1a  LAG   DE       1
H_007.3_AP_234       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:34         Halle 7.3  LAG   DE       1
H_007.1c_AP_280      2     AIR-CAP3702E-E-K9    58:ac:78:12:73:74        Halle 7.1c  LAG   DE       1
H_007.2b_AP_287      2     AIR-CAP3702E-E-K9    58:ac:78:15:93:d0        Halle 7.2b  LAG   DE       1
H_007.3a_FY_AP_923   2     AIR-CAP3702I-E-K9    00:2a:10:02:45:40  Ebene3 Foyer101   LAG   DE       1
H_007.2b_AP_284      2     AIR-CAP3702E-E-K9    58:ac:78:34:20:98        Halle 7.2b  LAG   DE       1
H_007.1a_FY_AP_838   2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:d4  Ebene1 Foyer 7.1  LAG   DE       1
H_007.2a_AP_226      2     AIR-CAP3702E-E-K9    58:ac:78:34:21:08        Halle 7.2a  LAG   DE       1
H_007.2c_AP_224      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:e8        Halle 7.2c  LAG   DE       1
H_007.1a_FY_AP_839   2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:44  Ebene1 Foyer 7.1  LAG   DE       1
H_007.2c_AP_209      2     AIR-CAP3702E-E-K9    58:ac:78:34:30:50        Halle 7.2c  LAG   DE       1
H_007.2c_AP_211      2     AIR-CAP3702E-E-K9    58:ac:78:0f:3d:48        Halle 7.2c  LAG   DE       1
SCH7_Kassenhalle_E02_AP_731  2     AIR-CAP3702E-E-K9    00:81:c4:98:3f:c4  Ebene2 Foyer SCH  LAG   DE       1
AP1588-2702e         2     AIR-CAP2702E-E-K9    00:81:c4:57:19:60              CL17  LAG   DE       1
H_007c_ZE2_AP_917    2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:64  ZE2-301 Foyer 7c  LAG   DE       1
SCH7_Garderobe_DG_E02_AP_928  2     AIR-CAP3702I-E-K9    00:81:c4:d7:0f:d0  Ebene2 Foyer SCH  LAG   DE       1
H_007a_ZE2_AP_916    2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:50  ZE2-101 Foyer 7a  LAG   DE       1
H_007a_ZE1_AP_878    2     AIR-CAP3702I-E-K9    00:81:c4:ca:61:74  ZE1-101 Foyer 7a  LAG   DE       1
SCH7_Kassenhalle_E02_AP_730  2     AIR-CAP3702E-E-K9    00:81:c4:99:20:40  Ebene2 Foyer SCH  LAG   DE       1
H_007b_ZE1_AP_879    2     AIR-CAP3702I-E-K9    00:2a:10:01:2c:f0  ZE1-201 Foyer 7b  LAG   DE       1
H_007.2a-007.2b_UG_AP_905  2     AIR-CAP3702I-E-K9    00:2a:10:02:45:cc  Übergang 7.2a/7  LAG   DE       1
SCH7_Windfang_E02_AP_929  2     AIR-CAP3702I-E-K9    00:81:c4:ca:5f:dc  Ebene2 Foyer SCH  LAG   DE       1
H_007c_ZE1_AP_880    2     AIR-CAP3702I-E-K9    00:81:c4:cc:6e:24  ZE1-301 Foyer 7c  LAG   DE       1
H_007.2b-007.2c_UG_AP_908  2     AIR-CAP3702I-E-K9    00:81:c4:ca:62:34  Übergang 7.2b/7  LAG   DE       1
H_007.2a-007.2b_UG_AP_906  2     AIR-CAP3702I-E-K9    00:81:c4:e9:90:a8  Übergang 7.2a/7  LAG   DE       1
H_007.2b-007.2c_UG_AP_907  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6d:98  Übergang 7.2b/7  LAG   DE       1
AP1546-2702e         2     AIR-CAP2702E-E-K9    18:8b:9d:7b:19:e4              CL17  LAG   DE       1
AP1562-2702e         2     AIR-CAP2702E-E-K9    58:ac:78:45:b4:50              CL17  LAG   DE       1
AP1548-2702e         2     AIR-CAP2702E-E-K9    18:8b:9d:7b:6c:48              CL17  LAG   DE       1
H_002.1_AP_74        2     AIR-CAP3702E-E-K9    58:ac:78:12:74:a4         Halle 2.1  LAG   DE       1
H_002.1_AP_141       2     AIR-CAP3702E-E-K9    58:ac:78:12:73:c8         Halle 2.1  LAG   DE       1
H_002.1_AP_103       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:a4         Halle 2.1  LAG   DE       1
H_002.1_AP_13        2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:d4         Halle 2.1  LAG   DE       1
H_002.1_AP_79        2     AIR-CAP3702E-E-K9    58:ac:78:15:93:dc         Halle 2.1  LAG   DE       1
H_002.1_AP_192       2     AIR-CAP3702E-E-K9    58:ac:78:12:75:8c         Halle 2.1  LAG   DE       1
H_002.1_AP_110       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:28         Halle 2.1  LAG   DE       1
H_002.1_AP_107       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:38         Halle 2.1  LAG   DE       1
H_002.1_AP_82        2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:dc         Halle 2.1  LAG   DE       1
H_002.1_AP_195       2     AIR-CAP3702E-E-K9    58:ac:78:0a:30:78         Halle 2.1  LAG   DE       1
H_002.1_AP_10        2     AIR-CAP3702E-E-K9    58:ac:78:12:7e:b8         Halle 2.1  LAG   DE       1
H_002.1_AP_106       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:58         Halle 2.1  LAG   DE       1
H_002.1_AP_75        2     AIR-CAP3702E-E-K9    58:ac:78:15:93:88         Halle 2.1  LAG   DE       1
H_002.1_AP_105       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:c4         Halle 2.1  LAG   DE       1
H_002.1_AP_81        2     AIR-CAP3702E-E-K9    58:ac:78:15:93:70         Halle 2.1  LAG   DE       1
H_002.1_AP_193       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:28         Halle 2.1  LAG   DE       1
H_003.1_AP_99        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:04         Halle 3.1  LAG   DE       1
H_003.1_AP_158       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:c4         Halle 3.1  LAG   DE       1
H_003.1_AP_175       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:bc         Halle 3.1  LAG   DE       1
H_003.1_AP_181       2     AIR-CAP3702E-E-K9    58:ac:78:12:74:2c         Halle 3.1  LAG   DE       1
H_003.1_AP_136       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:10         Halle 3.1  LAG   DE       1
H_003.1_AP_72        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:00         Halle 3.1  LAG   DE       1
H_002.1_AP_108       3     AIR-CAP3702E-E-K9    58:ac:78:34:20:74         Halle 2.1  LAG   DE       1
H_002.1_AP_28        3     AIR-CAP3702E-E-K9    58:ac:78:12:73:94         Halle 2.1  LAG   DE       1
H_003.1_AP_101       2     AIR-CAP3702E-E-K9    58:ac:78:00:07:48         Halle 3.1  LAG   DE       1
H_002.1_AP_76        3     AIR-CAP3702E-E-K9    58:ac:78:15:93:7c         Halle 2.1  LAG   DE       1
H_003.1_AP_25        2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:70         Halle 3.1  LAG   DE       1
H_003.1_AP_229       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:5c         Halle 3.1  LAG   DE       1
H_002.1_AP_104       3     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:d8         Halle 2.1  LAG   DE       1
H_003.1_AP_20        2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:40         Halle 3.1  LAG   DE       1
H_003.1_AP_21        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:2c         Halle 3.1  LAG   DE       1
H_003.1_AP_73        2     AIR-CAP3702E-E-K9    58:ac:78:34:23:f0         Halle 3.1  LAG   DE       1
H_003.1_AP_159       2     AIR-CAP3702E-E-K9    58:ac:78:12:74:50         Halle 3.1  LAG   DE       1
H_003.1_AP_162       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:28         Halle 3.1  LAG   DE       1
H_002.1_AP_35        3     AIR-CAP3702E-E-K9    58:ac:78:12:74:40         Halle 2.1  LAG   DE       1
H_002.1_AP_111       3     AIR-CAP3702E-E-K9    58:ac:78:34:20:68         Halle 2.1  LAG   DE       1
H_003.1_AP_230       2     AIR-CAP3702E-E-K9    58:ac:78:0a:30:48         Halle 3.1  LAG   DE       1
H_002.1_AP_16        3     AIR-CAP3702E-E-K9    58:ac:78:12:74:ec         Halle 2.1  LAG   DE       1
H_002.1_AP_196       3     AIR-CAP3702E-E-K9    70:e4:22:ff:23:08         Halle 2.1  LAG   DE       1
H_003.1_AP_100       3     AIR-CAP3702E-E-K9    58:ac:78:15:92:c0         Halle 3.1  LAG   DE       1
H_003.1_AP_77        3     AIR-CAP3702E-E-K9    58:ac:78:15:92:44         Halle 3.1  LAG   DE       1
H_003.1_AP_232       3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:c8         Halle 3.1  LAG   DE       1
H_003.1_AP_161       3     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:f0         Halle 3.1  LAG   DE       1
H_003.1_AP_19        3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:64         Halle 3.1  LAG   DE       1
H_003.1_AP_157       3     AIR-CAP3702E-E-K9    70:e4:22:ff:22:7c         Halle 3.1  LAG   DE       1
H_004.1_AP_169       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:94         Halle 4.1  LAG   DE       1
H_004.1_AP_39        2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:b4         Halle 4.1  LAG   DE       1
H_004.1_AP_38        2     AIR-CAP3702E-E-K9    70:e4:22:ff:23:48         Halle 4.1  LAG   DE       1
H_004.1_AP_42        2     AIR-CAP3702E-E-K9    58:ac:78:12:73:cc         Halle 4.1  LAG   DE       1
H_004.1_AP_172       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:c0         Halle 4.1  LAG   DE       1
H_004.1_AP_117       2     AIR-CAP3702E-E-K9    58:ac:78:12:74:60         Halle 4.1  LAG   DE       1
H_004.1_AP_122       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:40         Halle 4.1  LAG   DE       1
H_004.1_AP_40        2     AIR-CAP3702E-E-K9    70:e4:22:ff:22:d0         Halle 4.1  LAG   DE       1
H_004.1_AP_246       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:2c         Halle 4.1  LAG   DE       1
H_004.1_AP_329       2     AIR-CAP3702E-E-K9    70:e4:22:ff:22:a8         Halle 4.1  LAG   DE       1
H_004.1_AP_337       2     AIR-CAP3702E-E-K9    58:ac:78:0a:30:68         Halle 4.1  LAG   DE       1
H_004.1_AP_116       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:e0         Halle 4.1  LAG   DE       1
H_004.1_AP_194       2     AIR-CAP3702E-E-K9    70:e4:22:ff:23:64         Halle 4.1  LAG   DE       1
H_004.1_AP_57        2     AIR-CAP3702E-E-K9    58:ac:78:15:92:b0         Halle 4.1  LAG   DE       1
H_004.1_AP_245       3     AIR-CAP3702E-E-K9    58:ac:78:0f:34:70         Halle 4.1  LAG   DE       1
H_004.1_AP_120       3     AIR-CAP3702E-E-K9    58:ac:78:15:92:f8         Halle 4.1  LAG   DE       1
H_004.1_AP_330       3     AIR-CAP3702E-E-K9    70:e4:22:ff:22:8c         Halle 4.1  LAG   DE       1
H_004.1_AP_184       3     AIR-CAP3702E-E-K9    58:ac:78:12:73:9c         Halle 4.1  LAG   DE       1
H_004.1_AP_121       3     AIR-CAP3702E-E-K9    58:ac:78:15:92:b8         Halle 4.1  LAG   DE       1
H_004.1_AP_37        3     AIR-CAP3702E-E-K9    70:e4:22:ff:23:74         Halle 4.1  LAG   DE       1
H_004.1_AP_41        3     AIR-CAP3702E-E-K9    58:ac:78:0f:32:74         Halle 4.1  LAG   DE       1
H_004.1_AP_60        3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:4c         Halle 4.1  LAG   DE       1
H_003.1_AP_22        2     AIR-CAP3702E-E-K9    58:ac:78:15:92:b4         Halle 3.1  LAG   DE       1
H_004.1_AP_328       3     AIR-CAP3702E-E-K9    70:e4:22:ff:22:e4         Halle 4.1  LAG   DE       1
H_004.1_AP_171       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:2c         Halle 4.1  LAG   DE       1
H_005.2_AP_558       2     AIR-CAP3702E-E-K9    00:81:c4:08:c4:f4         Halle 5.2  LAG   DE       1
H_005.3_AP_515       2     AIR-CAP3702E-E-K9    00:81:c4:9e:8f:34         Halle 5.3  LAG   DE       1
H_005.3_AP_506       2     AIR-CAP3702E-E-K9    00:81:c4:b3:7f:cc         Halle 5.3  LAG   DE       1
H_005.2_AP_559       2     AIR-CAP3702E-E-K9    00:81:c4:29:e4:10         Halle 5.2  LAG   DE       1
H_005.3_AP_512       2     AIR-CAP3702E-E-K9    00:81:c4:34:70:1c         Halle 5.3  LAG   DE       1
H_005.2_AP_547       2     AIR-CAP3702E-E-K9    00:81:c4:32:b2:98         Halle 5.2  LAG   DE       1
H_005.2_AP_557       2     AIR-CAP3702E-E-K9    00:f6:63:ff:43:9c         Halle 5.2  LAG   DE       1
H_005.3_AP_516       2     AIR-CAP3702E-E-K9    00:81:c4:99:20:f8         Halle 5.3  LAG   DE       1
H_005.2_AP_550       2     AIR-CAP3702E-E-K9    00:81:c4:32:b3:34         Halle 5.2  LAG   DE       1
H_005.3_AP_511       2     AIR-CAP3702E-E-K9    00:81:c4:3c:f0:f8         Halle 5.3  LAG   DE       1
H_005.3_AP_513       2     AIR-CAP3702E-E-K9    00:81:c4:4c:43:90         Halle 5.3  LAG   DE       1
H_005.2_AP_556       2     AIR-CAP3702E-E-K9    00:81:c4:0a:9a:ec         Halle 5.2  LAG   DE       1
H_005.3_AP_514       2     AIR-CAP3702E-E-K9    00:81:c4:0a:9d:04         Halle 5.3  LAG   DE       1
H_005.3_AP_510       2     AIR-CAP3702E-E-K9    00:81:c4:32:b3:18         Halle 5.3  LAG   DE       1
H_005.3_AP_507       3     AIR-CAP3702E-E-K9    00:81:c4:9a:c2:10         Halle 5.3  LAG   DE       1
H_005.3_AP_508       3     AIR-CAP3702E-E-K9    00:81:c4:98:41:20         Halle 5.3  LAG   DE       1
H_005.3_AP_509       3     AIR-CAP3702E-E-K9    00:81:c4:99:20:f0         Halle 5.3  LAG   DE       1
H_005.3_AP_505       3     AIR-CAP3702E-E-K9    00:81:c4:9a:c1:14         Halle 5.3  LAG   DE       1
H_005.2_AP_539       3     AIR-CAP3702E-E-K9    00:81:c4:32:ad:d4         Halle 5.2  LAG   DE       1
H_005.2_AP_537       3     AIR-CAP3702E-E-K9    00:81:c4:3c:eb:88         Halle 5.2  LAG   DE       1
H_005.2_AP_536       3     AIR-CAP3702E-E-K9    00:81:c4:34:6b:7c         Halle 5.2  LAG   DE       1
H_005.2_AP_540       3     AIR-CAP3702E-E-K9    00:81:c4:3a:a9:08         Halle 5.2  LAG   DE       1
H_005.2_AP_538       3     AIR-CAP3702E-E-K9    00:81:c4:3c:ef:6c         Halle 5.2  LAG   DE       1
AP1620-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5e:90  default location  LAG   DE       1
H_006.2_AP_27        2     AIR-CAP3702E-E-K9    58:ac:78:12:73:78         Halle 6.2  LAG   DE       1
H_006.2_AP_316       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:90         Halle 6.2  LAG   DE       1
H_006.2_AP_198       2     AIR-CAP3702E-E-K9    58:ac:78:15:94:1c         Halle 6.2  LAG   DE       1
H_006.2_AP_314       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:e4         Halle 6.2  LAG   DE       1
H_006.2_AP_199       2     AIR-CAP3702E-E-K9    58:ac:78:0f:34:d4         Halle 6.2  LAG   DE       1
H_006.2_AP_61        2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:18         Halle 6.2  LAG   DE       1
H_006.2_AP_312       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:7c         Halle 6.2  LAG   DE       1
AP1654-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:f4:4c  default location  LAG   DE       1
AP1249-3702e         2     AIR-CAP3702E-E-K9    7c:ad:74:ff:6e:f6  default location  LAG   DE       1
H_006.2_AP_313       3     AIR-CAP3702E-E-K9    58:ac:78:15:93:b8         Halle 6.2  LAG   DE       1
H_006.2_AP_203       3     AIR-CAP3702E-E-K9    58:ac:78:00:12:88         Halle 6.2  LAG   DE       1
H_006.2_AP_29        3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:04         Halle 6.2  LAG   DE       1
H_006.2_AP_255       3     AIR-CAP3702E-E-K9    58:ac:78:15:92:f4         Halle 6.2  LAG   DE       1
AP1886-3802e         2     AIR-AP3802E-E-K9     a0:e0:af:34:1d:a2              CL17  LAG   DE       1
AP1885-3802e         2     AIR-AP3802E-E-K9     2c:d0:2d:f8:0f:e6              CL17  LAG   DE       1
AP1135-3702i         3     AIR-CAP3702I-E-K9    74:26:ac:4f:95:ec  default location  LAG   DE       1
H_001/002_ZE1_LH_Passau_AP595  2     AIR-CAP3702E-E-K9    00:81:c4:32:b0:50  ZE1 MF_1/2_Passa  LAG   DE       1
AP1887-3802e         2     AIR-AP3802E-E-K9     2c:d0:2d:f8:0f:bc              CL17  LAG   DE       1
AP1157-3702i         2     AIR-CAP3702I-E-K9    a8:9d:21:05:a4:b0  default location  LAG   DE       1
AP1199-3702i         2     AIR-CAP3702I-E-K9    58:97:bd:26:ec:2c  default location  LAG   DE       1
H_003.1_AP_71        3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:b8         Halle 3.1  LAG   DE       1
AP1192-3702i         2     AIR-CAP3702I-E-K9    58:97:bd:2e:fa:80  default location  LAG   DE       1
H_003b/004b_MF_ZE1_AP_851  2     AIR-CAP3702I-E-K9    00:81:c4:e9:91:14  ZE1 MF_ZA3-4_B-S  LAG   DE       1
AP1186-3702i         2     AIR-CAP3702I-E-K9    58:97:bd:2b:80:ec  default location  LAG   DE       1
H_001/002_ZE1_Passau_AP_724  2     AIR-CAP3702E-E-K9    00:81:c4:98:3f:54  Halle 1.1/2.1_MF  LAG   DE       1
H_001.1b/002.1b_MF_AP_817  2     AIR-CAP3702I-E-K9    00:81:c4:c3:5b:28  Halle 1.1b/2.1b_  LAG   DE       1
AP1603-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:91:21:60  default location  LAG   DE       1
H_003/4-005/6_UG_ZE1_AP_856  2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:c0  ZE1 ÜG 3/4 - 5/  LAG   DE       1
H_003.1a/004.1a_MF_AP_823  2     AIR-CAP3702I-E-K9    00:81:c4:d7:0f:78  Halle 3.1/4.1_MF  LAG   DE       1
H_003.1b/004.1b_MF_AP_821  2     AIR-CAP3702I-E-K9    00:2a:10:02:47:20  Halle 3.1/4.1_MF  LAG   DE       1
H_003b/004b_MF_ZE1_AP_852  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6e:ac  ZE1 MF_ZA3-4_B-S  LAG   DE       1
H_001.1/002.1_MF_AP_819  2     AIR-CAP3702I-E-K9    00:81:c4:d7:0f:88  Halle1.1/2.1_MF_  LAG   DE       1
H_003.1a/004.1a_MF_AP_824  2     AIR-CAP3702I-E-K9    00:81:c4:c8:c7:30  ZA3/4-E01 Halle   LAG   DE       1
H_005.1a/006.1a_MF_AP_826  2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:4c  Halle 5.1a/6.1a_  LAG   DE       1
EMS_AP_237           2     AIR-CAP3702E-E-K9    58:ac:78:34:20:40  Eingang Messe S  LAG   DE       1
AP1140-3702i         3     AIR-CAP3702I-E-K9    74:26:ac:68:f1:e0  default location  LAG   DE       1
H_003/004_ZE1_AP_853  2     AIR-CAP3702I-E-K9    00:81:c4:c3:5c:14  ZE1 ZA3/4_Mitte   LAG   DE       1
EMS_AP_239           2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:44  Eingang Messe S  LAG   DE       1
H_005a/006a_MF_ZE1_AP_858  2     AIR-CAP3702I-E-K9    00:2a:10:01:2c:90  ZE1 MF_ZA5-6_A-S  LAG   DE       1
H_001.1a/002.1a_MF_AP_793  2     AIR-CAP3702I-E-K9    00:81:c4:e9:8b:9c  Halle 1.1a/2.1a_  LAG   DE       1
H_005.1a/006.1a_MF_AP_825  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6d:5c  Halle 5.1a/6.1a_  LAG   DE       1
AP1610-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:91:20:08  default location  LAG   DE       1
H_001.1b/002.1b_MF_AP_818  2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:c8  Halle 1.1b/2.1b_  LAG   DE       1
H_003.1/004.1_MF_AP_822  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6e:1c  Halle 3.1/4.1_MF  LAG   DE       1
H_005a/006a_MF_ZE1_AP_859  2     AIR-CAP3702I-E-K9    00:81:c4:e9:8f:d8  ZE1 MF_ZA5-6_A-S  LAG   DE       1
EMS_AP_233           2     AIR-CAP3702E-E-K9    58:ac:78:12:74:3c  Eingang Messe S  LAG   DE       1
AP1604-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:77:59:28  default location  LAG   DE       1
AP1606-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:91:21:08  default location  LAG   DE       1
AP1605-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:77:59:38  default location  LAG   DE       1
AP1136-3702i         2     AIR-CAP3702I-E-K9    18:e7:28:ce:5a:a0              CL17  LAG   DE       1
AP2077-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8e:60  default location  LAG   DE       1
AP1243-3702e         2     AIR-CAP3702E-E-K9    bc:16:65:09:3c:8c  default location  LAG   DE       1
AP2076-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:04:5e  default location  LAG   DE       1
AP2029-3802i         2     AIR-AP3802I-E-K9     00:42:68:a0:fd:68  default location  LAG   DE       1
AP2009-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8d:c8  default location  LAG   DE       1
AP1156-3702i         2     AIR-CAP3702I-E-K9    a8:9d:21:05:a4:a4  default location  LAG   DE       1
AP2063-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8a:cc  default location  LAG   DE       1
AP2061-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:91:ba              CL17  LAG   DE       1
AP2094-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:56:5a  default location  LAG   DE       1
AP1664-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e2:26:9c  default location  LAG   DE       1
AP1665-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e2:26:80  default location  LAG   DE       1
AP2067-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:02:78  default location  LAG   DE       1
AP2088-3802i         2     AIR-AP3802I-E-K9     00:42:68:a0:fd:d2  default location  LAG   DE       1
AP1159-3702i         2     AIR-CAP3702I-E-K9    a8:9d:21:05:a6:7c  default location  LAG   DE       1
AP2091-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:5d:10  default location  LAG   DE       1
AP2008-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:01:38  default location  LAG   DE       1
AP2090-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:5e:18  default location  LAG   DE       1
AP1193-3702i         2     AIR-CAP3702I-E-K9    58:97:bd:2b:81:e8  default location  LAG   DE       1
AP2089-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:94:0a  default location  LAG   DE       1
AP2060-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8c:d2              CL17  LAG   DE       1
AP2075-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:91:56  default location  LAG   DE       1
AP2071-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:00:fc  default location  LAG   DE       1
AP2093-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:5c:e2  default location  LAG   DE       1
AP1153-3702i         2     AIR-CAP3702I-E-K9    a8:9d:21:2e:c1:34  default location  LAG   DE       1
AP2066-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:00:ae  default location  LAG   DE       1
AP2078-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:03:ea  default location  LAG   DE       1
AP2062-3802i         2     AIR-AP3802I-E-K9     00:42:68:a0:ff:d2  default location  LAG   DE       1
AP2070-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:03:ec  default location  LAG   DE       1
AP1634-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bc:b5:fc  default location  LAG   DE       1
AP2092-3802i         2     AIR-AP3802I-E-K9     00:42:68:a0:e7:9a  default location  LAG   DE       1
AP1718-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:a0  default location  LAG   DE       1
AP1660-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:90  default location  LAG   DE       1
AP1717-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:a0  default location  LAG   DE       1
AP1069-3702i         2     AIR-CAP3702I-E-K9    b8:38:61:2d:91:60  default location  LAG   DE       1
AP1112-3702i         2     AIR-CAP3702I-E-K9    bc:16:65:09:cc:a4  default location  LAG   DE       1
AP1713-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5f:14  default location  LAG   DE       1
AP1080-3702i         2     AIR-CAP3702I-E-K9    b8:38:61:48:b8:50  default location  LAG   DE       1
AP1008-3702i         3     AIR-CAP3702I-E-K9    b8:38:61:48:c9:c8  default location  LAG   DE       1
AP1715-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5e:d0  default location  LAG   DE       1
AP1178-3702i         3     AIR-CAP3702I-E-K9    58:97:bd:26:ec:34  default location  LAG   DE       1
AP2407-3702i         3     AIR-CAP3702I-E-K9    58:97:bd:26:ec:5c  default location  LAG   DE       1
AP1181-3702i         3     AIR-CAP3702I-E-K9    58:97:bd:2b:82:c0  default location  LAG   DE       1
AP1714-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:58  default location  LAG   DE       1
AP1118-3702i         3     AIR-CAP3702I-E-K9    bc:16:65:09:cd:18  default location  LAG   DE       1
AP1035-3702i         3     AIR-CAP3702I-E-K9    b8:38:61:43:61:14  default location  LAG   DE       1
AP1023-3702i         3     AIR-CAP3702I-E-K9    b8:38:61:2d:9b:fc  default location  LAG   DE       1
AP1038-3702i         3     AIR-CAP3702I-E-K9    b8:38:61:48:ca:40  default location  LAG   DE       1
AP1716-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:7a:96:a8  default location  LAG   DE       1
AP1611-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:83:18:2c  default location  LAG   DE       1
AP1601-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:8a:67:50  default location  LAG   DE       1
AP1271-3702e         2     AIR-CAP3702E-E-K9    7c:ad:74:ff:61:12  default location  LAG   DE       1
AP1608-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:77:59:c0  default location  LAG   DE       1
AP1669-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:64  default location  LAG   DE       1
AP1658-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:97:58  default location  LAG   DE       1
AP1667-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:b4  default location  LAG   DE       1
AP1657-3702p         2     AIR-CAP3702P-E-K9    00:c8:8b:21:32:50  default location  LAG   DE       1
AP1678-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bc:b6:40  default location  LAG   DE       1
AP1672-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:a5:8c  default location  LAG   DE       1
AP1637-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:a6:24  default location  LAG   DE       1
AP1663-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5f:44  default location  LAG   DE       1
AP1635-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5e:94  default location  LAG   DE       1
AP1698-3702p         2     AIR-CAP3702P-E-K9    00:f2:8b:f4:17:6c              CL17  LAG   DE       1
AP1690-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:54              CL17  LAG   DE       1
AP1677-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:cc  default location  LAG   DE       1
AP1280-3702e         2     AIR-CAP3702E-E-K9    7c:ad:74:ff:62:6e  default location  LAG   DE       1
AP1680-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:90              CL17  LAG   DE       1
AP1253-3702e         2     AIR-CAP3702E-E-K9    7c:ad:74:ff:63:02  default location  LAG   DE       1
AP1675-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:e4  default location  LAG   DE       1
AP1661-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:80  default location  LAG   DE       1
AP1621-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:1c  default location  LAG   DE       1
AP1662-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:9a:84  default location  LAG   DE       1
AP1630-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5f:04  default location  LAG   DE       1
AP1631-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:9a:f0  default location  LAG   DE       1
AP1639-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:a5:dc  default location  LAG   DE       1
AP1627-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5f:18  default location  LAG   DE       1
AP1681-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:0c              CL17  LAG   DE       1
AP1624-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:cc  default location  LAG   DE       1
AP1632-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0c:98  default location  LAG   DE       1
AP1652-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:78  default location  LAG   DE       1
AP1688-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:9b:20  default location  LAG   DE       1
AP1629-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:90  default location  LAG   DE       1
AP1687-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:54  default location  LAG   DE       1
AP1640-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:f8  default location  LAG   DE       1
AP1628-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:e0  default location  LAG   DE       1
AP1686-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5e:bc  default location  LAG   DE       1
AP1638-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:64  default location  LAG   DE       1
AP1633-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:e4  default location  LAG   DE       1
H_005.2a/006.2a_MF_AP_466  2     AIR-CAP3702E-E-K9    00:81:c4:9a:c0:94  Halle 5.2a/6.2a_  LAG   DE       1
H_001.2b/002.2b_MF_AP_600  2     AIR-CAP3702E-E-K9    00:81:c4:3a:ac:90  Halle 1.2b/2.2b_  LAG   DE       1
H_001.2a/2.2a_MF_AP_594  2     AIR-CAP3702E-E-K9    00:f6:63:ff:42:c8  Halle 1.2a/2.2a_  LAG   DE       1
H_003.2b/004.2b_MF_AP_468  2     AIR-CAP3702E-E-K9    00:81:c4:98:27:98  Halle 3.2b/4.2b_  LAG   DE       1
H_005.2a/006.2a_MF_AP_465  2     AIR-CAP3702E-E-K9    00:81:c4:9a:c0:7c  Halle 5.2a/6.2a_  LAG   DE       1
H_003.2a/004.2a_MF_AP_469  2     AIR-CAP3702E-E-K9    00:81:c4:3c:f2:4c  Halle 3.2a/4.2a_  LAG   DE       1
H_003.2a/004.2a_MF_AP_470  2     AIR-CAP3702E-E-K9    00:81:c4:4c:3f:c4  Halle 3.2a/4.2a_  LAG   DE       1
H_001.2a/002.2a_MF_AP_599  2     AIR-CAP3702E-E-K9    00:81:c4:4c:3e:bc  Halle 1.2a/2.2a_  LAG   DE       1
H_003.2b/004.2b_MF_AP_467  2     AIR-CAP3702E-E-K9    00:81:c4:99:1f:24  Halle 3.2b/4.2b_  LAG   DE       1
H_001.2b/002.2b_MF_AP_601  2     AIR-CAP3702E-E-K9    00:81:c4:34:2a:d4  Halle 1.2b/2.2b_  LAG   DE       1
H_003.2/004.2_MF_AP_889  2     AIR-CAP3702I-E-K9    00:81:c4:ca:61:34  Halle 3.2/4.2 ZA  LAG   DE       1
AP1666-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:fc  default location  LAG   DE       1
AP1668-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:c0:35:a8  default location  LAG   DE       1
AP1693-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:c8  default location  LAG   DE       1
AP1671-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:f6:dc  default location  LAG   DE       1
AP2059-3802i         2     AIR-AP3802I-E-K9     00:42:68:c5:be:10              CL17  LAG   DE       1
AP1068-3702i         2     AIR-CAP3702I-E-K9    bc:16:65:09:ce:70  default location  LAG   DE       1
AP1061-3702i         2     AIR-CAP3702I-E-K9    b8:38:61:48:ca:0c  default location  LAG   DE       1
AP1143-3702i         2     AIR-CAP3702I-E-K9    64:12:25:4b:da:20  default location  LAG   DE       1
AP1602-3702p         2     AIR-CAP3702P-E-K9    e8:65:49:77:59:90  default location  LAG   DE       1
AP2079-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:03:a6  default location  LAG   DE       1
AP1697-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:d4  default location  LAG   DE       1
AP1884-3802e         2     AIR-AP3802E-E-K9     a0:e0:af:34:1d:74              CL17  LAG   DE       1
AP1720-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:88              CL17  LAG   DE       1
AP1123-3702i         2     AIR-CAP3702I-E-K9    64:12:25:3e:7d:f0  default location  LAG   DE       1
AP1538-2702e         2     AIR-CAP2702E-E-K9    f4:0f:1b:26:7b:b0              CL17  LAG   DE       1
AP1626-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:30  default location  LAG   DE       1
AP1656-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:a3:98  default location  LAG   DE       1
AP1623-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:87:5f:34  default location  LAG   DE       1
AP1245-3702e         3     AIR-CAP3702E-E-K9    7c:ad:74:ff:6a:3e  default location  LAG   DE       1
EMS_AP_164           2     AIR-CAP3702E-E-K9    58:ac:78:12:74:24  Eingang Messe S  LAG   DE       1
H_003a/004a_MF_ZE1_AP_854  2     AIR-CAP3702I-E-K9    00:81:c4:98:34:20  ZE1 MF_ZE1_A-Sei  LAG   DE       1
EMS_AP_166           2     AIR-CAP3702E-E-K9    58:ac:78:34:20:10  Eingang Messe S  LAG   DE       1
H_005/006_ZE2_MF_AP_912  2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:f4   ZE2 Mitte ZA5/6  LAG   DE       1
H_005/006_ZE2_MF_AP_913  2     AIR-CAP3702I-E-K9    00:2a:10:02:54:64   ZE2 Mitte ZA5/6  LAG   DE       1
EMS_AP_165           2     AIR-CAP3702E-E-K9    70:e4:22:e5:12:c8  Eingang Messe S  LAG   DE       1
EMS_AP_236           2     AIR-CAP3702E-E-K9    58:ac:78:34:20:04  Eingang Messe S  LAG   DE       1
H_003a/004a_MF_ZE1_AP_855  2     AIR-CAP3702I-E-K9    00:2a:10:02:44:68  ZE1 MF_ZE1_A-Sei  LAG   DE       1
EMS_AP_240           2     AIR-CAP3702E-E-K9    58:ac:78:15:93:bc  Eingang Messe S  LAG   DE       1
EMS_AP_59            2     AIR-CAP3702E-E-K9    58:ac:78:15:92:ac  Eingang Messe S  LAG   DE       1
AP1270-3702e         3     AIR-CAP3702E-E-K9    bc:16:65:09:47:00  default location  LAG   DE       1
AP1670-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:e5:a6:8c  default location  LAG   DE       1
AP1607-3702p         3     AIR-CAP3702P-E-K9    e8:65:49:83:17:d4  default location  LAG   DE       1
AP1622-3702p         3     AIR-CAP3702P-E-K9    00:c8:8b:21:32:8c  default location  LAG   DE       1
AP1625-3702p         3     AIR-CAP3702P-E-K9    00:f2:8b:f4:17:58  default location  LAG   DE       1
AP2012-3802i         2     AIR-AP3802I-E-K9     00:42:68:a0:fd:26              CL17  LAG   DE       1
AP2013-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8e:6c              CL17  LAG   DE       1
AP1679-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:87:5f:8c  default location  LAG   DE       1
AP1712-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:e8  default location  LAG   DE       1
AP1708-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:e5:a6:90  default location  LAG   DE       1
AP1705-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0d:a8  default location  LAG   DE       1
AP1709-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:40              CL17  LAG   DE       1
AP1702-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e3:bc  default location  LAG   DE       1
AP1704-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:84  default location  LAG   DE       1
AP1706-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e4:80  default location  LAG   DE       1
AP1703-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:78:7c  default location  LAG   DE       1
AP1701-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bf:e6:30           Filipes  LAG   DE       1
AP1707-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0b:98  default location  LAG   DE       1
AP1711-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:a2:0c:28              CL17  LAG   DE       1
AP1710-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5f:20  default location  LAG   DE       1
AP2007-3802i         2     AIR-AP3802I-E-K9     00:42:68:c5:c1:22  default location  LAG   DE       1
AP2011-3802i         2     AIR-AP3802I-E-K9     00:42:68:c5:db:7e  default location  LAG   DE       1
H_007.1b_AP_308      2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:dc        Halle 7.1b  LAG   DE       1
H_007.1b_AP_279      2     AIR-CAP3702E-E-K9    58:ac:78:12:73:ac        Halle 7.1b  LAG   DE       1
H_007.1b_AP_278      2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:a0        Halle 7.1b  LAG   DE       1
H_007.1b_AP_309      2     AIR-CAP3702E-E-K9    58:ac:78:12:74:18        Halle 7.1b  LAG   DE       1
AP1125-3702i         2     AIR-CAP3702I-E-K9    74:26:ac:cf:6a:58              CL17  LAG   DE       1
H_007.1b_AP_283      2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:90        Halle 7.1b  LAG   DE       1
H_006_ZE1_Dessau_AP_867  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6e:98  Halle 7 --> 6 De  LAG   DE       1
H_007.1a-007.1b_UG_AP_840  2     AIR-CAP3702I-E-K9    00:2a:10:01:2c:a8  Übergang 7.1a/7  LAG   DE       1
H_002_ZE1_Lindau_AP_877  2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:e0  Halle 7 --> 2 Li  LAG   DE       1
H_004_ZE1_Weimar_AP_871  2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:6c  Halle 7 --> 4 We  LAG   DE       1
H_001/002_MF_ZE1_AP_848  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6d:04  ZE1 MF_ZA1-2 Mit  LAG   DE       1
H_007.1b_AP_115      2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:44        Halle 7.1b  LAG   DE       1
H_007.1a-007.1b_UG_AP_841  2     AIR-CAP3702I-E-K9    00:81:c4:c8:cb:04  Übergang 7.1a/7  LAG   DE       1
H_002_ZE1_Lindau_AP_875  2     AIR-CAP3702I-E-K9    00:2a:10:02:42:14  Halle 7 --> 2 Li  LAG   DE       1
H_006_ZE1_Dessau_AP_869  2     AIR-CAP3702I-E-K9    00:81:c4:ca:61:58  Halle 7 --> 6 De  LAG   DE       1
H_007.1b_AP_281      2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:90        Halle 7.1b  LAG   DE       1
H_004_ZE1_Weimar_AP_873  2     AIR-CAP3702I-E-K9    00:81:c4:e9:8f:44  Halle 7 --> 4 We  LAG   DE       1
H_007.1b_AP_142      2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:28        Halle 7.1b  LAG   DE       1
AP1696-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:87:5e:b4  default location  LAG   DE       1
AP1576-2702e         2     AIR-CAP2702E-E-K9    00:f6:63:63:c1:1c              CL17  LAG   DE       1
AP1575-2702e         2     AIR-CAP2702E-E-K9    00:3a:7d:c9:ab:98              CL17  LAG   DE       1
AP1683-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:bc:b6:34              CL17  LAG   DE       1
AP1036-3702i         3     AIR-CAP3702I-E-K9    b8:38:61:43:5a:58  default location  LAG   DE       1
AP2023-3802i         2     AIR-AP3802I-E-K9     00:42:68:a7:53:64  default location  LAG   DE       1
AP2004-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8e:48  default location  LAG   DE       1
AP2026-3802i         2     AIR-AP3802I-E-K9     58:ac:78:de:8e:72              CL17  LAG   DE       1
AP2027-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:01:22              CL17  LAG   DE       1
AP2074-3802i         2     AIR-AP3802I-E-K9     00:42:68:a7:62:38  default location  LAG   DE       1
AP2024-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:00:ec              CL17  LAG   DE       1
AP2005-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:02:4c              CL17  LAG   DE       1
AP2065-3802i         2     AIR-AP3802I-E-K9     00:42:68:a1:02:a8  default location  LAG   DE       1
AP1653-3702p         3     AIR-CAP3702P-E-K9    00:35:1a:87:5e:80              CL17  LAG   DE       1
AP1882-3802e         2     AIR-AP3802E-E-K9     2c:d0:2d:f8:10:52              CL17  LAG   DE       1
H_003.2/4.2-005.2/6.2_UG_AP_464  2     AIR-CAP3702E-E-K9    00:81:c4:99:1d:94  Ebene2 MF ÜG Au  LAG   DE       1
H_003.2-005.2_UG_AP_463  2     AIR-CAP3702E-E-K9    00:81:c4:9a:bf:bc  Ebene2 West ÜG   LAG   DE       1
H_004.1-006.1_UG_AP_607  2     AIR-CAP3702E-E-K9    00:81:c4:18:57:70  Ebene1 Ost ÜG A  LAG   DE       1
H_004.2-006.2_UG_AP_462  2     AIR-CAP3702E-E-K9    00:81:c4:b3:7d:78  Ebene2 Ost ÜG A  LAG   DE       1
H_001.1-003.1_UG_AP_606  2     AIR-CAP3702E-E-K9    00:81:c4:08:c4:a8  Ebene1 West ÜG   LAG   DE       1
H_001.1/2.1-003.1/4.1_UG_AP_725  2     AIR-CAP3702E-E-K9    00:81:c4:9e:8d:d4  Ebene1 MF ÜG Au  LAG   DE       1
H_005.2b_KF_AP_897   2     AIR-CAP3702I-E-K9    00:81:c4:ca:61:98  Ebene2 West Kopf  LAG   DE       1
H_003.1-005.1_UG_AP_605  2     AIR-CAP3702E-E-K9    00:81:c4:3a:ae:dc  Ebene1 West ÜG   LAG   DE       1
H_002_ZE1_Lindau_AP_876  2     AIR-CAP3702I-E-K9    00:81:c4:ca:61:cc  Halle 7 --> 2 Li  LAG   DE       1
H_001.2/2.2-003.2/4.2_UG_AP_603  2     AIR-CAP3702E-E-K9    00:81:c4:34:2b:44  Ebene2 MF ÜG Au  LAG   DE       1
H_005.2_AP_unnamed   2     AIR-CAP3702E-E-K9    00:81:c4:3c:f1:c8         halle-5-2  LAG   DE       1
H_004.1-007.1b_UG_AP_598  2     AIR-CAP3702E-E-K9    00:81:c4:3a:a9:1c  Ebene1 ÜG Auße  LAG   DE       1
H_001b/002b_MF_ZE1_AP_847  2     AIR-CAP3702I-E-K9    00:2a:10:02:44:a4  ZE1 MF_ZA1-2_B-S  LAG   DE       1
H_002.1-007.1a_UG_AP_597  2     AIR-CAP3702E-E-K9    00:81:c4:34:70:0c  Ebene1 ÜG Auße  LAG   DE       1
H_002.1-004.1_UG_AP_604  2     AIR-CAP3702E-E-K9    00:81:c4:3a:ae:ec  Ebene1 Ost ÜG A  LAG   DE       1
H_001b/002b_MF_ZE1_AP_846  2     AIR-CAP3702I-E-K9    00:81:c4:e9:91:ec  ZE1 MF_ZA1-2_B-S  LAG   DE       1
SCH7_Garderobe_DG_E02_AP_927  2     AIR-CAP3702I-E-K9    00:2a:10:02:47:38  Ebene2 Foyer SCH  LAG   DE       1
H_001a/002a_MF_ZE1_AP_849  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6c:90  ZE1 MF_ZA1-2_A-S  LAG   DE       1
H_006.1-007.1c_UG_AP_596  2     AIR-CAP3702E-E-K9    00:81:c4:3a:a9:60  Ebene1 ÜG Auße  LAG   DE       1
H_002.2-007.2a_UG_AP_473  2     AIR-CAP3702E-E-K9    00:81:c4:99:1f:b8  Ebene2 ÜG Auße  LAG   DE       1
EMS_UG_E01_AP_816    2     AIR-CAP3702I-E-K9    00:81:c4:cc:6d:c4  Ebene1 Durchfahr  LAG   DE       1
H_004_ZE1_Weimar_AP_870  2     AIR-CAP3702I-E-K9    00:81:c4:e9:92:28  Halle 7 --> 4 We  LAG   DE       1
H_006_ZE1_Dessau_AP_866  2     AIR-CAP3702I-E-K9    00:2a:10:02:46:6c  Halle 7 --> 6 De  LAG   DE       1
H_002_ZE1_Lindau_AP_874  2     AIR-CAP3702I-E-K9    00:81:c4:cc:6c:c4  Halle 7 --> 2 Li  LAG   DE       1
H_005.2b_KF_AP_896   2     AIR-CAP3702I-E-K9    00:2a:10:02:47:04  Ebene2 West Kopf  LAG   DE       1
H_004_ZE1_Weimar_AP_872  2     AIR-CAP3702I-E-K9    00:2a:10:01:2d:28  Halle 7 --> 4 We  LAG   DE       1
H_006_ZE1_Dessau_AP_868  2     AIR-CAP3702I-E-K9    00:2a:10:01:2c:9c  Halle 7 --> 6 De  LAG   DE       1
H_001/2-H_003/4_UG_ZE1_AP_850  2     AIR-CAP3702I-E-K9    00:2a:10:02:45:64  ZE1 ÜG 1/2 - 3/  LAG   DE       1
H_006.2_AP_62        3     AIR-CAP3702E-E-K9    58:ac:78:0f:32:b0         Halle 6.2  LAG   DE       1
AP1651-3702p         2     AIR-CAP3702P-E-K9    00:35:1a:af:7a:a0              CCB1  LAG   DE       1
AP1240-3702e         2     AIR-CAP3702E-E-K9    7c:ad:74:ff:67:ce  default location  LAG   DE       1



Site Name........................................ CL17-Keynote
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... Keynote_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 22              noc_clients          Disabled                          None
 21              customer_clients     Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------



Site Name........................................ CL17-Keynote-demo
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... Demo_b
5 GHz band....................................... Demo_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------



Site Name........................................ CL17-WOS
Site Description................................. <none>
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... Standard_a

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None
 22              noc_clients          Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------
H_003.2_AP_247       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:ec         Halle 3.2  LAG   DE       1
H_003.2_AP_26        2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:9c         Halle 3.2  LAG   DE       1
H_003.2_AP_12        2     AIR-CAP3702E-E-K9    58:ac:78:12:74:14         Halle 3.2  LAG   DE       1
H_003.2_AP_252       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:6c         Halle 3.2  LAG   DE       1
H_003.2_AP_250       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:68         Halle 3.2  LAG   DE       1
H_003.2_AP_138       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:ac         Halle 3.2  LAG   DE       1
H_003.2_AP_109       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:50         Halle 3.2  LAG   DE       1
H_003.2_AP_70        2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:74         Halle 3.2  LAG   DE       1
H_003.2_AP_221       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:a8         Halle 3.2  LAG   DE       1
H_003.2_AP_216       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:e4         Halle 3.2  LAG   DE       1
H_003.2_AP_112       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:70         Halle 3.2  LAG   DE       1
H_003.2_AP_23        3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:48         Halle 3.2  LAG   DE       1
H_003.2_AP_69        3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:24         Halle 3.2  LAG   DE       1
H_003.2_AP_113       3     AIR-CAP3702E-E-K9    70:e4:22:e5:13:f0         Halle 3.2  LAG   DE       1
H_003.2_AP_220       3     AIR-CAP3702E-E-K9    58:ac:78:12:74:d4         Halle 3.2  LAG   DE       1
H_003.2_AP_137       3     AIR-CAP3702E-E-K9    70:e4:22:e5:12:c4         Halle 3.2  LAG   DE       1
H_003.2_AP_214       3     AIR-CAP3702E-E-K9    58:ac:78:15:93:98         Halle 3.2  LAG   DE       1
H_003.2_AP_135       3     AIR-CAP3702E-E-K9    58:ac:78:12:73:70         Halle 3.2  LAG   DE       1
H_003.2_AP_11        3     AIR-CAP3702E-E-K9    70:e4:22:e5:12:b8         Halle 3.2  LAG   DE       1
H_001.2_AP_307       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:ec         Halle 1.2  LAG   DE       1
H_001.2_AP_183       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:d8         Halle 1.2  LAG   DE       1
H_001.2_AP_180       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:ac         Halle 1.2  LAG   DE       1
H_001.2_AP_148       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:d0         Halle 1.2  LAG   DE       1
H_001.2_AP_84        2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:84         Halle 1.2  LAG   DE       1
H_001.2_AP_302       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:90         Halle 1.2  LAG   DE       1
H_001.2_AP_98        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:f4         Halle 1.2  LAG   DE       1
H_001.2_AP_128       2     AIR-CAP3702E-E-K9    58:ac:78:12:73:64         Halle 1.2  LAG   DE       1
H_001.2_AP_129       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:1c         Halle 1.2  LAG   DE       1
H_001.2_AP_304       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:30         Halle 1.2  LAG   DE       1
H_001.2_AP_223       2     AIR-CAP3702E-E-K9    58:ac:78:12:74:44         Halle 1.2  LAG   DE       1
H_001.2_AP_34        2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:18         Halle 1.2  LAG   DE       1
H_001.2_AP_185       2     AIR-CAP3702E-E-K9    70:e4:22:e4:01:b0         Halle 1.2  LAG   DE       1
H_001.2_AP_130       2     AIR-CAP3702E-E-K9    70:e4:22:e5:14:2c         Halle 1.2  LAG   DE       1
H_001.2_AP_306       3     AIR-CAP3702E-E-K9    58:ac:78:34:1f:8c         Halle 1.2  LAG   DE       1
H_001.2_AP_123       3     AIR-CAP3702E-E-K9    70:e4:22:e5:13:64         Halle 1.2  LAG   DE       1
H_001.2_AP_32        3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:1c         Halle 1.2  LAG   DE       1
H_001.2_AP_150       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:a4         Halle 1.2  LAG   DE       1
H_001.2_AP_149       3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:58         Halle 1.2  LAG   DE       1
H_001.2_AP_102       3     AIR-CAP3702E-E-K9    70:e4:22:ff:23:4c         Halle 1.2  LAG   DE       1
H_001.2_AP_182       3     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:48         Halle 1.2  LAG   DE       1
H_001.2_AP_124       3     AIR-CAP3702E-E-K9    58:ac:78:0f:32:f4         Halle 1.2  LAG   DE       1
H_001.2_AP_96        3     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:30         Halle 1.2  LAG   DE       1
H_003.2_AP_248       3     AIR-CAP3702E-E-K9    58:ac:78:12:73:d4         Halle 3.2  LAG   DE       1
H_003.2_AP_24        3     AIR-CAP3702E-E-K9    58:ac:78:34:1f:b8         Halle 3.2  LAG   DE       1
H_004.2_AP_297       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:7c         Halle 4.2  LAG   DE       1
H_004.2_AP_300       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:fc         Halle 4.2  LAG   DE       1
H_004.2_AP_295       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:9c         Halle 4.2  LAG   DE       1
H_004.2_AP_206       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:fc         Halle 4.2  LAG   DE       1
H_004.2_AP_292       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:78         Halle 4.2  LAG   DE       1
H_003.2_AP_36        2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:f4         Halle 3.2  LAG   DE       1
H_004.2_AP_294       2     AIR-CAP3702E-E-K9    58:ac:78:34:21:2c         Halle 4.2  LAG   DE       1
H_004.2_AP_191       2     AIR-CAP3702E-E-K9    70:e4:22:ff:23:34         Halle 4.2  LAG   DE       1
H_004.2_AP_2         2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:84         Halle 4.2  LAG   DE       1
H_002.2-004.2_UG_AP_471  2     AIR-CAP3702E-E-K9    00:81:c4:b3:7d:64  Ebene2 Ost ÜG A  LAG   DE       1
H_004.2_AP_296       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:94         Halle 4.2  LAG   DE       1
H_004.2_AP_212       2     AIR-CAP3702E-E-K9    58:ac:78:34:30:94         Halle 4.2  LAG   DE       1
H_004.2_AP_4         2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:bc         Halle 4.2  LAG   DE       1
H_004.2_AP_210       2     AIR-CAP3702E-E-K9    58:ac:78:0f:3c:f4         Halle 4.2  LAG   DE       1
H_004.2_AP_127       2     AIR-CAP3702E-E-K9    58:ac:78:34:2f:dc         Halle 4.2  LAG   DE       1
H_004.2_AP_125       2     AIR-CAP3702E-E-K9    58:ac:78:0f:3c:00         Halle 4.2  LAG   DE       1
H_004.2_AP_190       2     AIR-CAP3702E-E-K9    70:e4:22:ff:23:04         Halle 4.2  LAG   DE       1
H_004.2_AP_204       3     AIR-CAP3702E-E-K9    58:ac:78:12:7f:68         Halle 4.2  LAG   DE       1
H_004.2_AP_33        3     AIR-CAP3702E-E-K9    58:ac:78:34:1e:0c         Halle 4.2  LAG   DE       1
H_004.2_AP_293       3     AIR-CAP3702E-E-K9    58:ac:78:34:20:34         Halle 4.2  LAG   DE       1
H_004.2_AP_301       3     AIR-CAP3702E-E-K9    58:ac:78:0f:32:78         Halle 4.2  LAG   DE       1
H_004.2_AP_126       3     AIR-CAP3702E-E-K9    58:ac:78:0f:34:6c         Halle 4.2  LAG   DE       1
H_004.2_AP_298       3     AIR-CAP3702E-E-K9    58:ac:78:12:75:dc         Halle 4.2  LAG   DE       1
H_004.2_AP_299       3     AIR-CAP3702E-E-K9    58:ac:78:0f:33:a4         Halle 4.2  LAG   DE       1
H_002.2_AP_274       2     AIR-CAP3702E-E-K9    58:ac:78:0f:33:08         Halle 2.2  LAG   DE       1
H_002.2_AP_132       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:9c         Halle 2.2  LAG   DE       1
H_002.2_AP_118       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:e8         Halle 2.2  LAG   DE       1
H_002.2_AP_241       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:38         Halle 2.2  LAG   DE       1
H_002.2_AP_260       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:c8         Halle 2.2  LAG   DE       1
H_002.2_AP_324       2     AIR-CAP3702E-E-K9    70:e4:22:e5:13:dc         Halle 2.2  LAG   DE       1
H_002.2_AP_45        2     AIR-CAP3702E-E-K9    58:ac:78:0a:30:bc         Halle 2.2  LAG   DE       1
H_002.2_AP_65        2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:50         Halle 2.2  LAG   DE       1
H_002.2_AP_323       2     AIR-CAP3702E-E-K9    58:ac:78:12:73:68         Halle 2.2  LAG   DE       1
H_002.2_AP_276       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:6c         Halle 2.2  LAG   DE       1
H_002.2_AP_273       2     AIR-CAP3702E-E-K9    58:ac:78:34:1e:9c         Halle 2.2  LAG   DE       1
H_002.2_AP_231       2     AIR-CAP3702E-E-K9    58:ac:78:00:06:ec         Halle 2.2  LAG   DE       1
H_002.2_AP_322       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:f4         Halle 2.2  LAG   DE       1
H_002.2_AP_275       2     AIR-CAP3702E-E-K9    58:ac:78:15:93:e8         Halle 2.2  LAG   DE       1
H_002.2_AP_272       2     AIR-CAP3702E-E-K9    58:ac:78:15:93:90         Halle 2.2  LAG   DE       1
H_002.2_AP_261       2     AIR-CAP3702E-E-K9    58:ac:78:34:1f:ac         Halle 2.2  LAG   DE       1
H_002.2_AP_134       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:48         Halle 2.2  LAG   DE       1
H_002.2_AP_133       2     AIR-CAP3702E-E-K9    58:ac:78:0f:32:8c         Halle 2.2  LAG   DE       1
H_002.2_AP_266       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2e:ec         Halle 2.2  LAG   DE       1
H_002.2_AP_259       2     AIR-CAP3702E-E-K9    58:ac:78:0a:2f:3c         Halle 2.2  LAG   DE       1
H_002.2_AP_320       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:b0         Halle 2.2  LAG   DE       1
H_002.2_AP_131       2     AIR-CAP3702E-E-K9    58:ac:78:15:92:2c         Halle 2.2  LAG   DE       1
H_002.2_AP_321       2     AIR-CAP3702E-E-K9    58:ac:78:34:20:b8         Halle 2.2  LAG   DE       1
H_002.2_AP_271       2     AIR-CAP3702E-E-K9    58:ac:78:00:06:64         Halle 2.2  LAG   DE       1



Site Name........................................ default-group
Site Description................................. <none>
NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... <none>

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 1               customer_clients     Disabled                          None
 4               v6                   Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------



Site Name........................................ stackenblochen
Site Description................................. stackenblochen
Venue Group Code................................. Unspecified
Venue Type Code.................................. Unspecified

NAS-identifier................................... none
Client Traffic QinQ Enable....................... FALSE
DHCPv4 QinQ Enable............................... FALSE
AP Operating Class............................... Not-configured
Capwap Prefer Mode............................... Not-configured

RF Profile
----------
2.4 GHz band..................................... <none>
5 GHz band....................................... <none>

WLAN ID          Interface          Network Admission Control          Radio Policy
-------          -----------        --------------------------         ------------
 17              null                 Disabled                          None

*AP3600 with 802.11ac Module will only advertise first 8 WLANs on 5GHz radios.


 Lan Port configs
 ----------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled      Disabled     None
 2           Disabled                   None
 3           Disabled                   None

 External 3G/4G module configs
 -----------------------------

LAN          Status        POE          RLAN
---          -------       ----         -----
 1           Disabled                   None

AP Name             Slots  AP Model             Ethernet MAC       Location          Port  Country  Priority
------------------  -----  -------------------  -----------------  ----------------  ----  -------  --------

'''

def parse(raw_output):
    """

    :param raw_output:
    :return:
    """

    apgroups={}
    #regexp to match number of groups
    'Total Number of AP Groups........................ 9'
    number_re = re.compile(r'Total Number of AP Groups\.+\s(.*)')
    # regexp to match group name
    'Site Name........................................ CL17-Backoffice'
    name_re = re.compile(r'Site Name\.+\s(.*)')
    # regexp to match ap names
    'any k.nd_of g@rbag&         2     AIR-CAP2702E-E-K9    18:8b:9d:7b:19:e4              CL17  LAG   DE       1'
    ap_name_re = re.compile(r'(.*?)\s*\d\s{5}AIR.*')
    # matches empyy line
    end_scope_re = re.compile(r'^$')
    # matches wlan_ID and Interface_name
    '21              customer_clients     Disabled                          None'
    wlan_re = re.compile(r'\s*(?P<wlan_id>\d+)\s+(?P<if_name>.*?)\s.*')
    need_number = True
    scope = None
    ap_group_number = 0
    for line in raw_output.splitlines():
        # get apgroup count
        if need_number:
            try:
                ap_group_number = int(number_re.match(line).groups()[0])
                need_number = False
            except:
                pass
        if scope is None:
            if re.match(r'RF Profile',line):
                scope = 'rf-profile'
            if re.match(r'WLAN ID', line):
                scope = 'wlan-override'
            if re.match(r'AP Name', line):
                scope = 'ap-table'
            else:
                try:
                    group_name = name_re.match(line).groups()[0]
                    aps = []
                    wlans = []
                    group_details = {'name': group_name, 'aps': aps, 'wlans': wlans}
                    apgroups[group_name] = group_details
                except:
                    pass
        if scope == 'rf-profile':
            try:
                profile_24 = re.match(r'2\.4 GHz band\.+ (.*)',line).groups()[0]
                group_details['rf_profile_24'] = profile_24
            except:
                pass
            try:
                profile_5 = re.match(r'5 GHz band\.+ (.*)',line).groups()[0]
                group_details['rf_profile_5'] = profile_5
            except:
                pass
        if scope == 'wlan-override':
            try:
                match =  wlan_re.match(line)
                wlan_entry = match.groupdict()
                wlans.append(wlan_entry)
            except:
                pass
        if scope == 'ap-table':
            # match ap and add them to the list
            try:
                ap_name = ap_name_re.match(line).groups()[0]
                aps.append(ap_name)
            except:
                pass
        if end_scope_re.match(line):
            scope = None

    # sanity check
    if len(apgroups) != ap_group_number:
        print('Uh Oh, some output is missing')
    # remove this
    else:
        print('All Good')
    pprint(apgroups)
    return apgroups

if __name__ == '__main__':
    apgroups = parse(raw_output)
    with open(FILE, 'w') as f:
        f.write(yaml.dump(default_flow_style=False))


