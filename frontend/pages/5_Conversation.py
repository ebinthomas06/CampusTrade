import streamlit as st
import requests
from jwt import decode
import os
import sidebar  

st.set_page_config(
    page_title="Conversations - CampusTrade",
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

my_username = st.session_state.get('user', {}).get('username')

@st.cache_data(ttl=10) 
def fetch_conversations():
    all_messages_list = []
    url = f"{API_URL}/inbox/"
    
    try:
        while url:
            response = requests.get(url, headers=get_auth_headers())
            if response.status_code != 200:
                st.error("Could not fetch conversations.")
                return []
                
            data = response.json()
            all_messages_list.extend(data.get('results', [])) 
            url = data.get('next') 
            
        grouped = {}
        for msg in all_messages_list:
            other_user = msg['sender'] if msg['sender'] != my_username else msg['receiver']
            key = (msg['item'], other_user)
            
            if key not in grouped or msg['created_at'] > grouped[key]['created_at']:
                grouped[key] = msg
                grouped[key]['other_user'] = other_user
        
        return sorted(grouped.values(), key=lambda x: x['created_at'], reverse=True)
        
    except Exception as e:
        st.error(f"Error fetching conversations: {e}")
        return []

st.title("Your Conversations")

conversations = fetch_conversations()

if not conversations:
    st.info("You have no conversations.")
else:
    for conv in conversations:
        with st.container(border=True):
            st.subheader(f"Chat with {conv['other_user']} about: {conv['item_title']}")
            st.write(f"**Last Message:** {conv['body']}")
            st.caption(f"On {conv['created_at']}")
            
            button_key = f"chat_{conv['item']}_{conv['other_user']}"
            if st.button("Open Chat", icon="💬", key=button_key, use_container_width=True):
                st.session_state['current_chat_item_id'] = conv['item']
                st.session_state['current_chat_other_user'] = conv['other_user']
                
                st.switch_page("pages/_Chat_Thread.py")