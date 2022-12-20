path_root = '/home/claire/Desktop/pylife'
import sys
sys.path.append(path_root)
from pylife.env import get_env
DEV = get_env()
from pylife.datalife import Apilife
from pylife.useful import unwrap, is_list_of_list
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

# Path file for API ids
path_ids = '/home/claire/Desktop/prodv2'
path_save = '/home/claire/Desktop/'
name = "4veCS1_1801"

# Create dataframe containing relevant indicators
columnss = ['ts', 'Steps', 'RR', 'Min rr', 'Max rr', 'Var rr', 'pnn50', 'Bpm', 'Min bpm', 'Max bpm', 'Var bpm',
            'RR b1', 'Min rr b1', 'Max rr b1', 'Var rr b1','Rpm b1', 'Min rpm b1', 'Max rpm b1', 'Var rpm b1',
           'RR b2', 'Min rr b2', 'Max rr b2', 'Var rr b2', 'Rpm b2', 'Min rpm b2', 'Max rpm b2', 'Var rpm b2', 
           'Mean temp1', 'Mean temp2']
  
cecg = []
cbreath = []
for end_user in ["4veCS1"]: # "4wVX5v", "2EMrKQ", "38sQL3", "2EuiHN"]:
     # Request info
     from_time       = "2022-01-18 14:00:00"
     to_time         = "2022-01-18 14:05:00"
     time_zone       = 'CET'
     end_user        = end_user
     
     activity_type = 'Test'
     project = ''
     df_all = []
     while from_time < "2022-01-18 14:10:00":
         params = {'path_ids': path_ids, 'end_user': end_user, 
                   'from_time': from_time, 'to_time': to_time, 'time_zone': time_zone,
                   'device_model': 't-shirt',
                   'flag_acc': True, 'flag_breath': True,
                   'flag_ecg': True, 'flag_temp': True, 'flag_temp_valid': True,
                   'flag_imp': False, 
                   'activity_types': activity_type, 'api_version':2,
                   }
         df_ = []
         al = Apilife(params)
         
         al.get()
         al.parse()
         al.filt()
         al.clean()
         al.analyze()
         if not al.is_empty_:
             cecg.extend(al.ecg.indicators_clean_3_)
             
             cbreath.extend(al.breath_2.indicators_clean_)
         from_time = to_time
         to_time = str(np.datetime64(from_time)+np.timedelta64(5*60, 's')).replace("T", " ")
         
         
         if not al.is_empty_:
             
              if len(al.accx.sig_) >0:
                  steps = al.accx.steps_
                  if is_list_of_list(steps):
                    steps = unwrap(steps)
                  steps = np.sum(steps) 
              else:
                  steps = None
              rr = al.ecg.rr_
              if is_list_of_list(rr):
                rr = unwrap(rr)
                
              df_.append(from_time)
              df_.append(steps)
             
              if len(rr)>0:
                  df_.extend([al.ecg.bpm_ms_, np.min(rr), np.max(rr), al.ecg.bpm_var_ms_,  al.ecg.pnn50_[0]])
             
                  df_.extend([al.ecg.bpm_, 60/(np.max(rr)/1000), 60/(np.min(rr)/1000), al.ecg.bpm_var_])
                 
              else:
                  df_.extend([None, None, None, None, None])
                  df_.extend([None, None, None, None])
             
             
              rrb1 = al.breath_1.rr_
              if is_list_of_list(rrb1):
                rrb1 = unwrap(rrb1)
             
            
              if len(rrb1)>0:
                  df_.extend([al.breath_1.rpm_s_, np.min(rrb1), np.max(rrb1), al.breath_1.rpm_var_s_])
                  df_.extend([al.breath_1.rpm_, 60/np.max(rrb1), 60/np.min(rrb1), al.breath_1.rpm_var_])
              else:
                  df_.extend([None, None, None, None])
                  df_.extend([None, None, None, None])
         
              rrb2 = al.breath_2.rr_
              if is_list_of_list(rrb2):
                rrb2 = unwrap(rrb2)
          
             
              if len(rrb2)>0:
                  df_.extend([al.breath_2.rpm_s_, np.min(rrb2), np.max(rrb2), al.breath_2.rpm_var_s_])
                  df_.extend([al.breath_2.rpm_, 60/np.max(rrb2), 60/np.min(rrb2), al.breath_2.rpm_var_])
              else:
                  df_.extend([None, None, None, None])
                  df_.extend([None, None, None, None])
                 
              temp1 = al.temp_1.sig_
              if is_list_of_list(temp1):
                temp1 = unwrap(temp1)
              df_.append(np.mean(temp1)/100)
             
              temp2= al.temp_2.sig_
              if is_list_of_list(temp2):
                temp2 = unwrap(temp2)
              df_.append(np.mean(temp2)/100)
             
             
              df_all.append(df_)
             
file = pd.DataFrame(df_all, columns=columnss)
     
file.to_csv(path_save+name+".csv")   

         
#%%
##SAVE FIGS FOR DATA ANALYSIS REPORT
#

import seaborn as sns
sns.set_theme()


# RR

