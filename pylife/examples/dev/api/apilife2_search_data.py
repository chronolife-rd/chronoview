# Path to pylife
path_root = 'C:/Users/MichelClet/Desktop/mcl/python/'
# Path to API ids file
path_ids = 'C:/Users/MichelClet/Desktop/mcl/api/v2/prod/'

import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
import numpy as np
import pandas as pd
from pylife.api_v2_functions import get
from pylife.api_functions import get_ids
from pylife.api_functions import map_results
from pylife.api_functions import get_result_info
from pylife.api_functions import time_shift
from pylife.useful import unwrap

# %% Build the query parameters object.

user, token, url  = get_ids(path_ids=path_ids)

from_date   = "2022-06-05"
to_date     = "2022-06-10"
end_users   = ['7fbCwc'] 
utc_offset  = 0


# %%
days_s                  = []
starts_s                = []
ends_s                  = []
durations_s             = []
heartbeat_qualitys_s    = []
activity_means_s        = []
activity_stds_s         = []
user_ids_s              = []
ref_clients_s           = []

print('Search for T-shirt activation between', from_date, 'and', to_date)
for ie, end_user in enumerate(end_users):
    from_time       = "00:00:00"
    to_time         = "23:59:00"
    types           = 'heartbeat_quality_index,averaged_temp_1'
    
    from_date64 = np.datetime64(from_date) 
    to_date64   = np.datetime64(to_date) 
    dates       = np.arange(from_date64, to_date64 + np.timedelta64(1, 'D'))
    
    days                = []
    starts              = []
    ends                = []
    starts_worn         = []
    ends_worn           = []
    durations           = []
    durations_worn      = []
    heartbeat_qualitys  = []
    for it, date in enumerate(dates):
        
        # day
        datas = get(token, url, end_user, date, from_time, to_time, types=types)

        t1 = time_shift(str(date) + ' ' + from_time, -utc_offset, time_format='h') 
        previous_date = np.datetime64(t1[:10])
        previous_from_time = t1[11:]
        # day - 1
        datas.extend(get(token, url, end_user, previous_date, previous_from_time, to_time, types=types))
                
        if len(datas) > 0:
            
            results_mapped          = map_results(datas, types)
            heartbeat_quality_info  = get_result_info(datas=results_mapped, result_type='heartbeat_quality_index')
            temp_info               = get_result_info(datas=results_mapped, result_type='averaged_temp_1')
            
            hrq                     = unwrap(heartbeat_quality_info['values'])
            times                   = unwrap(heartbeat_quality_info['times'])
            temp                    = unwrap(temp_info['values'])
            
            if len(temp) > len(times):
                temp                    = temp[:len(times)]
            if len(temp) < len(times):
                for i in range(len(times)-len(temp)):
                    temp.append(np.nan)
                    
            array                   = np.array([times, hrq, temp])
            df                      = pd.DataFrame(array.T, columns=['times', 'hrq', 'temp'])
            df                      = df.sort_values(by='times')
            
            next_date = date + np.timedelta64(1, 'D')
            tmax = np.datetime64(str(next_date) + 'T' + '00:00:00')
            tmax = tmax - np.timedelta64(utc_offset, 'h')
            if len(df) == 0:
                continue
            df = df[df.times < tmax]
            
            timestamps              = df['times'].values.astype('datetime64[s]')
            hrqs                    = df['hrq'].values.astype('float')
            # acts                    = df['act'].values.astype('float')
            temps                   = df['temp'].values.astype('float')
            tdiff                   = (timestamps[1:] - timestamps[:-1])/np.timedelta64(1, 's')
            idiff                   = np.where(tdiff > 30*60)
            if len(idiff) > 0:
                idiff = idiff[0]+1
                timestamps_s    = np.split(timestamps, idiff)
                hrqs_s          = np.split(hrqs, idiff)
                temps_s         = np.split(temps, idiff)
            else:
                timestamps_s    = timestamps
                hrqs_s          = hrqs
                temps_s         = temps
            if len(timestamps_s[0]) == 0:
                continue
                
            for i in range(len(timestamps_s)):
                timestamps              = timestamps_s[i]
                hrq                     = hrqs_s[i]
                temp                    = temps_s[i]/100
                start                   = timestamps[0]
                end                     = timestamps[-1]
    
                minutes_total           = (end - start)/np.timedelta64(1, 'm')
                hours                   = int(minutes_total/60)
                minutes                 = int((minutes_total/60 - hours)*60)
                duration                = str(hours) + ':' + str(minutes)
                
                start                   = time_shift(str(start).replace('T', ' '), utc_offset, time_format='h') 
                end                     = time_shift(str(end).replace('T', ' '), utc_offset, time_format='h')
                
                temp_mean               = int(np.mean(temp))
                temp_std                = int(np.std(temp))
                
                iworn                   = np.where(temp > 30)[0]
                if len(iworn) > 1:
                    imin = iworn[0]
                    imax = iworn[-1]
                    timestamps_worn     = timestamps[iworn]
                    start_worn          = timestamps_worn[0]
                    end_worn            = timestamps_worn[-1]
        
                    minutes_total           = (end_worn - start_worn)/np.timedelta64(1, 'm')
                    hours                   = int(minutes_total/60)
                    minutes                 = int((minutes_total/60 - hours)*60)
                    duration_worn           = str(hours) + ':' + str(minutes)
                
                    start_worn                   = time_shift(str(start_worn).replace('T', ' '), utc_offset, time_format='h') 
                    end_worn                     = time_shift(str(end_worn).replace('T', ' '), utc_offset, time_format='h')
                    
                    hrq_mean                     = int(round(sum(hrq[iworn])/len(hrq[iworn])*100))
                else:
                    timestamps_worn = None
                    start_worn      = None
                    end_worn        = None
                    duration_worn   = None
                    hrq_mean        = None
                
                    
                if duration == '0:0':
                    continue
                
                days.append(str(date))
                starts.append(str(start)[11:-3])
                ends.append(str(end)[11:-3])
                starts_worn.append(str(start_worn)[11:-3])
                ends_worn.append(str(end_worn)[11:-3])
                durations.append(duration)
                durations_worn.append(duration_worn)
                heartbeat_qualitys.append(hrq_mean)
    
    
    print()
    print('-------', end_user, '-------')
    if len(days) == 0:
        print('No data found')
    else:
        for j in range(len(days)):
            print()
            print('Date         ', days[j])
            print('Tshirt allumé    UTC + ' + str(utc_offset) + ': ', starts[j], '-', ends[j], '(', durations[j], ')')
            if durations_worn[j] == None:
                print('Tshirt porté     Aucune données')
            else:
                print('Tshirt porté     UTC + ' + str(utc_offset) + ': ', starts_worn[j], '-', ends_worn[j], '(', durations_worn[j], ') - Heart rate quality:', heartbeat_qualitys[j], '%'
                      )
            
    user_ids_s.extend(np.repeat(end_user, len(days)))
    days_s.extend(days)
    starts_s.extend(starts)
    ends_s.extend(ends)
    durations_s.extend(durations)
    heartbeat_qualitys_s.extend(heartbeat_qualitys)
