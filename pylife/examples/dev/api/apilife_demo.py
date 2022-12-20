# Path pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'

# Path file for API ids
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'

import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
import matplotlib.pyplot as plt

# %%

end_user        = '2S3Pth'
from_time       = "2022-05-30 18:30:00"
to_time         = "2022-05-30 18:33:00"
time_zone       = 'CEST'

activity_type   = 'Test'
project         = ''

params = {'path_ids': path_ids, 'api_version': 2,
          'end_user': end_user, 
          'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
          'device_model': 'tshirt',
          'flag_acc': True, 'flag_breath': True, 
          'flag_ecg': True, 'flag_temp': True, 'flag_temp_valid': False,
          'flag_imp': False,    
          'activity_types': activity_type,
          }

al = Apilife(params)
print('Getting...')
al.get()
print('Parsing...')
al.parse()

plt.close('all')
al.show()
plt.show()

