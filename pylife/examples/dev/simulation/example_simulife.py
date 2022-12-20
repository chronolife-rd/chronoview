path_root = 'C:/Users/MichelClet/Desktop/Files/pylife'
import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Simulife
import matplotlib.pyplot as plt

# %%

path_data = 'C:/Users/MichelClet/Desktop/Files/data/simul/'
params = {'path_data': path_data, 'device_model': 't-shirt',
          'flag_acc': True, 'flag_breath': True, 
          'flag_ecg': True, 'flag_temp': True, 'flag_imp': False,
          'flag_1seg': True, 'flag_clean_temp': True,
          'flag_disconnection': False, 'flag_clean_acc': True,
          'flag_clean_breath': True, 'flag_clean_ecg': True
          }
 
sl = Simulife(params)
print('loading...')
sl.parse()

plt.close('all')
sl.show()

# %%
print('cleaning...')
sl.filt()
sl.clean()
# sl.breath_2.show(on_sig='filt', color='C0', show_indicators='clean')

plt.close('all')
sl.ecg.show(on_sig='raw', color='C0',show_indicators='clean')

# %%
print('analyzing...')
sl.analyze()

# %%
print(sl.ecg.hrv_)