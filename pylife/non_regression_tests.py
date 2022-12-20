# Path to pylife
path_root = 'C:/Users/Blandinelandrieu/Desktop/'
import numpy as np
import pandas as pd
import pickle
import sys
sys.path.append(path_root)
#path_data = './data/'
from pylife.simul_functions import simul_breath, simul_ecg, simul_acc, simul_temp, simul_imp, simul_noise
from pylife.siglife import ECG, Breath_1, Temperature_1, Impedance_1
from pylife.siglife import Acceleration_x, Accelerations
import matplotlib.pyplot as plt
import csv

# %% testing on generated signals

# Flag for disconnection
flag_disconnection_ = [True, False]

# Flag for clean breath
flag_clean_breath_  = [True, False]

# Flag for clean ecg
flag_clean_ecg_     = [True, False]

# Flag for clean temperature
flag_clean_temp_    = [True, False]

duration                = 1*60
disconnection_duration  = np.timedelta64(10, 's') # seconds
sig_noise_amp           = 8
time_now                = np.datetime64('now')

n_step_pm   = 100
n_step_error_margin = 5

rpm         = 12
rpm_error_margin= 1

bpm         = 60
bpm_error_margin = 5

temp_error_margin = 1

test_results= pd.DataFrame(columns=['signal', 'with_disconnection', 'clean', 
                                    'expected_value','calc_value','valid_result'])