indic = 'rr'
file = pd.read_csv(path_save+name+".csv")
file['ts'] = file['ts'].apply(lambda x:str(x)[10:16])
fig, ax1 = plt.subplots()
ax = sns.lineplot(data=file, x="ts", y="RR", color='b', marker="o", label='RR')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 50, fontsize=7)
ax.set_xlabel('time')
ax.set(ylim=(0, 3000))
x = file['ts']
y1 = file['Min ' + indic]
y2 = file['Max ' + indic]
ax1.fill_between(x, y1, y2, alpha =0.2, color='b', label='HRV')
ax1.set_ylabel("RR (ms)")
ax2=ax1.twinx()
ax2.set_ylabel("Steps")
ax2.fill_between(x, file['Steps'], color='g', alpha=0.2, label='Steps')
ax2.set(ylim=(0, 500))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.rc('font', size=8)    
ax2.legend(lines1 +lines2, labels1+labels2, loc=0)
sns.set(font_scale=0.1)
plt.savefig(path_save+name + '_' + indic+'.png', orientation='landscape')

#bpm
sns.set_theme()
indic = 'bpm'
file = pd.read_csv(path_save+name+".csv")
file['ts'] = file['ts'].apply(lambda x:str(x)[10:16])
fig, ax1 = plt.subplots()
ax = sns.lineplot(data=file, x="ts", y="Bpm", color='b', marker="o", label='HR (bpm)')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 50, fontsize=7)
ax.set_xlabel('time')
ax.set(ylim=(0, 200))
x = file['ts']
y1 = file['Min ' + indic]
y2 = file['Max ' + indic]
ax1.fill_between(x, y1, y2, alpha =0.2, color='b', label='HRV')
ax1.set_ylabel("HR (bpm)")
ax2=ax1.twinx()
ax2.set_ylabel("Steps")
ax2.fill_between(x, file['Steps'], color='g', alpha=0.2, label='Steps')
ax2.set(ylim=(0, 500))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.rc('font', size=8)    
ax2.legend(lines1 +lines2, labels1+labels2, loc=0)
plt.savefig(path_save+name + '_' + indic+'.png', orientation='landscape')


# RPM b1

sns.set_theme()
indic = 'rpm b1'
file = pd.read_csv(path_save+name+".csv")
file['ts'] = file['ts'].apply(lambda x:str(x)[10:16])
fig, ax1 = plt.subplots()
ax = sns.lineplot(data=file, x="ts", y="Rpm b1", color='y', marker="o", label='rpm')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 50, fontsize=7)
ax.set_xlabel('time')
ax.set(ylim=(0, 40))
x = file['ts']
y1 = file['Min ' + indic]
y2 = file['Max ' + indic]
ax1.fill_between(x, y1, y2, alpha =0.2, color='y', label='BRV')
ax1.set_ylabel("Breathing rate (rpm)")
ax2=ax1.twinx()
ax2.set_ylabel("Steps")
ax2.fill_between(x, file['Steps'], color='g', alpha=0.2, label='Steps')
ax2.set(ylim=(0, 500))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.rc('font', size=8)    
ax2.legend(lines1 +lines2, labels1+labels2, loc=0)
sns.set(font_scale=0.1)
plt.savefig(path_save+name + '_' + indic+'.png', orientation='landscape')


# RPM b2

sns.set_theme()
indic = 'rpm b2'
file = pd.read_csv(path_save+name+".csv")
file['ts'] = file['ts'].apply(lambda x:str(x)[10:16])
fig, ax1 = plt.subplots()
ax = sns.lineplot(data=file, x="ts", y="Rpm b2", color='y', marker="o", label='rpm')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 50, fontsize=7)
ax.set_xlabel('time')
ax.set(ylim=(0, 100))
x = file['ts']
y1 = file['Min ' + indic]
y2 = file['Max ' + indic]
ax1.fill_between(x, y1, y2, alpha =0.2, color='y', label='BRV')
ax1.set_ylabel("Breathing rate (rpm)")
ax2=ax1.twinx()
ax2.set_ylabel("Steps")
ax2.fill_between(x, file['Steps'], color='g', alpha=0.2, label='Steps')
ax2.set(ylim=(0, 500))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.rc('font', size=8)    
ax2.legend(lines1 +lines2, labels1+labels2, loc=0)
sns.set(font_scale=0.1)
plt.savefig(path_save+name + '_' + indic+'.png', orientation='landscape')



# TEMP

sns.set_theme()
indic = 'temp'
file = pd.read_csv(path_save+name+".csv")
file['ts'] = file['ts'].apply(lambda x:str(x)[10:16])
file['temp'] = (file['Mean temp1'] + file['Mean temp2'])/2
file['Temperature variation'] = file['temp'].diff()
fig, ax1 = plt.subplots()
ax = sns.lineplot(data=file, x="ts", y='Temperature variation', color='orange', marker="o", label='Temperature variation')
ax.set_xticklabels(ax.get_xticklabels(), rotation = 50, fontsize=7)
ax.set_xlabel('time')
ax.set(ylim=(-5, 5))
ax2=ax1.twinx()
ax2.set_ylabel("Steps")
ax2.fill_between(x, file['Steps'], color='g', alpha=0.2, label='Steps')
ax2.set(ylim=(0, 500))
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.rc('font', size=8)    
ax2.legend(lines1 +lines2, labels1+labels2, loc=0)
sns.set(font_scale=0.1)
plt.savefig(path_save+name + '_' + indic+'.png', orientation='landscape')










