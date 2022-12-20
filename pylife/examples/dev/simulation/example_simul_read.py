import sys
path_root = 'C:/Users/MichelClet/Desktop/Files'
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()

from pylife.datalife import Apilife

import numpy as np
import pickle
import matplotlib.pyplot as plt
from pylife.siglife import Accelerations

# %%
path_data = path_root + '/data/simul/'
flag_1seg = False
flag_disconnection = True
flag_clean_acc = False
flag_clean_breath = True
flag_clean_ecg = False
flag_clean_temp = False

savefilename = ['1seg_','disco_', 'acc_', 'breath_', 'ecg_', 'temp']
if not flag_1seg:
    savefilename[0] = 'no-' + savefilename[0]
if not flag_disconnection:
    savefilename[1] = 'no-' + savefilename[1]
if not flag_clean_acc:
    savefilename[2] = 'no-' + savefilename[2]
if not flag_clean_breath:
    savefilename[3] = 'no-' + savefilename[3]
if not flag_clean_ecg:
    savefilename[4] = 'no-' + savefilename[4]
if not flag_clean_temp:
    savefilename[5] = 'no-' + savefilename[5]
savefilename = ''.join(savefilename)
        
with open((path_data + savefilename + '.pkl'), 'rb') as file:
    data = pickle.load(file)
    
# %% siglife classes
accx = data['accx']
accy = data['accy']
accz = data['accz']
acc = Accelerations(accx, accy, accz)
breath = data['breath']
ecg = data['ecg']
temp = data['temp']
imp = data['imp']

# %%
ecg.show()