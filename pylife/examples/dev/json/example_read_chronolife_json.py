path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'
import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
# Add other imports
from pylife.data_manager.datalife import Jsonlife

# ----- Load data -----
path_data = path_root + '/pylife/data/chronolife/tshirt/'
file_name = '20200417_0919_fRbLJaqJR_FFoOiZzHJron0q7BkeWlqBfcH_f3-_FPs.json'
path_file = path_data + file_name 

params = {'path': path_file,
          'rm_db': 0, # remove double data: 1 = yes, 0 = no 
          'flag_acc': True, 
          'flag_breath': True, 
          'flag_ecg': True, 
          'flag_temp': True,
          # 'tmin': np.datetime64('2020-04-16T18:45:00'), # min datetime target
          # 'tmax': np.datetime64('2020-04-16T18:50:00'), # max datetime target
          }

jsl = Jsonlife(params)  
jsl.parse()