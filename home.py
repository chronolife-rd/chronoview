import streamlit as st 
from PIL import Image
# import calendar
from show import show_raw_data, show_qrcode
from datetime import datetime as dt
from constant import (init_session_state, 
                      URL_ROOT,
                      LOGO_CLIFE,
                      )
from back_functions import (api_auth, 
                  save_credentials,
                  remove_credentials,
                  )
from template.style import hide_menu, set_footer_style
from version import VERSION

st.set_page_config("Chronoview ",page_icon= "⌚",layout="wide",)
hide_menu()
init_session_state()

clife_image = Image.open('assets/Clife.png')

# %%
with st.sidebar:
    col_logo,_=st.columns(2)
    col_logo.image(LOGO_CLIFE)
    username    = st.text_input("Username", st.session_state['username'], placeholder="Ex: Chronnolife")
    api_key     = st.text_input("API key", st.session_state['api_key'], placeholder="Ex: f9VBqQoTiU0mnAKoXK1lky", type="password")
 
    if api_key:
        st.session_state.api_key = api_key

    col1, col2 = st.columns(2)
    button_sign_in = col1.button('Sign in')
    button_sign_out = col2.button('Sign out')
    
    if button_sign_in and not st.session_state.auth_status:
        
        # % GET: Retrieve relevant properties of the specified user.
        url = URL_ROOT + "/user/{userId}".format(userId=username)
        message, status_code = api_auth(api_key, url, username)
        
        if status_code == 200:
            st.session_state.auth_status = True
        else:
            st.session_state.auth_status = False
            
        if st.session_state.auth_status:
            st.success(message)
            path_creds = save_credentials(username, api_key)
            
            if st.session_state.count == 0:
                st.balloons()
                st.session_state.count = st.session_state.count + 1
        else:
            st.error(message)
            
            
    if button_sign_out:
       st.session_state.auth_status = False 
       st.warning('Not connected')
       try:
           remove_credentials(username)
       except:
           pass
       
with st.container():
    if st.session_state.auth_status:
        
        # ----- Header -----
        cview_col1, cview_col2,_= st.columns([1,2,1])
        cview_col1.image(clife_image,width= 59)
        cview_col2.markdown("<h2 style='text-align: center; color: #397E97 '> Chronoview</h2>", unsafe_allow_html=True)
        
        # ----- Generate QR code -----
        show_qrcode()
        
        # ----- Parameters selection -----
        data_form = st.form("data_form")
        col1_data_form, col2_data_form, col3_data_form, col4_data_form, col5_data_form = data_form.columns([1,1,1,1,1])
        # Date picker
        date = col1_data_form.date_input("🗓️ Select date:", max_value=dt.now(), key="ksd")
        # Time picker
        start_time = col2_data_form.text_input("Start time HH:MM", "22:22")
        end_time = col3_data_form.text_input("End time HH:MM", "22:23")
        # User ID input
        data_user = col4_data_form.text_input("🏃🏼‍♂️ User ID","5P4svk")
        # Show button
        data_request = data_form.form_submit_button("Show")
        # code_id, datas, paramsI =  request_indicators(data_user, date)
        show_raw_data(username, data_user, date, start_time, end_time)
        data_form.success("Data has been successfully requested")
        
    else:
            st.info('Please enter a Username and an API-key to access Chronoview')
    
footer = set_footer_style()
footer +="""
<div class="footer">
<p style="color: grey;">Version
"""
footer += VERSION
footer +="""
</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)


