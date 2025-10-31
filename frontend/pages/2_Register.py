# In pages/2_Register.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Register", layout="centered")
st.title("Register for CampusTrade")

with st.form("register_form"):
    username = st.text_input("Username")
    # Remember to use your college's domain
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
                    st.error(f"Registration failed: {response.json()}")
            except Exception as e:
                st.error(f"An error occurred: {e}")