from pylife.datalife import Apilife
import requests
import os
from constant import URL_ROOT
import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode

def get_data(username, end_user_id, time_zone, t0, t1):

    path_creds = os.getcwd() + '/secret/' + username
    
    params = {'path_ids': path_creds, 'api_version': 2,
              'end_user': end_user_id, 
              'from_time': t0, 'to_time': t1, 'time_zone': time_zone,
              'device_model': 'tshirt',
              'flag_acc': True, 'flag_breath': True, 
              'flag_ecg': True, 'flag_temp': True, 
              'flag_imp': True,  'activity_types': '',
              'activity_types': '',
              }

    al = Apilife(params)
    print('Getting...')
    al.get()
    print('Parsing...')
    al.parse()
    print('Filtering...')
    al.filt()
    return al

def api_auth(api_key, url, userId):
    status_code = None
    message = None
    
    reply = requests.get(url, headers={"X-API-Key": api_key})
    status_code = reply.status_code
    message = api_status(reply.status_code)

    return message, status_code

def api_status(status_code, user_text='username'):
    
    if status_code == 200:
        message = 'Connected'
    elif status_code == 400:
        message = 'Part of the request could not be parsed or is incorrect'
    elif status_code == 401:
        message = 'Incorrect API key'
    elif status_code == 403:
        message = 'Not authorized'
    elif status_code == 404:
        message = 'Incorrect url'
    elif status_code == 500:
        message = 'Incorrect ' + user_text
    elif status_code == 0:
        message = "You are disconnect"
        
    return message

def save_credentials(username, api_key):
    path_creds = os.getcwd() + '/secret/' + username
    if not os.path.exists(path_creds):
        os.mkdir(path_creds)
        
    with open(path_creds + '/api_ids.txt', 'w') as f:
        f.write('user = ' + username + '\ntoken = ' + api_key + '\nurl = ' + URL_ROOT + "/data")
    
    return path_creds
        
def remove_credentials(username):
    path_creds = os.getcwd() + '/secret/' + username
    os.remove(path_creds + '/api_ids.txt')
    os.rmdir(path_creds)
    

def test_time(start_time, end_time):
    message = False
    
    if start_time == "":
        message = "Start time format is empty"
        st.error(message)
        st.stop()
    if end_time == "":
        message = "End time format is empty"
        st.error(message)
        st.stop()
    if ":" not in start_time:
        message = "Start time format is incorrect"
        st.error(message)
        st.stop()
    if ":" not in end_time:
        message = "End time format is incorrect"
        st.error(message)
        st.stop()
    
    if len(start_time) != 5:
        message = "Start time format is incorrect"
        st.error(message)
        st.stop()
    if len(end_time) != 5:
        message = "End time format is incorrect"
        st.error(message)
        st.stop()
        
    try:
        tmp = int(start_time[:2])
        del tmp
        tmp = int(start_time[3:])
        del tmp
    except:
        message = "Start time format is incorrect"
        st.error(message)
        st.stop()
        
    try:
        tmp = int(end_time[:2])
        del tmp
        tmp = int(end_time[3:])
        del tmp
    except:
        message = "End time format is incorrect"
        st.error(message)
        st.stop()
        
        
    if int(start_time[:2]) < 0 or int(start_time[:2]) > 24:
        message = "Start time hours must be between 00 and 24"
        st.error(message)
        st.stop()
    if int(end_time[:2]) < 0 or int(end_time[:2]) > 24:
        message = "End time hours must be between 00 and 24"
        st.error(message)
        st.stop()
        
    if int(start_time[3:]) < 0 or int(start_time[3:]) > 59:
        message = "Start time minutes must be between 00 and 59"
        st.error(message)
        st.stop()
    if int(end_time[3:]) < 0 or int(end_time[3:]) > 59:
        message = "End time minutes must be between 00 and 59"
        st.error(message)
        st.stop()
        
    if int(end_time[:2]) < int(start_time[:2]):
        message = "End time must be greater than Start time"
        st.error(message)
        st.stop()
    if int(end_time[:2]) == int(start_time[:2]) and int(end_time[3:]) < int(start_time[3:]):
        message = "End time must be greater than Start time"
        st.error(message)
        st.stop()
    if end_time == start_time:
        message = "End time must be greater than Start time"
        st.error(message)
        st.stop()

@st.cache
def convert_data_to_excel(data):
    # Cache the conversion to prevent computation on every rerun
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def generate_qrcode(device_name):
    # creating the variable for the QR code
    qr = qrcode.QRCode(
        version = 1,
        box_size = 15,
        border = 10
        )

    # adding a link for the QR code to open
    data = 'chronomonitoring://' + device_name
    qr.add_data(data)
    qr.make(fit=True)
    
    return qr