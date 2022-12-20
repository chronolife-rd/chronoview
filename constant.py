import streamlit as st
import os
from PIL import Image

URL_ROOT = "https://prod.chronolife.net/api/2"
CURRENT_DIRECTORY = os.getcwd()

LOGO_CLIFE = Image.open(CURRENT_DIRECTORY + '/assets/logoclife.png')

def init_session_state():
    if 'username' not in st.session_state:
        st.session_state.username = ''
        
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''

    if 'end_user' not in st.session_state:
            st.session_state.saveEndUser = ''

    if 'auth_status' not in st.session_state:
            st.session_state.auth_status = False

    if 'count' not in st.session_state:
            st.session_state.count = 0