# In pages/5_Conversation.py
import streamlit as st
import requests
from jwt import decode

API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Conversations", layout="wide")

# --- FIX: CHECK FOR PARAMS AT THE TOP ---
# Check if the user has clicked a chat *before* rendering the page
if "item_id" in st.query_params and "other_user_username" in st.query_params:
    st.switch_page("pages/Chat_Thread.py")
# --- END FIX ---

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

@st.cache_data(ttl=10) # Short cache for messages
def fetch_conversations():
    try:
        # Note: This might fetch all pages if you have pagination.
        # For simplicity, we'll fetch just the first page.
        response = requests.get(f"{API_URL}/inbox/", headers=get_auth_headers())
        if response.status_code == 200:
            # Handle paginated or non-paginated data
            data = response.json()
            all_messages = data.get('results', data) # Get 'results' if paginated
            
            # --- Grouping Logic ---
            grouped = {}
            for msg in all_messages:
                other_user = msg['sender'] if msg['sender'] != my_username else msg['receiver']
                key = (msg['item'], other_user)
                
                if key not in grouped or msg['created_at'] > grouped[key]['created_at']:
                    grouped[key] = msg
                    grouped[key]['other_user'] = other_user
            
            return sorted(grouped.values(), key=lambda x: x['created_at'], reverse=True)
        else:
            st.error("Could not fetch conversations.")
            return []
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
            
            # --- FIX: BUTTON LOGIC ---
            button_key = f"chat_{conv['item']}_{conv['other_user']}"
            if st.button("Open Chat", icon="💬", key=button_key, use_container_width=True):
                # 1. Store the chat info in session_state
                st.session_state['current_chat_item_id'] = conv['item']
                st.session_state['current_chat_other_user'] = conv['other_user']
                
                # 2. Switch the page
                st.switch_page("pages/Chat_Thread.py")