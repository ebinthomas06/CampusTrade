# In pages/1_Login.py
import streamlit as st
import requests
from jwt import decode

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Login", layout="centered")
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
            
            # Use jwt.decode (PyJWT)
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

# --- UI ---
if 'user' in st.session_state:
    st.success(f"You are already logged in as {st.session_state['user']['username']}!")
    st.page_link("app.py", label="Go to Home", icon="🏠") # Link to app.py
else:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if login_user(username, password):
                # On successful login, navigate to home
                st.switch_page("app.py")