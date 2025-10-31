# In pages/Chat_Thread.py
import streamlit as st
import requests
from jwt import decode

API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Chat", layout="centered")

# --- Authentication Check ---
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

# --- Get URL Parameters from SESSION_STATE ---
try:
    # Read from session_state instead of query_params
    item_id = st.session_state["current_chat_item_id"]
    other_user = st.session_state["current_chat_other_user"]
except KeyError:
    st.error("Invalid chat session. Please go back to your conversations.")
    st.page_link("pages/5_Conversation.py", label="Go to Conversations", icon="⬅️")
    st.stop()
# --- END FIX ---

@st.cache_data(ttl=5) # Very short cache for chat
def fetch_chat_thread(item_id, other_user):
    # ... (this function is correct) ...
    try:
        url = f"{API_URL}/chat/{item_id}/{other_user}/"
        response = requests.get(url, headers=get_auth_headers())
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching chat: {e}")
        return []

def send_message(item_id, body):
    # ... (this function is correct) ...
    try:
        response = requests.post(f"{API_URL}/messages/create/", headers=get_auth_headers(), data={
            "item_id": item_id,
            "body": body
        })
        if response.status_code == 201:
            st.cache_data.clear() # Clear cache to show new message
            return True
        else:
            st.error(f"Failed to send: {response.json()}")
            return False
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return False

# --- UI ---
st.title(f"Chat with {other_user}")
st.page_link("pages/5_Conversation.py", label="Back to Conversations", icon="⬅️")

messages = fetch_chat_thread(item_id, other_user)

# --- Chat Message Display ---
st.header(f"Chat with {other_user}", divider="gray") # Added a header for clarity

for msg in messages:
    # Check if the message sender is the current logged-in user
    if msg['sender'] == my_username:
        # If yes, use "user" to align to the right
        with st.chat_message(name="user"):
            st.write(msg['body'])
            # Format the date for a cleaner look
            st.caption(f"Sent: {msg['created_at']}") 
    else:
        # If no, use the sender's name to align to the left
        with st.chat_message(name=msg['sender']):
            st.write(msg['body'])
            st.caption(f"Received: {msg['created_at']}")

# --- Chat Input Box ---
prompt = st.chat_input("Send a reply...")
if prompt:
    if send_message(item_id, prompt):
        st.rerun()