# Path to API ids file
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'
# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'

import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
import json
from pylife.api_functions import get_ids
from pylife.api_v2_functions import get


user, token, url  = get_ids(path_ids=path_ids)
date            = "2022-04-08"
from_time       = "09:15:00"
to_time         = "09:20:00"
end_user        = "5YXjZB"

types   =   'accx,accy,accz,breath_1,breath_2,ecg,temp_1,temp_2,imp,'\
            'ecg_filtered,breath_1_filtered,breath_2_filtered,ecg_quality_index,'\
            'heartbeat,HRV,heartbeat_quality_index,HRV_quality_index,'\
            'rr_interval,sdnn,rmssd,pnn50,'\
            'respiratory_rate,respiratory_rate_quality_index,'\
            'averaged_temp_1,averaged_temp_2,'\
            'activity_level,averaged_activity,steps_number' 

datas = get(token, url, end_user, date, from_time, to_time, types=types)

# %%

with open('data.json', 'w') as outfile:
    json.dump(datas, outfile)
