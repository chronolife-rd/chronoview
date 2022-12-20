# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'
# Path to API ids file
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'

import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()

from pylife.datalife import Apilife
from pylife.process_functions import process_data_interval

# %% Load data

# Request info
from_time       = "2022-01-18 14:00:00"
to_time         = "2022-01-18 14:05:00"
time_zone       = 'CET'
end_user        = "4veCS1"
dict_params         = {}
dict_params['api']  = {'path_ids': path_ids, 'end_user': end_user, 'api_version': 2,
                       'from_time': from_time, 'to_time': to_time, 
                       'time_zone': time_zone, 'device_model': 't-shirt',
                       'flag_acc': True, 'flag_breath': True, 
                       'flag_ecg': True, 'flag_temp': True}
al = Apilife(dict_params['api'])
al.get()
al.parse()
# al.filt()
# al.clean()
# al.analyze()

# %% Define parameters
dict_params              = {}
dict_params['accx']      = {'times':        al.accx.times_, 
                            'sig':          al.accx.sig_, 
                            'fs':           al.accx.fs_, 
                            'fw_version':   al.accx.fw_version_}

dict_params['accy']      = {'times':        al.accy.times_, 
                            'sig':          al.accy.sig_, 
                            'fs':           al.accy.fs_, 
                            'fw_version':   al.accy.fw_version_}

dict_params['accz']      = {'times':        al.accz.times_, 
                            'sig':          al.accz.sig_, 
                            'fs':           al.accz.fs_, 
                            'fw_version':   al.accz.fw_version_}

dict_params['breath_1']  = {'times':        al.breath_1.times_, 
                            'sig':          al.breath_1.sig_, 
                            'fs':           al.breath_1.fs_,
                            'fw_version':   [al.breath_1.fw_version_]}

dict_params['breath_2']  = {'times':        al.breath_2.times_, 
                            'sig':          al.breath_2.sig_, 
                            'fs':           al.breath_2.fs_, 
                            'fw_version':   al.breath_2.fw_version_}

dict_params['ecg']       = {'times':        al.ecg.times_, 
                            'sig':          al.ecg.sig_, 
                            'fs':           al.ecg.fs_, 
                            'fw_version':   al.ecg.fw_version_}

dict_params['temp_1']    = {'times':        al.temp_1.times_, 
                            'sig':          al.temp_1.sig_, 
                            'fs':           al.temp_1.fs_, 
                            'fw_version':   al.temp_1.fw_version_}

dict_params['temp_2']    = {'times':        al.temp_2.times_, 
                            'sig':          al.temp_2.sig_, 
                            'fs':           al.temp_2.fs_,
                            'fw_version':   al.temp_2.fw_version_}

# % Process data
dict_result = process_data_interval(dict_params)

# %%
print()
print(from_time, '==>' ,to_time)
print('')
print('steps_number             ', dict_result["steps_number"])
print('averaged_activity        ', dict_result["averaged_activity"])
print('')
print('breath quality index     ', dict_result["respiratory_rate"])
print('respiratory_rate         ', dict_result["respiratory_rate"])
print('')
print('heartbeat quality index  ', dict_result["heartbeat_quality_index"])
print('hrv quality index        ', dict_result["HRV_quality_index"])
print('heartbeat                ', dict_result["heartbeat"])
print('HRV                      ', dict_result["HRV"])
print('RR interval              ', dict_result["rr_interval"])
print('sdnn                     ', dict_result["sdnn"])
print('rmssd                    ', dict_result["rmssd"])
print('lnrmssd                  ', dict_result["lnrmssd"])
print('pnn50                    ', dict_result["pnn50"])
print('')
print('averaged_temp_1          ', dict_result["averaged_temp_1"])
print('averaged_temp_2          ', dict_result["averaged_temp_2"])
