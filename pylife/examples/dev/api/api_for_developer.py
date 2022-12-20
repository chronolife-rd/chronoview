import sys
path_pylife = 'C:/Users/MichelClet/Desktop/Files/pylife'
sys.path.append(path_pylife)
from pylife.env import get_env
DEV = get_env()

import numpy as np
from pylife.api_functions import test_login_with_token
from pylife.api_functions import get_ids
from pylife.api_functions import find
from pylife.api_functions import map_data
from pylife.api_functions import map_data_filt
from pylife.api_functions import map_results
from pylife.api_functions import map_data_app
from pylife.api_functions import get_sig_info
from pylife.api_functions import get_result_info
from pylife.api_functions import get_app_info


# %% POST. Login with token
path_api_ids = 'C:/Users/MichelClet/Desktop/Files/mcl/api/prod'
user, token, url = get_ids(path_api_ids)
test_login_with_token(url, user, token)

from_time       = "2021-01-14 10:00:00" # UTC TIME
to_time         = "2021-01-14 10:01:00" # UTC TIME
end_users       = "4G53AC" # 

types = ['accx', 'accy', 'accz', 'breath_1', 'breath_2', 'ecg', 
         'temp_1', 'temp_2', 'temp_1_valid', 'temp_2_valid', 'imp',
          'ecg_filtered', 'breath_1_filtered', 'breath_2_filtered', 'ecg_quality_index',
          'heartbeat', 'HRV', 'heartbeat_quality_index', 'HRV_quality_index',
          'respiratory_rate', 'respiratory_rate_quality_index',          
          'activity_level', 'steps_number', 
          ]
         
# --- Find data in database
datas = find(user, token, url, end_users, from_time, to_time, types=types, verbose=1)
# --- Map data 
datas_mapped = map_data(datas, types)
# --- Map data filtered
datas_filtered_mapped = map_data_filt(datas, types)
# --- Map results
results_mapped = map_results(datas, types)
# --- Map data app info
app_info_mapped = map_data_app(datas, types)

print('Number of data events', len(datas_mapped['users'][0]['data']))
print('Number of data filtered events', len(datas_filtered_mapped['users'][0]['data']))
print('Number of results events', len(results_mapped['users'][0]['data']))
print('Number of app info events', len(app_info_mapped['users'][0]['data']))
    
data_types = []
for data in datas_mapped['users'][0]['data']:
    data_types.append(data['type'])
print(np.unique(data_types))

#%% Signals
# Acceleration
accx_info = get_sig_info(datas_mapped, 'accx', verbose=0)
accy_info = get_sig_info(datas_mapped, 'accy', verbose=0)
accz_info = get_sig_info(datas_mapped, 'accz', verbose=0)

# Breath
breath_1_info = get_sig_info(datas_mapped, 'breath_1_filtered', verbose=0)
breath_2_info = get_sig_info(datas_mapped, 'breath_2', verbose=0)

# ECG
ecg_info = get_sig_info(datas_mapped, 'ecg', verbose=0)

# Temperature
temp_1_info = get_sig_info(datas_mapped, 'temp_1', verbose=0)
temp_2_info = get_sig_info(datas_mapped, 'temp_2', verbose=0)

# Temperature
temp_1_valid_info = get_sig_info(datas_mapped, 'temp_1_valid', verbose=0)
temp_2_valid_info = get_sig_info(datas_mapped, 'temp_2_valid', verbose=0)

# Pulmonary Impedance
imp_1_info = get_sig_info(datas_mapped, 'imp_1', verbose=0)
imp_2_info = get_sig_info(datas_mapped, 'imp_2', verbose=0)
imp_3_info = get_sig_info(datas_mapped, 'imp_3', verbose=0)
imp_4_info = get_sig_info(datas_mapped, 'imp_4', verbose=0)

# %%  Signals filtered
ecg_filt_info       = get_sig_info(datas=datas_filtered_mapped, signal_type='ecg_filtered')
breath_1_filt_info  = get_sig_info(datas=datas_filtered_mapped, signal_type='breath_1_filtered')
breath_2_filt_info  = get_sig_info(datas=datas_filtered_mapped, signal_type='breath_2_filtered')

# %% Results
ecg_quality_info                = get_result_info(datas=results_mapped, result_type='ecg_quality_index')
heartbeat_info                  = get_result_info(datas=results_mapped, result_type='heartbeat')
heartbeat_quality_info          = get_result_info(datas=results_mapped, result_type='heartbeat_quality_index')
HRV_info                        = get_result_info(datas=results_mapped, result_type='HRV')
HRV_quality_info                = get_result_info(datas=results_mapped, result_type='HRV_quality_index')
respiratory_rate_info           = get_result_info(datas=results_mapped, result_type='respiratory_rate')
respiratory_rate_quality_info   = get_result_info(datas=results_mapped, result_type='respiratory_rate_quality_index')
activity_level_info             = get_result_info(datas=results_mapped, result_type='activity_level')
steps_number_info               = get_result_info(datas=results_mapped, result_type='steps_number')

# %% App info
battery         = get_app_info(datas=app_info_mapped, result_type='battery')
ble             = get_app_info(datas=app_info_mapped, result_type='ble_disconnected')
notification    = get_app_info(datas=app_info_mapped, result_type='notification')