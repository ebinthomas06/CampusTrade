import streamlit as st
import requests
import sidebar 

st.set_page_config(
    page_title="Register - CampusTrade", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Could not find CSS file: {file_name}")

load_css("style.css")
sidebar.build_sidebar()

API_URL = "http://127.0.0.1:8000/api"

st.title("Register for CampusTrade")

with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("College Email (e.g., user@iiitkottayam.ac.in)")
    password = st.text_input("Password", type="password")
    password2 = st.text_input("Confirm Password", type="password")
    
    submitted = st.form_submit_button("Register")

    if submitted:
        if password != password2:
            st.error("Passwords do not match!")
        else:
            try:
                response = requests.post(f"{API_URL}/register/", data={
                    "username": username,
                    "email": email,
                    "password": password
                })
                
                if response.status_code == 201:
                    st.success("Registration successful! Please log in.")
                    st.page_link("pages/1_Login.py", label="Go to Login", icon="➡️")
                else:
                    try:
                        error_data = response.json()
                        if 'email' in error_data:
                            st.error(f"Registration failed: {error_data['email'][0]}")
                        elif 'username' in error_data:
                            st.error(f"Registration failed: {error_data['username'][0]}")
                        else:
                            st.error(f"Registration failed: {error_data}")
                    except requests.exceptions.JSONDecodeError:
                        st.error("Registration failed. An unknown error occurred.")
            except Exception as e:
                st.error(f"An error occurred: {e}")