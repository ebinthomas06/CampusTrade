import streamlit as st
import requests
import sidebar
import time

st.set_page_config(
    page_title="Post Item - CampusTrade", 
    layout="centered",
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
    st.error("You must be logged in to post an item.")
    st.page_link("pages/1_Login.py", label="Login", icon="➡️")
    st.stop()
def get_auth_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

if st.session_state.get("form_submitted_successfully", False):
    st.success("Item posted successfully!")
    st.session_state["post_title"] = ""
    st.session_state["post_description"] = ""
    st.session_state["post_price"] = 0.0
    st.session_state["post_trade_for"] = ""
    st.session_state["form_submitted_successfully"] = False

st.title("Post a New Item")

with st.form("post_item_form"):
    if "post_title" not in st.session_state:
        st.session_state.post_title = ""
    if "post_description" not in st.session_state:
        st.session_state.post_description = ""
    if "post_price" not in st.session_state:
        st.session_state.post_price = 0.0
    if "post_trade_for" not in st.session_state:
        st.session_state.post_trade_for = ""
        
    title = st.text_input("Title", key="post_title")
    description = st.text_area("Description", key="post_description")
    price = st.number_input("Price (INR)", min_value=0.0, format="%.2f", key="post_price")
    trade_for = st.text_input("Willing to trade for (optional)", key="post_trade_for")
    
    submitted = st.form_submit_button("Post Item")

    if submitted:
        if not title:
            st.error("Title is required.")
        else:
            try:
                response = requests.post(f"{API_URL}/items/", headers=get_auth_headers(), data={
                    "title": title,
                    "description": description,
                    "price": price,
                    "trade_for": trade_for
                })
                
                if response.status_code == 201:
                    st.session_state.form_submitted_successfully = True
                    st.rerun() 
                else:
                    st.error(f"Failed to post item: {response.json()}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

