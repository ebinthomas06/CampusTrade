import streamlit as st
import requests
import sidebar
from datetime import datetime
import time

st.set_page_config(
    page_title="Chat - CampusTrade",
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
    st.error("You must be logged in to chat.")
    st.page_link("pages/1_Login.py", label="Login", icon="➡️")
    st.stop()

def get_auth_headers():
    token = st.session_state.get('access_token')
    return {"Authorization": f"Bearer {token}"} if token else {}

my_username = st.session_state['user']['username']

item_id = st.session_state.get('current_chat_item_id')
other_user_username = st.session_state.get('current_chat_other_user')

if not item_id or not other_user_username:
    st.error("Invalid chat session. Please go back to your conversations.")
    st.page_link("pages/5_Conversation.py", label="Go to Conversations", icon="💬")
    st.stop()

@st.cache_data(ttl=5)
def fetch_chat_thread(item_id, other_user):
    try:
        url = f"{API_URL}/chat/{item_id}/{other_user}/"
        res = requests.get(url, headers=get_auth_headers())
        return res.json() if res.status_code == 200 else []
    except Exception as e:
        st.error(f"Error fetching chat: {e}")
        return []

def send_message(item_id, body):
    try:
        res = requests.post(
            f"{API_URL}/messages/create/",
            headers=get_auth_headers(),
            data={"item_id": item_id, "body": body}
        )
        if res.status_code == 201:
            st.cache_data.clear()
            st.rerun() 
        else:
            st.error(f"Failed to send: {res.text}")
    except Exception as e:
        st.error(f"Error: {e}")

#heading
st.title(f"Chat with {other_user_username}")
st.page_link("pages/5_Conversation.py", label="Back to Conversations", icon="⬅️")

#messages
messages = fetch_chat_thread(item_id, other_user_username)

chat_container = st.container(height=550, border=False)

with chat_container:
    if not messages:
        st.markdown("<p style='text-align:center; color:#999;'>Start the conversation!</p>", unsafe_allow_html=True)
    else:
        for msg in messages:
            is_me = msg['sender'] == my_username
            align_class = "chat-bubble-right" if is_me else "chat-bubble-left"
            
            try:
                dt_object = datetime.fromisoformat(msg['created_at'].replace('Z', '+00:00'))
                formatted_time = dt_object.strftime("%b %d, %H:%M")
            except ValueError:
                formatted_time = msg['created_at']
            
            st.markdown(f"""
                <div class="chat-bubble {align_class}">
                    <div class="chat-sender">{msg['sender']}</div>
                    <div class="chat-body">{msg['body']}</div>
                    <div class="chat-time">{formatted_time}</div>
                </div>
                """, unsafe_allow_html=True)

#chat input box
with st.form("send_message_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1]) # 5 parts for input, 1 for button
    with col1:
        prompt = st.text_input("Send a reply...", label_visibility="collapsed", placeholder="Type your message...")
    with col2:
        submitted = st.form_submit_button("Send", use_container_width=True)

if submitted and prompt and prompt.strip():
    send_message(item_id, prompt.strip())


scroll_selector = '[data-testid="stVerticalBlock"] [data-testid="stVerticalBlockBorderWrapper"]'
js = f"""
<script>
    function scroll() {{
        var container = window.parent.document.querySelector('{scroll_selector}');
        if (container) {{
            container.scrollTop = container.scrollHeight;
        }}
    }}
    setTimeout(scroll, 100);
</script>
"""
st.markdown(js, unsafe_allow_html=True)