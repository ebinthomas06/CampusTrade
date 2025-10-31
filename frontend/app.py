# In app.py
import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="CampusTrade", layout="wide")

def get_auth_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

@st.cache_data(ttl=300)
def fetch_items(search_query=""):
    try:
        url = f"{API_URL}/items/?search={search_query}"
        response = requests.get(url, headers=get_auth_headers()) # Pass headers for safety
        if response.status_code == 200:
            data = response.json()
            return data.get('results', data)
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching items: {e}")
        return []

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("Welcome to CampusTrade!")
    
# --- Sidebar ---
with st.sidebar:
    st.image("logo.png", width=100) 
    
    if 'user' in st.session_state:
        st.subheader(f"Welcome, {st.session_state['user']['username']}!")
        
        # --- NO MORE MANUAL PAGE LINKS HERE ---
        # The pages are already listed at the top.
        
        if st.button("Logout", use_container_width=True):
            logout()
    else:
        st.subheader("Welcome, Guest!")
        # The Login/Register pages are already in the top list.
    
    st.divider()
    search_query = st.text_input("Search items...")
    
# --- Main Content Area ---
st.header("Items For Sale")

# --- FIX: Get the current user's username ---
my_username = st.session_state.get('user', {}).get('username')

items = fetch_items(search_query)

if not items:
    st.info("No items found.")
else:
    col_count = 3
    cols = st.columns(col_count)
    for i, item in enumerate(items):
        with cols[i % col_count]:
            with st.container(border=True):
                st.subheader(item['title'])
                st.caption(f"Sold by {item['seller']}")
                st.write(item['description'])
                st.subheader(f"₹{item['price']}")
                if item['trade_for']:
                    st.text(f"Trade for: {item['trade_for']}")
                
                # --- FIX: Add logic to change the button ---
                if item['seller'] == my_username:
                    # If user is the seller, link to "My Items" page
                    st.page_link(
                        "pages/4_My_Items.py",
                        label="View My Item",
                        icon="📦",
                        use_container_width=True
                    )
                else:
                    # If user is NOT the seller, link to chat
                    button_key = f"contact_{item['id']}"
                    if st.button("Contact Seller / View", icon="✉️", key=button_key, use_container_width=True):
                        st.session_state['current_chat_item_id'] = item['id']
                        st.session_state['current_chat_other_user'] = item['seller']
                        st.switch_page("pages/Chat_Thread.py")
                # --- END FIX ---