import streamlit as st

def hide_menu():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    

def set_footer_style():
    footer="""<style>
    a:link , a:visited{
    color: blue;
    background-color: transparent;
    text-decoration: underline;
    }

    a:hover,  a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
    }

    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    }
    </style>
    """
    
    return footer

    