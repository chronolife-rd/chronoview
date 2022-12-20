import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from back_functions import get_data
from pylife.useful import unwrap
from back_functions import test_time, test_end_user, convert_data_to_excel, generate_qrcode
import pandas as pd

def show_raw_data(username, end_user, date, start_time, end_time, timezone_option):
    
    test_time(start_time, end_time)
    test_end_user(end_user)
    
    if timezone_option == 'France (Winter Time)':
        time_zone       = 'CET'
    elif timezone_option == 'France (Summer Time)':
        time_zone       = 'CEST'    
    elif timezone_option == 'GMT':
        time_zone       = 'GMT'
        
    start_time      += ':00'
    end_time        += ':00'
    from_datetime   = str(date) + " " + start_time
    to_datetime     = str(date) + " " + end_time
    
    al = get_data(username, end_user, time_zone, from_datetime, to_datetime)
    # fig = go.Figure()
    if al.is_empty_:
        st.warning("No data found")
        st.stop()
    raw_expender = st.expander("Raw Data", expanded=False)
    
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, 
                        subplot_titles=('ECG',  'Abdominal Breath', 'Thoracic Breath',
                                        'Temperatures', 'Accelerations')
                        )
    fig.add_trace(go.Scatter(x=unwrap(al.ecg.times_), y=unwrap(al.ecg.sig_),
                        mode='lines',
                        name='Electrocardiogram'),
                          row=1, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.breath_2.times_), y=unwrap(al.breath_2.sig_),
                             mode='lines',
                             line=dict(color="green", width=2),
                             name='Abdominal respiration'),
                  row=2, col=1, 
                  )
    fig.add_trace(go.Scatter(x=unwrap(al.breath_1.times_), y=unwrap(al.breath_1.sig_),
                        mode='lines',
                        name='Thoracic respiration'),
                           row=3, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.temp_1.times_), y=unwrap(al.temp_1.sig_),
                             mode='lines',
                             name='Right Temperature'),
                  row=4, col=1,
                  )
    fig.add_trace(go.Scatter(x=unwrap(al.temp_2.times_), y=unwrap(al.temp_2.sig_),
                        mode='lines',
                        name='Left Temperature'),
                        row=4, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accx.times_), y=unwrap(al.accx.sig_),
                        mode='lines',
                        name='Accx'),
                        row=5, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accy.times_), y=unwrap(al.accy.sig_),
                        mode='lines',
                        name='Accy'),
                        row=5, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accz.times_), y=unwrap(al.accz.sig_),
                        mode='lines',
                        name='Accz'),
                        row=5, col=1)
    fig.update_layout(width=500, height=750)
    raw_expender.plotly_chart(fig, True)
    
    option = raw_expender.selectbox(
    'Select raw data to download',
    ('ECG', 'Respiration', 'Temperature', 'Acceleration'))
    
    if option == 'Temperature':
        temp_1 = unwrap(al.temp_1.sig_)
        temp_2 = unwrap(al.temp_2.sig_)
        temp_times = unwrap(al.temp_1.times_)
        columns = ['Timesstamps', 'Right Temperature', 'Left Temperature']
        data = pd.DataFrame(np.array([temp_times, temp_1, temp_2]).T, columns=columns)
    elif option == 'ECG':
        ecg = unwrap(al.ecg.sig_)
        ecg_times = unwrap(al.ecg.times_)
        columns = ['Timesstamps', 'ECG']
        data = pd.DataFrame(np.array([ecg_times, ecg]).T, columns=columns)
    elif option == 'Respiration':
        breath_1 = unwrap(al.breath_1.sig_)
        breath_2 = unwrap(al.breath_2.sig_)
        breath_times = unwrap(al.breath_1.times_)
        columns = ['Timesstamps', 'Thoracic Breath', 'Abdominal Breath']
        data = pd.DataFrame(np.array([breath_times, breath_1, breath_2]).T, columns=columns)
    elif option == 'Acceleration':
        accx = unwrap(al.accx.sig_)
        accy = unwrap(al.accy.sig_)
        accz = unwrap(al.accz.sig_)
        acc_times = unwrap(al.accx.times_)
        columns = ['Timesstamps', 'Acceleration x', 'Acceleration y', 'Acceleration z']
        data = pd.DataFrame(np.array([acc_times, accx, accy, accz]).T, columns=columns)
    
    excel = convert_data_to_excel(data)
    
    raw_expender.download_button(
        label=("Download " + option + " Raw Data"),
        data=excel,
        file_name=(option.lower() + '_raw_data.xlsx'),
    )
    
    # ------------------------------------------------------------------------
    
    filt_expender = st.expander("Filtered Data", expanded=False)
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, 
                        subplot_titles=('ECG',  'Abdominal Breath', 'Thoracic Breath',
                                        'Temperatures', 'Accelerations')
                        )
    fig.add_trace(go.Scatter(x=unwrap(al.ecg.times_), y=unwrap(al.ecg.sig_filt_),
                        mode='lines',
                        name='Electrocardiogram'),
                          row=1, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.breath_2.times_), y=unwrap(al.breath_2.sig_filt_),
                             mode='lines',
                             line=dict(color="green", width=2),
                             name='Abdominal respiration'),
                  row=2, col=1, 
                  )
    fig.add_trace(go.Scatter(x=unwrap(al.breath_1.times_), y=unwrap(al.breath_1.sig_filt_),
                        mode='lines',
                        name='Thoracic respiration'),
                           row=3, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.temp_1.times_), y=unwrap(al.temp_1.sig_),
                             mode='lines',
                             name='Right Temperature'),
                  row=4, col=1,
                  )
    fig.add_trace(go.Scatter(x=unwrap(al.temp_2.times_), y=unwrap(al.temp_2.sig_),
                        mode='lines',
                        name='Left Temperature'),
                        row=4, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accx.times_), y=unwrap(al.accx.sig_),
                        mode='lines',
                        name='Accx'),
                        row=5, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accy.times_), y=unwrap(al.accy.sig_),
                        mode='lines',
                        name='Accy'),
                        row=5, col=1)
    fig.add_trace(go.Scatter(x=unwrap(al.accz.times_), y=unwrap(al.accz.sig_),
                        mode='lines',
                        name='Accz'),
                        row=5, col=1)
    fig.update_layout(width=500, height=750)
    filt_expender.plotly_chart(fig, True)
    
    
    option = filt_expender.selectbox(
    'Select filtered data to download',
    ('ECG', 'Respiration'))
    
    if option == 'ECG':
        ecg = unwrap(al.ecg.sig_filt_)
        ecg_times = unwrap(al.ecg.times_)
        columns = ['Timesstamps', 'ECG']
        data = pd.DataFrame(np.array([ecg_times, ecg]).T, columns=columns)
    elif option == 'Respiration':
        breath_1 = unwrap(al.breath_1.sig_filt_)
        breath_2 = unwrap(al.breath_2.sig_filt_)
        breath_times = unwrap(al.breath_1.times_)
        columns = ['Timesstamps', 'Thoracic Breath', 'Abdominal Breath']
        data = pd.DataFrame(np.array([breath_times, breath_1, breath_2]).T, columns=columns)
    
    excel = convert_data_to_excel(data)
    
    filt_expender.download_button(
        label=("Download " + option + " Filtered Data"),
        data=excel,
        file_name=(option.lower() + '_filtered_data.xlsx'),
    )

def show_qrcode():
    qrcode_expender = st.expander("Generate QR code", expanded=False)
    # T-shirt Reference
    device_name = qrcode_expender.text_input("T-shirt name","DiagW-03rk")
    # Show button
    qrcode_button = qrcode_expender.button("Generate QR code")
    
    if qrcode_button:
        img_file = 'qrcode.png'
        qr = generate_qrcode(device_name)
        # adding the color
        img = qr.make_image(fill = 'black', back_color = 'white')
        img.save(img_file)
        _,center,_ = qrcode_expender.columns(3)
        center.image(img_file, width=250)