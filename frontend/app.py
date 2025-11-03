import streamlit as st
import requests
import time
import sidebar 

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="CampusTrade - Home", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("style.css not found! Please create the file.")

load_css("style.css")
sidebar.build_sidebar() 

def get_auth_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

@st.cache_data(ttl=300)
def fetch_items(search_query=""):
    try:
        url = f"{API_URL}/items/?search={search_query}"
        response = requests.get(url, headers=get_auth_headers()) 
        if response.status_code == 200:
            data = response.json()
            return data.get('results', data)
        else:
            return []
    except Exception as e:
        print(f"Error fetching items: {e}")
        return []

st.markdown("<h1 style='text-align: center;'>Welcome to CampusTrade!</h1>", unsafe_allow_html=True)
st.header("Items For Sale", divider="gray")

search_query = st.query_params.get("search", "")

my_username = st.session_state.get('user', {}).get('username')
items = fetch_items(search_query) 

if not items:
    if search_query:
        st.info(f"No items found for '{search_query}'.")
    else:
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
                st.markdown(f"### ₹{item['price']}") 
                
                if item['trade_for']:
                    st.text(f"Trade for: {item['trade_for']}")
                
                if item['seller'] == my_username:
                    st.page_link(
                        "pages/4_My_Items.py",
                        label="View My Item",
                        icon="📦",
                        use_container_width=True
                    )
                else:
                    button_key = f"contact_{item['id']}"
                    if st.button("Contact Seller / View", icon="✉️", key=button_key, use_container_width=True):
                        st.session_state['current_chat_item_id'] = item['id']
                        st.session_state['current_chat_other_user'] = item['seller']
                        st.switch_page("pages/_Chat_Thread.py")