import streamlit as st
import requests
from jwt import decode
import os
import sidebar 

st.set_page_config(
    page_title="Login - CampusTrade", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("style.css not found!")

load_css("style.css")
sidebar.build_sidebar()

API_URL = "http://127.0.0.1:8000/api"

st.title("Login to CampusTrade")

def login_user(username, password):
    try:
        response = requests.post(f"{API_URL}/token/", data={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            tokens = response.json()
            st.session_state['access_token'] = tokens['access']
            st.session_state['refresh_token'] = tokens['refresh']
            
            user_data = decode(tokens['access'], options={"verify_signature": False})
            st.session_state['user'] = user_data
            
            st.rerun() 
            return True
        else:
            st.error(response.json().get('detail', 'Invalid credentials.'))
            return False
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend. Is the Django server running?")
        return False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

if 'user' in st.session_state:
    st.success(f"You are already logged in as {st.session_state['user']['username']}!")
    st.page_link("app.py", label="Go to Home", icon="🏠")
else:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login_user(username, password):
                st.switch_page("app.py")