path_root = 'C:/Users/MichelClet/Desktop/Files/'
import sys
sys.path.append(path_root)
# --- Set/get DEV env
from pylife.env import get_env
DEV = get_env()
# --- Add other imports
from pylife.datalife import Jsonlife
import matplotlib.pyplot as plt

# %% ----- Set data path and file info
path_data = 'C:/Users/MichelClet/Downloads/datafiles/'
file_name = '2sgzQu_2021-10-22.json'
path_file = path_data + file_name

# %% ----- Set Jsonlife parameters 
params = {'path': path_file,
          'rm_db': 1,               # remove double data: 1 = yes, 0 = no 
          'flag_acc':           True,         # flag for loading acceleration signals
          'flag_breath':        True,      # flag for loading breath signals
          'flag_ecg':           True,         # flag for loading ecg signal
          'flag_temp':          False,        # flag for loading temperature signals
          'flag_temp_valid':    True,  # flag for loading temperature valid signals
          }

# %% ----- Create new instance of Jsonlife
jsl = Jsonlife(params)  

# %% ----- Load all signals with True flag
jsl.parse()

# %% ----- Show all signals loaded on raw signals (original signals)
plt.close('all')
jsl.show(on_sig='raw')

# %% ----- Show ecg only, on raw signal
jsl.show(signal_type='ecg', on_sig='raw')

# %% ----- Show breath_1 only, on a specific segment of raw signal
jsl.show(signal_type='breath_1', id_seg=0, on_sig='raw')

# %% ----- Show all signals with colored segment to identify segments sizes and disconnections  
jsl.show_unwrap_colors(on_sig='raw')

# %% ----- Show accx only, with colored segment to identify segments sizes and disconnections  
jsl.show_unwrap_colors(signal_type='accx', on_sig='raw')

# %% ----- Clean signals (remove noise, filter, etc.)
jsl.filt()
jsl.clean()

# %% ----- Show ecg on filtered signal 1st segment
jsl.show(signal_type='ecg', id_seg=0, on_sig='filt')

# %% ----- Show ecg on filtered signal 1st segment with indicators of clean data
jsl.show(signal_type='ecg', on_sig='filt', flag_indicators=True)

# %% ----- Show breath_2 on cleaned signal 1st segment
jsl.show(signal_type='breath_2', id_seg=0, on_sig='clean')

# %% ----- Analyze on clean signal (number of steps, breaths bpm, ECG bpm)
jsl.analyze(on_sig='clean')

# %% ----- Extract signal classes (Siglife type)
accx = jsl.accx
accy = jsl.accy
accz = jsl.accz
breath_1 = jsl.breath_1
breath_2 = jsl.breath_2
ecg = jsl.ecg