for flag_disconnection in flag_disconnection_:
    if flag_disconnection:
        n_seg = 2
        print('with no disconection')
    else:
        n_seg = 1
        print('with disconection')
        
        
    for flag_clean_breath in flag_clean_breath_:
        # % BREATH
        #print('flag_clean_breath', flag_clean_breath)
        fs=20
        sig_s = []
        times_s = []
        last_time = time_now
        for i in range(n_seg):
            if flag_clean_breath:
                sig = simul_breath(duration, fs, rpm, noise_amp=1e-1)
                sig = sig*1000
            else:
                sig = simul_noise(duration, fs, noise_amp=sig_noise_amp)
            
            sig     = sig.astype('int')
            times   = np.arange(last_time, 
                              last_time + np.timedelta64(int(len(sig)/fs*1e6), 'us'),
                              np.timedelta64(int(1/fs*1e6), 'us'))
            last_time = times[-1]
            if flag_disconnection:
                last_time = last_time + disconnection_duration
                
            sig_s.append(sig)
            times_s.append(times)
        
        breath = Breath_1({'times': times_s, 'sig': sig_s, 'fs': fs})
        breath.filt()
        breath.clean()
        breath.analyze()
        #print('calculated RPM ', breath.rpm_, ' true rpm ', rpm)
        # plt.figure()
        # breath.show(on_sig='filt')
        if flag_clean_breath :
            correct_pred= (rpm - rpm_error_margin <= round(breath.rpm_[0],1) <= rpm +rpm_error_margin)
            test_results.loc[len(test_results.index)] = ['breath_rpm',flag_disconnection,
                                                         flag_clean_breath,
                                 [rpm], breath.rpm_,  correct_pred ]
        else:
            correct_pred= (breath.rpm_==[])
            test_results.loc[len(test_results.index)] = ['breath_rpm',flag_disconnection,
                                                         flag_clean_breath,
                                 [], breath.rpm_,  correct_pred ]
    #print('test_results with breath', test_results)
    for flag_clean_ecg in flag_clean_ecg_:
        # % ECG
        noise = 1/50
        fs = 200
        prev = 1/100
        sig_s = []
        times_s = []
        last_time = time_now
        for i in range(n_seg):
            if flag_clean_ecg:
                sig = simul_ecg(duration, fs, bpm, afib=False, noise_amp=1e-2)
                sig = sig*1000
            else:
                sig = simul_noise(duration, fs, noise_amp=sig_noise_amp)
            sig = sig.astype('int')
            times = np.arange(last_time, 
                              last_time + np.timedelta64(int(len(sig)/fs*1e6), 'us'),
                              np.timedelta64(int(1/fs*1e6), 'us'))
            last_time = times[-1]
            if flag_disconnection:
                last_time = last_time + disconnection_duration
                
            sig_s.append(sig)
            times_s.append(times)
        ecg = ECG({'times': times_s, 'sig': sig_s, 'fs': fs})
        ecg.filt()
        ecg.clean()
        ecg.analyze()
        #print('BPM', ecg.bpm_)
        # plt.figure()
        # ecg.show()

        if flag_clean_ecg :
            correct_pred= (bpm - bpm_error_margin <= round(ecg.bpm_[0],1)
                           <= bpm + bpm_error_margin)
            test_results.loc[len(test_results.index)] = ['ecg_bpm', flag_disconnection,
                                                         flag_clean_ecg,
                                 [bpm], ecg.bpm_,  correct_pred ]
        else:
            correct_pred= (ecg.bpm_==[])
            test_results.loc[len(test_results.index)] = ['ecg_bpm', flag_disconnection,
                                                         flag_clean_ecg,
                                 [], ecg.bpm_,  correct_pred ]
         
            
    for flag_clean_temp in flag_clean_temp_:
        # % TEMP
        fs = 1
        sig_s = []
        times_s = []
        last_time = time_now
        for i in range(n_seg):
            if flag_clean_temp:
                sig = simul_temp(duration, fs, mean_temp=2500, noise_amp=.1)
            else:
                sig = simul_temp(duration, fs, mean_temp=0, noise_amp=0)
            times = np.arange(last_time, 
                              last_time + np.timedelta64(int(len(sig)/fs*1e6), 'us'),
                              np.timedelta64(int(1/fs*1e6), 'us'))
            last_time = times[-1]
            if flag_disconnection:
                last_time = last_time + disconnection_duration
            sig_s.append(sig)
            times_s.append(times)
        temp = Temperature_1({'times': times_s, 'sig': sig_s, 'fs': fs})
        temp.filt()
        temp.clean()
        temp.analyze()
        #print('Temp mean', np.mean(temp.mean_))
        
        if flag_clean_temp :
            correct_pred= (25 - temp_error_margin <= temp.mean_
                           <= 25 + temp_error_margin)
            test_results.loc[len(test_results.index)] = ['Temp_Celsius', flag_disconnection,
                                                         flag_clean_temp,
                                 25, temp.mean_,  correct_pred ]
        else:
            correct_pred= (temp.mean_== 0)
            test_results.loc[len(test_results.index)] = ['Temp_Celsius', flag_disconnection,
                                                         flag_clean_temp,
                                 0, temp.mean_,  correct_pred ]
        
        
        
        # plt.figure()
        # temp.show()
        # plt.ylim(20,30)
                 
        # # % IMP
        # fs = 1/(10*60)
        # sig_s = []
        # times_s = []
        # last_time = time_now
        # for i in range(n_seg):
        #     sig = simul_imp(duration, fs)
        #     sig = sig.astype('int')
        #     times = np.arange(last_time, 
        #                       last_time + np.timedelta64(int(len(sig)/fs*1e6), 'us'),
        #                       np.timedelta64(int(1/fs*1e6), 'us'))
        #     last_time = times[-1]
        #     if flag_disconnection:
        #         last_time = last_time + disconnection_duration
        #     sig_s.append(sig)
        #     times_s.append(times)
        # imp = Impedance_1({'times': times_s, 'sig': sig_s, 'fs': fs})
        # # plt.figure()
        # # imp.show()
        
        # %
        # savefilename = ['simul']
        # if flag_disconnection:
        #     savefilename.append('_disco')
        # if not flag_clean_breath:
        #     savefilename.append('_br-nok')
        # if not flag_clean_ecg:
        #     savefilename.append('_ecg-nok')
        # if not flag_clean_temp:
        #     savefilename.append('_temp-nok')
        # savefilename = ''.join(savefilename)
        # data = {'accx': accx, 'accy': accy, 'accz': accz, 'acc': acc, 'breath': breath, 
        #         'ecg': ecg, 'temp': temp}
        # with open((path_data + savefilename + '.pkl'), 'wb') as file:
        #     pickle.dump(data, file)
        #     print(savefilename + '.pkl saved in', path_data)
        #     print('-----------------------------------------')

    # % ACC 
    # we don't clean acceleration signals
    fs=50
    
    sig_s       = []
    times_s     = []
    last_time   = time_now
    
    for i in range(n_seg):
        sig1 = simul_acc(duration/2, fs, n_step_pm, noise_amp=.5)
        sig1 = sig1*200
        sig2 = simul_acc(duration/2, fs, n_step_pm=0, noise_amp=.5)
        sig = np.hstack((sig1, sig2))
        sig = sig.astype('int')
        times = np.arange(last_time, 
                          last_time + np.timedelta64(int(len(sig)/fs*1e6), 'us'),
                          np.timedelta64(int(1/fs*1e6), 'us'))
        last_time = times[-1]
        if flag_disconnection:
            last_time = last_time + disconnection_duration
        sig_s.append(sig)
        times_s.append(times)
    accx    = Acceleration_x({'times': times_s, 'sig': np.array(sig_s), 'fs': fs})
    accy    = Acceleration_x({'times': times_s, 'sig': np.array(sig_s)-20, 'fs': fs})
    accz    = Acceleration_x({'times': times_s, 'sig': np.array(sig_s)+20, 'fs': fs})
    acc     = Accelerations(accx, accy, accz)
    acc.filt()
    acc.clean()
    acc.analyze()
    #plt.figure()
    #accx.show()
    
    #print('N steps', acc.n_steps_)   
    
    
    if flag_disconnection :
        correct_pred= (n_step_pm - n_step_error_margin <=  acc.n_steps_
                       <= n_step_pm + n_step_error_margin)
        test_results.loc[len(test_results.index)] = ['n_steps', flag_disconnection,
                                                     True,
                             n_step_pm,  acc.n_steps_,  correct_pred ]
    else:
        correct_pred= (n_step_pm/2 - n_step_error_margin/2 <=  acc.n_steps_
                       <= n_step_pm/2 + n_step_error_margin/2)
        test_results.loc[len(test_results.index)] = ['n_steps', flag_disconnection,
                                                     True,
                             n_step_pm/2,  acc.n_steps_,  correct_pred ]
        
test_results.to_excel('non_regression_tests.xlsx')

#%% show non valid test results
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(test_results.loc[test_results['valid_result']==False])

