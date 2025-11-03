import streamlit as st
import requests
from jwt import decode
import os
import sidebar  

st.set_page_config(
    page_title="My Items - CampusTrade", 
    layout="wide", 
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

if 'user' not in st.session_state:
    st.error("You must be logged in to view this page.")
    st.page_link("pages/1_Login.py", label="Login", icon="➡️")
    st.stop()

def get_auth_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

@st.cache_data(ttl=60) 
def fetch_my_items():
    try:
        response = requests.get(f"{API_URL}/my-items/", headers=get_auth_headers())
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching items: {e}")
        return []

def delete_item(item_id):
    try:
        response = requests.delete(f"{API_URL}/items/{item_id}/", headers=get_auth_headers())
        if response.status_code == 204:
            st.success("Item deleted!")
            st.cache_data.clear() 
            st.rerun()
        else:
            st.error(f"Failed to delete item: {response.json()}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("My Listed Items")

my_items = fetch_my_items()

if not my_items:
    st.info("You have not posted any items yet.")
else:
    for item in my_items:
        col1, col2 = st.columns([4, 1]) 
        
        with col1:
            with st.container(border=True):
                st.subheader(item['title'])
                st.write(item['description'])
                st.markdown(f"### ₹{item['price']}")
                if item['trade_for']:
                    st.text(f"Trade for: {item['trade_for']}")
        
        with col2:
            if st.button("Delete", key=f"delete_{item['id']}", type="primary", use_container_width=True):
                delete_item(item['id'])