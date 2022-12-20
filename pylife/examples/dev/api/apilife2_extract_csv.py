# Path to API ids file
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'
# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'

import os
import sys
sys.path.append(path_root)
import pandas as pd
import numpy as np

from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
from pylife.useful import unwrap
from report.excel import create_report_folder
from report.excel import excel_report, excel_report_split

# %%

end_user        = "5YXjZB" # Medbase: 5qfYth, Skinup: 5YXjZB, Rowan: 4CDHyt 
date            = '2022-04-21'
from_time       = "00:45:00"
to_time         = "00:50:00"
time_zone       = 'CEST'

entity          = 'SkinUp' # CLIENT
device          = 'CST'

activity_type   = 'Day'
from_time       = date + ' ' + from_time
to_time         = date + ' ' + to_time

params = {'path_ids': path_ids, 'api_version': 2,
          'end_user': end_user, 
          'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
          'device_model': 'tshirt',
          'flag_acc': True, 'flag_breath': True, 
          'flag_ecg': True, 'flag_temp': True, 'flag_temp_valid': False,
          'flag_imp': True,    
          'activity_types': activity_type,
          }

al = Apilife(params)
print('Getting...')
al.get()
print('Parsing...')
al.parse()
print('filtering...')
al.filt()
print('cleaning...')
al.clean()
print('analysing...')
al.analyze()

# %%
window_time     = 1*60

# Folder where result will be saved
result_folder = os.getcwd()

# % Create folder to store result and get path_save 
path_save = create_report_folder(result_folder, entity, end_user, from_time, to_time, activity_type=activity_type)

# Generate xls report 
report = excel_report(al, verbose=1,
                        flag_clean=al.flag_clean_,
                        flag_analyze=al.flag_analyze_,
                        path_save=path_save)

report_ts = excel_report_split(al, window_time, path_save)

# %% Breath
acc_times       = unwrap(al.accx.times_)
accx            = unwrap(al.accx.sig_)
accy            = unwrap(al.accy.sig_)
accz            = unwrap(al.accz.sig_)
breath_times    = unwrap(al.breath_1.times_)
breath_1        = unwrap(al.breath_1.sig_filt_)
breath_2        = unwrap(al.breath_2.sig_filt_)
ecg_times       = unwrap(al.ecg.times_)
ecg             = unwrap(al.ecg.sig_filt_)
temp_times      = unwrap(al.temp_1.times_)
temp_1          = unwrap(al.temp_1.sig_filt_)
temp_2          = unwrap(al.temp_2.sig_filt_)

# %%
data = np.array([acc_times, accx, accy, accz])
df = pd.DataFrame(data.T, columns=['times', 'accx', 'accy', 'accz'])
df.to_csv(path_save + 'raw_data_acceleration.csv', sep=',', encoding='utf-8')

data = np.array([breath_times, breath_1, breath_2])
df = pd.DataFrame(data.T, columns=['times', 'thoracic_respiration', 'abdominal_respiration'])
df.to_csv(path_save + 'raw_data_respiration.csv', sep=',', encoding='utf-8')

data = np.array([ecg_times, ecg])
df = pd.DataFrame(data.T, columns=['times', 'ecg'])
df.to_csv(path_save + 'raw_data_ecg.csv', sep=',', encoding='utf-8')

data = np.array([temp_times, temp_1, temp_2])
df = pd.DataFrame(data.T, columns=['times', 'right_temperature', 'left_temperature'])
df.to_csv(path_save + 'raw_data_temperature.csv', sep=',', encoding='utf-8')

