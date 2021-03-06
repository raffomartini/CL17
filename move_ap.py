from WlcInventory import WlcInventory
import re

INITIAL_WLC = 'WLC7'
END_WLC = 'WLC7'

# output = '''\
# some garbage
# other garbage
#
# an empty line
#
# <other kind of garbage>
# H_005a/006a_MF_ZE1_AP_858  2     AIR-CAP3702I-E-K9     00:2a:10:01:2c:90  ZE1 MF_ZA5-6_A-S  DE          10.7.6.34          0       [0 ,0 ,0 ]
# H_005a/006a_MF_ZE1_AP_859  2     AIR-CAP3702I-E-K9     00:81:c4:e9:8f:d8  ZE1 MF_ZA5-6_A-S  DE          10.7.6.36          0       [0 ,0 ,0 ]
# H_005.1a/006.1a_MF_AP_826  2     AIR-CAP3702I-E-K9     00:2a:10:01:2d:4c  Halle 5.1a/6.1a_  DE          10.7.6.35          0       [0 ,0 ,0 ]
# H_005.2a/006.2a_MF_AP_466  2     AIR-CAP3702E-E-K9     00:81:c4:9a:c0:94  Halle 5.2a/6.2a_  DE          10.7.6.33          0       [0 ,0 ,0 ]
# H_005.1a/006.1a_MF_AP_825  2     AIR-CAP3702I-E-K9     00:81:c4:cc:6d:5c  Halle 5.1a/6.1a_  DE          10.7.6.32          0       [0 ,0 ,0 ]
# H_007.2a_AP_242      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:58  Halle 7.2a        DE          10.7.7.34          0       [0 ,0 ,0 ]
# H_002.2-007.2a_UG_AP_473  2     AIR-CAP3702E-E-K9     00:81:c4:99:1f:b8  Ebene2 ÜG Auße  DE          10.7.7.35          0       [0 ,0 ,0 ]
# H_007a_ZE1_AP_878    2     AIR-CAP3702I-E-K9     00:81:c4:ca:61:74  ZE1-101 Foyer 7a  DE          10.7.7.36          0       [0 ,0 ,0 ]
# H_007.2a_FY_AP_904   2     AIR-CAP3702I-E-K9     00:2a:10:01:2d:10  Ebene2 Foyer 7.2  DE          10.7.7.38          0       [0 ,0 ,0 ]
# H_002.1-007.1a_UG_AP_597  2     AIR-CAP3702E-E-K9     00:81:c4:34:70:0c  Ebene1 ÜG Auße  DE          10.7.7.39          0       [0 ,0 ,0 ]
# H_007.2a_FY_AP_903   2     AIR-CAP3702I-E-K9     00:81:c4:e9:91:48  Ebene2 Foyer 7.2  DE          10.7.7.43          0       [0 ,0 ,0 ]
# H_007.2a_AP_226      2     AIR-CAP3702E-E-K9     58:ac:78:34:21:08  Halle 7.2a        DE          10.7.7.74          0       [0 ,0 ,0 ]
# H_007.2a_AP_225      2     AIR-CAP3702E-E-K9     58:ac:78:34:20:84  Halle 7.2a        DE          10.7.7.93          0       [0 ,0 ,0 ]
# H_007.2a_AP_152      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2e:dc  Halle 7.2a        DE          10.7.7.70          0       [0 ,0 ,0 ]
# H_007.2a_AP_151      2     AIR-CAP3702E-E-K9     58:ac:78:12:73:7c  Halle 7.2a        DE          10.7.7.76          0       [0 ,0 ,0 ]
# H_007.2a_AP_228      2     AIR-CAP3702E-E-K9     58:ac:78:34:20:88  Halle 7.2a        DE          10.7.7.79          0       [0 ,0 ,0 ]
# H_007.2a_AP_238      2     AIR-CAP3702E-E-K9     70:e4:22:e5:13:68  Halle 7.2a        DE          10.7.7.77          0       [0 ,0 ,0 ]
# H_007.2a_AP_170      2     AIR-CAP3702E-E-K9     58:ac:78:15:93:74  Halle 7.2a        DE          10.7.7.75          0       [0 ,0 ,0 ]
# H_007.1a_FY_AP_838   2     AIR-CAP3702I-E-K9     00:2a:10:01:2d:d4  Ebene1 Foyer 7.1  DE          10.7.7.44          0       [0 ,0 ,0 ]
# H_007.1a_FY_AP_839   2     AIR-CAP3702I-E-K9     00:81:c4:c8:cb:44  Ebene1 Foyer 7.1  DE          10.7.7.47          0       [0 ,0 ,0 ]
# H_007.1a_AP_140      2     AIR-CAP3702E-E-K9     58:ac:78:34:20:08  Halle 7.1a        DE          10.7.7.48          0       [0 ,0 ,0 ]
# H_007.1a_AP_227      2     AIR-CAP3702E-E-K9     58:ac:78:0f:33:d0  Halle 7.1a        DE          10.7.7.50          0       [0 ,0 ,0 ]
# H_007.1a_AP_139      2     AIR-CAP3702E-E-K9     58:ac:78:0f:32:cc  Halle 7.1a        DE          10.7.7.55          0       [0 ,0 ,0 ]
# H_007.1a_AP_153      2     AIR-CAP3702E-E-K9     58:ac:78:34:1e:54  Halle 7.1a        DE          10.7.7.56          0       [0 ,0 ,0 ]
# H_007.1a_AP_155      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:14  Halle 7.1a        DE          10.7.7.57          0       [0 ,0 ,0 ]
# H_007.1a_AP_154      2     AIR-CAP3702E-E-K9     58:ac:78:34:21:28  Halle 7.1a        DE          10.7.7.58          0       [0 ,0 ,0 ]
# H_007.1a_AP_50       2     AIR-CAP3702E-E-K9     58:ac:78:15:94:48  Halle 7.1a        DE          10.7.7.64          0       [0 ,0 ,0 ]
# H_007.1a_AP_78       2     AIR-CAP3702E-E-K9     70:e4:22:e5:13:20  Halle 7.1a        DE          10.7.7.66          0       [0 ,0 ,0 ]
# H_007.1a_AP_80       2     AIR-CAP3702E-E-K9     58:ac:78:34:20:44  Halle 7.1a        DE          10.7.7.67          0       [0 ,0 ,0 ]
# H_007c_ZE1_AP_880    2     AIR-CAP3702I-E-K9     00:81:c4:cc:6e:24  ZE1-301 Foyer 7c  DE          10.7.7.68          0       [0 ,0 ,0 ]
# H_007b_ZE1_AP_879    2     AIR-CAP3702I-E-K9     00:2a:10:01:2c:f0  ZE1-201 Foyer 7b  DE          10.7.7.69          0       [0 ,0 ,0 ]
# H_006.1-007.1c_UG_AP_596  2     AIR-CAP3702E-E-K9     00:81:c4:3a:a9:60  Ebene1 ÜG Auße  DE          10.7.7.71          0       [0 ,0 ,0 ]
# H_007.2a-007.2b_UG_AP_905  2     AIR-CAP3702I-E-K9     00:2a:10:02:45:cc  Übergang 7.2a/7  DE          10.7.7.78          0       [0 ,0 ,0 ]
# H_007.1b-007.1c_UG_AP_843  2     AIR-CAP3702I-E-K9     00:81:c4:cc:6e:b4  Übergang 7.1b/7  DE          10.7.7.73          0       [0 ,0 ,0 ]
# H_007.1b-007.1c_UG_AP_842  2     AIR-CAP3702I-E-K9     00:81:c4:c3:5a:e0  Übergang 7.1b/7  DE          10.7.7.80          0       [0 ,0 ,0 ]
# H_007.2a-007.2b_UG_AP_906  2     AIR-CAP3702I-E-K9     00:81:c4:e9:90:a8  Übergang 7.2a/7  DE          10.7.7.81          0       [0 ,0 ,0 ]
# H_007.1c_AP_277      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:1c  Halle 7.1c        DE          10.7.7.82          0       [0 ,0 ,0 ]
# H_007.2b_AP_217      2     AIR-CAP3702E-E-K9     58:ac:78:15:93:a8  Halle 7.2b        DE          10.7.7.95          0       [0 ,0 ,0 ]
# H_007.2b_AP_289      2     AIR-CAP3702E-E-K9     58:ac:78:34:23:ec  Halle 7.2b        DE          10.7.7.96          0       [0 ,0 ,0 ]
# H_007.1c_AP_311      2     AIR-CAP3702E-E-K9     58:ac:78:00:06:60  Halle 7.1c        DE          10.7.7.84          0       [0 ,0 ,0 ]
# H_007.2b_AP_287      2     AIR-CAP3702E-E-K9     58:ac:78:15:93:d0  Halle 7.2b        DE          10.7.7.102         0       [0 ,0 ,0 ]
# H_007.1c_AP_310      2     AIR-CAP3702E-E-K9     58:ac:78:34:1f:74  Halle 7.1c        DE          10.7.7.85          0       [0 ,0 ,0 ]
# H_007.2b_AP_114      2     AIR-CAP3702E-E-K9     70:e4:22:e5:13:e8  Halle 7.2b        DE          10.7.7.86          0       [0 ,0 ,0 ]
# H_007.1c_AP_303      2     AIR-CAP3702E-E-K9     58:ac:78:0f:33:a8  Halle 7.1c        DE          10.7.7.87          0       [0 ,0 ,0 ]
# H_007.2b_AP_187      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:34  Halle 7.2b        DE          10.7.7.88          0       [0 ,0 ,0 ]
# H_007.1c_AP_290      2     AIR-CAP3702E-E-K9     58:ac:78:15:92:34  Halle 7.1c        DE          10.7.7.89          0       [0 ,0 ,0 ]
# H_007.2b_AP_282      2     AIR-CAP3702E-E-K9     58:ac:78:15:92:d0  Halle 7.2b        DE          10.7.7.91          0       [0 ,0 ,0 ]
# H_007.1c_AP_286      2     AIR-CAP3702E-E-K9     58:ac:78:12:73:b0  Halle 7.1c        DE          10.7.7.92          0       [0 ,0 ,0 ]
# H_007.1c_AP_288      2     AIR-CAP3702E-E-K9     58:ac:78:00:07:20  Halle 7.1c        DE          10.7.7.42          0       [0 ,0 ,0 ]
# H_007.2b_AP_284      2     AIR-CAP3702E-E-K9     58:ac:78:34:20:98  Halle 7.2b        DE          10.7.7.103         0       [0 ,0 ,0 ]
# H_007.2b_AP_285      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2e:fc  Halle 7.2b        DE          10.7.7.100         0       [0 ,0 ,0 ]
# H_007.1c_AP_291      2     AIR-CAP3702E-E-K9     58:ac:78:34:1f:ec  Halle 7.1c        DE          10.7.7.41          0       [0 ,0 ,0 ]
# H_007.1c_AP_280      2     AIR-CAP3702E-E-K9     58:ac:78:12:73:74  Halle 7.1c        DE          10.7.7.83          0       [0 ,0 ,0 ]
# H_007.2b_AP_8        2     AIR-CAP3702E-E-K9     58:ac:78:00:11:b8  Halle 7.2b        DE          10.7.7.90          0       [0 ,0 ,0 ]
# H_007c_ZE2_AP_917    2     AIR-CAP3702I-E-K9     00:2a:10:01:2d:64  ZE2-301 Foyer 7c  DE          10.7.7.31          0       [0 ,0 ,0 ]
# H_007a_ZE2_AP_916    2     AIR-CAP3702I-E-K9     00:81:c4:c8:cb:50  ZE2-101 Foyer 7a  DE          10.7.7.52          0       [0 ,0 ,0 ]
# H_007.2b-007.2c_UG_AP_907  2     AIR-CAP3702I-E-K9     00:81:c4:cc:6d:98  Übergang 7.2b/7  DE          10.7.7.51          0       [0 ,0 ,0 ]
# H_007.2b-007.2c_UG_AP_908  2     AIR-CAP3702I-E-K9     00:81:c4:ca:62:34  Übergang 7.2b/7  DE          10.7.7.53          0       [0 ,0 ,0 ]
# H_007.3_AP_235       2     AIR-CAP3702E-E-K9     58:ac:78:0f:32:58  Halle 7.3         DE          10.7.7.54          0       [0 ,0 ,0 ]
# H_007.2c_AP_209      2     AIR-CAP3702E-E-K9     58:ac:78:34:30:50  Halle 7.2c        DE          10.7.7.97          0       [0 ,0 ,0 ]
# H_007.2c_AP_222      2     AIR-CAP3702E-E-K9     58:ac:78:15:92:f0  Halle 7.2c        DE          10.7.7.60          0       [0 ,0 ,0 ]
# H_007.3_AP_160       2     AIR-CAP3702E-E-K9     58:ac:78:12:74:e8  Halle 7.3         DE          10.7.7.59          0       [0 ,0 ,0 ]
# H_007.3_AP_234       2     AIR-CAP3702E-E-K9     70:e4:22:e5:13:34  Halle 7.3         DE          10.7.7.61          0       [0 ,0 ,0 ]
# H_007.2c_AP_146      2     AIR-CAP3702E-E-K9     58:ac:78:15:92:20  Halle 7.2c        DE          10.7.7.101         0       [0 ,0 ,0 ]
# H_007.3_AP_179       2     AIR-CAP3702E-E-K9     58:ac:78:15:92:64  Halle 7.3         DE          10.7.7.62          0       [0 ,0 ,0 ]
# H_007.2c_AP_211      2     AIR-CAP3702E-E-K9     58:ac:78:0f:3d:48  Halle 7.2c        DE          10.7.7.63          0       [0 ,0 ,0 ]
# H_007.3_AP_85        2     AIR-CAP3702E-E-K9     58:ac:78:34:20:48  Halle 7.3         DE          10.7.7.65          0       [0 ,0 ,0 ]
# H_007.2c_AP_7        2     AIR-CAP3702E-E-K9     58:ac:78:34:2f:e8  Halle 7.2c        DE          10.7.7.98          0       [0 ,0 ,0 ]
# SCH7_Garderobe_DG_E02_AP_928  2     AIR-CAP3702I-E-K9     00:81:c4:d7:0f:d0  Ebene2 Foyer SCH  DE          10.7.7.94          0       [0 ,0 ,0 ]
# H_007.2c_AP_208      2     AIR-CAP3702E-E-K9     58:ac:78:34:30:60  Halle 7.2c        DE          10.7.7.105         0       [0 ,0 ,0 ]
# H_007.3_AP_176       2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:0c  Halle 7.3         DE          10.7.7.106         0       [0 ,0 ,0 ]
# SCH7_Windfang_E02_AP_929  2     AIR-CAP3702I-E-K9     00:81:c4:ca:5f:dc  Ebene2 Foyer SCH  DE          10.7.7.104         0       [0 ,0 ,0 ]
# H_007.2c_AP_224      2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:e8  Halle 7.2c        DE          10.7.7.108         0       [0 ,0 ,0 ]
# SCH7_Garderobe_DG_E02_AP_927  2     AIR-CAP3702I-E-K9     00:2a:10:02:47:38  Ebene2 Foyer SCH  DE          10.7.7.107         0       [0 ,0 ,0 ]
# H_007.3_AP_87        2     AIR-CAP3702E-E-K9     58:ac:78:0a:2f:dc  Halle 7.3         DE          10.7.7.109         0       [0 ,0 ,0 ]
# H_007.2c_AP_213      2     AIR-CAP3702E-E-K9     58:ac:78:34:20:e0  Halle 7.2c        DE          10.7.7.112         0       [0 ,0 ,0 ]
# SCH7_Kassenhalle_E02_AP_730  2     AIR-CAP3702E-E-K9     00:81:c4:99:20:40  Ebene2 Foyer SCH  DE          10.7.7.110         0       [0 ,0 ,0 ]
# H_007.2c_AP_147      2     AIR-CAP3702E-E-K9     58:ac:78:0f:33:e0  Halle 7.2c        DE          10.7.7.114         0       [0 ,0 ,0 ]
# SCH7_Kassenhalle_E02_AP_731  2     AIR-CAP3702E-E-K9     00:81:c4:98:3f:c4  Ebene2 Foyer SCH  DE          10.7.7.113         0       [0 ,0 ,0 ]
# H_007.3a_FY_AP_924   2     AIR-CAP3702I-E-K9     00:81:c4:c8:cb:74  Ebene3 Foyer101   DE          10.7.7.111         0       [0 ,0 ,0 ]
# H_007.3a_FY_AP_923   2     AIR-CAP3702I-E-K9     00:2a:10:02:45:40  Ebene3 Foyer101   DE          10.7.7.115         0       [0 ,0 ,0 ]
# H_007.3_AP_173       2     AIR-CAP3702E-E-K9     58:ac:78:0f:33:00  Halle 7.3         DE          10.7.7.99          0       [0 ,0 ,0 ]
# H_004.2_AP_206       2     AIR-CAP3702E-E-K9     58:ac:78:0f:32:fc  Halle 4.2         DE          10.7.4.59          0       [0 ,0 ,0 ]
# H_001.2_AP_304       2     AIR-CAP3702E-E-K9     58:ac:78:0f:33:30  Halle 1.2         DE          10.7.2.56          0       [0 ,0 ,0 ]
# H_005.2a/006.2a_MF_AP_465  2     AIR-CAP3702E-E-K9     00:81:c4:9a:c0:7c  Halle 5.2a/6.2a_  DE          10.7.6.37          0       [0 ,0 ,0 ]
# AP1820-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:88  default location  DE          10.7.1.76          0       [0 ,0 ,0 ]
# AP1819-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c2:fa  default location  DE          10.7.1.80          0       [0 ,0 ,0 ]
# AP1821-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:ea  default location  DE          10.7.1.77          0       [0 ,0 ,0 ]
# AP1823-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c2:ec  default location  DE          10.7.1.79          0       [0 ,0 ,0 ]
# AP1824-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:c6  default location  DE          10.7.1.78          0       [0 ,0 ,0 ]
# AP1825-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:0c  default location  DE          10.7.1.81          0       [0 ,0 ,0 ]
# AP1822-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:06  default location  DE          10.7.1.82          0       [0 ,0 ,0 ]
# AP1832-3802e         2     AIR-AP3802E-E-K9      00:f6:63:4a:99:48  default location  DE          10.7.1.74          0       [0 ,0 ,0 ]
# AP1831-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c1:e4  default location  DE          10.7.1.54          0       [0 ,0 ,0 ]
# AP1828-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c2:0c  default location  DE          10.7.1.50          0       [0 ,0 ,0 ]
# AP1827-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c1:d2  default location  DE          10.7.1.49          0       [0 ,0 ,0 ]
# AP1829-3802e         2     AIR-AP3802E-E-K9      00:6b:f1:26:20:38  default location  DE          10.7.1.56          0       [0 ,0 ,0 ]
# AP1830-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:82  default location  DE          10.7.1.75          0       [0 ,0 ,0 ]
# AP1826-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:5e:2e:2e  default location  DE          10.7.1.73          0       [0 ,0 ,0 ]
# H_002.1_AP_141       2     AIR-CAP3702E-E-K9     58:ac:78:12:73:c8  Halle 2.1         DE          10.7.2.82          0       [0 ,0 ,0 ]
# H_002.1_AP_79        2     AIR-CAP3702E-E-K9     58:ac:78:15:93:dc  Halle 2.1         DE          10.7.2.75          0       [0 ,0 ,0 ]
# H_002.1_AP_103       2     AIR-CAP3702E-E-K9     58:ac:78:15:92:a4  Halle 2.1         DE          10.7.2.74          0       [0 ,0 ,0 ]
# H_002.1_AP_10        2     AIR-CAP3702E-E-K9     58:ac:78:12:7e:b8  Halle 2.1         DE          10.7.2.79          0       [0 ,0 ,0 ]
# H_002.1_AP_81        2     AIR-CAP3702E-E-K9     58:ac:78:15:93:70  Halle 2.1         DE          10.7.2.77          0       [0 ,0 ,0 ]
# H_002.1_AP_74        2     AIR-CAP3702E-E-K9     58:ac:78:12:74:a4  Halle 2.1         DE          10.7.2.78          0       [0 ,0 ,0 ]
# H_002.1_AP_106       2     AIR-CAP3702E-E-K9     58:ac:78:34:20:58  Halle 2.1         DE          10.7.2.80          0       [0 ,0 ,0 ]
# H_002.1_AP_28        3     AIR-CAP3702E-E-K9     58:ac:78:12:73:94  Halle 2.1         DE          10.7.2.83          0       [0 ,0 ,0 ]
# H_002.1_AP_196       3     AIR-CAP3702E-E-K9     70:e4:22:ff:23:08  Halle 2.1         DE          10.7.2.84          0       [0 ,0 ,0 ]
# H_002.1_AP_193       3     AIR-CAP3702E-E-K9     58:ac:78:34:1e:28  Halle 2.1         DE          10.7.2.85          0       [0 ,0 ,0 ]
# H_002.1_AP_111       3     AIR-CAP3702E-E-K9     58:ac:78:34:20:68  Halle 2.1         DE          10.7.2.86          0       [0 ,0 ,0 ]
# H_007.2a_AP_163      2     AIR-CAP3702E-E-K9     58:ac:78:34:1e:74  Halle 7.2a        DE          10.7.7.72          0       [0 ,0 ,0 ]
# H_003.2/4.2-005.2/6.2_UG_AP_464  2     AIR-CAP3702E-E-K9     00:81:c4:99:1d:94  Ebene2 MF ÜG Au  DE          10.7.4.37          0       [0 ,0 ,0 ]
# H_003.2/004.2_MF_AP_889  2     AIR-CAP3702I-E-K9     00:81:c4:ca:61:34  Halle 3.2/4.2 ZA  DE          10.7.4.38          0       [0 ,0 ,0 ]
# H_003.1/004.1_MF_AP_822  2     AIR-CAP3702I-E-K9     00:81:c4:cc:6e:1c  Halle 3.1/4.1_MF  DE          10.7.4.39          0       [0 ,0 ,0 ]
# H_003/4-005/6_UG_ZE1_AP_856  2     AIR-CAP3702I-E-K9     00:81:c4:c8:cb:c0  ZE1 ÜG 3/4 - 5/  DE          10.7.4.40          0       [0 ,0 ,0 ]
# H_003/004_ZE1_AP_853  2     AIR-CAP3702I-E-K9     00:81:c4:c3:5c:14  ZE1 ZA3/4_Mitte   DE          10.7.4.41          0       [0 ,0 ,0 ]
# H_003b/004b_MF_ZE1_AP_851  2     AIR-CAP3702I-E-K9     00:81:c4:e9:91:14  ZE1 MF_ZA3-4_B-S  DE          10.7.4.124         0       [0 ,0 ,0 ]
# H_003b/004b_MF_ZE1_AP_852  2     AIR-CAP3702I-E-K9     00:81:c4:cc:6e:ac  ZE1 MF_ZA3-4_B-S  DE          10.7.4.126         0       [0 ,0 ,0 ]
# H_003.2b/004.2b_MF_AP_468  2     AIR-CAP3702E-E-K9     00:81:c4:98:27:98  Halle 3.2b/4.2b_  DE          10.7.4.127         0       [0 ,0 ,0 ]
# H_003.2b/004.2b_MF_AP_467  2     AIR-CAP3702E-E-K9     00:81:c4:99:1f:24  Halle 3.2b/4.2b_  DE          10.7.4.145         0       [0 ,0 ,0 ]
# H_003.1b/004.1b_MF_AP_821  2     AIR-CAP3702I-E-K9     00:2a:10:02:47:20  Halle 3.1/4.1_MF  DE          10.7.4.146         0       [0 ,0 ,0 ]
# AP1834-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:ba  default location  DE          10.7.1.84          0       [0 ,0 ,0 ]
# AP1838-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:5e:07:a2  default location  DE          10.7.1.83          0       [0 ,0 ,0 ]
# AP1836-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:7c  default location  DE          10.7.1.33          0       [0 ,0 ,0 ]
# AP1835-3802e         2     AIR-AP3802E-E-K9      00:6b:f1:26:23:0e  default location  DE          10.7.1.32          0       [0 ,0 ,0 ]
# AP1839-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c3:08  default location  DE          10.7.1.35          0       [0 ,0 ,0 ]
# AP1833-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:a9:c3:18  default location  DE          10.7.1.31          0       [0 ,0 ,0 ]
# AP1837-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:d0  default location  DE          10.7.1.34          0       [0 ,0 ,0 ]
# AP1849-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:f0  default location  DE          10.7.1.93          0       [0 ,0 ,0 ]
# AP1845-3802e         2     AIR-AP3802E-E-K9      a0:3d:6f:5e:07:b0  default location  DE          10.7.1.90          0       [0 ,0 ,0 ]
# AP1846-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:e9:ac  default location  DE          10.7.1.95          0       [0 ,0 ,0 ]
# AP1847-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:33:ea:0e  default location  DE          10.7.1.96          0       [0 ,0 ,0 ]
# AP1850-3802e         2     AIR-AP3802E-E-K9      a0:e0:af:34:1d:62  default location  DE          10.7.1.94          0       [0 ,0 ,0 ]
# AP1851-3802e         2     AIR-AP3802E-E-K9      2c:d0:2d:f8:10:12  default location  DE          10.7.1.91          0       [0 ,0 ,0 ]
# H_002.1_AP_195       2     AIR-CAP3702E-E-K9     58:ac:78:0a:30:78  Halle 2.1         DE          10.7.2.170         0       [0 ,0 ,0 ]
# AP1848-3802e         2     AIR-AP3802E-E-K9      28:6f:7f:06:cf:40  default location  DE          10.7.1.92          0       [0 ,0 ,0 ]
# garbage
#
# <more garbage>
# '''
# ap_list = [line.split()[0] for line in output.splitlines()]

ap_data_re = re.compile(
        r"(\w.+?)\s.*(([0-9a-f]{2}[:-]){5}([0-9a-f]{2}))\s.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

if __name__ == '__main__':
    wlc_list = [INITIAL_WLC, END_WLC]
    wlcs = WlcInventory()
    wlcs.connect_to_many(wlc_list)
    output = wlcs.send_instruction(INITIAL_WLC, ['show ap summary'])[0]

    # match lines starting with APx, and grab AP name
    regex = [ap_data_re.match(line) for line in output.splitlines()]
    ap_list = [(ap_match.groups()[0], ap_match.groups()[1], ap_match.groups()[-1]) for ap_match in regex if
           ap_match is not None]
    commands = ['config ap primary-base {} {} {}'.format(END_WLC, ap[0], wlcs.wlcs[END_WLC]['ip']) for ap in ap_list]
    wlcs.send_instruction(INITIAL_WLC,commands)

