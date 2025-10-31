# In pages/3_Post_Item.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Post Item", layout="centered")

# --- Authentication Check ---
if 'user' not in st.session_state:
    st.error("You must be logged in to post an item.")
    st.page_link("pages/1_Login.py", label="Login", icon="➡️")
    st.stop() # Stop script execution

def get_auth_headers():
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

st.title("Post a New Item")

with st.form("post_item_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    price = st.number_input("Price (INR)", min_value=0.0, format="%.2f")
    trade_for = st.text_input("Willing to trade for (optional)")
    
    submitted = st.form_submit_button("Post Item")

    if submitted:
        try:
            response = requests.post(f"{API_URL}/items/", headers=get_auth_headers(), data={
                "title": title,
                "description": description,
                "price": price,
                "trade_for": trade_for
            })
            
            if response.status_code == 201:
                st.success("Item posted successfully!")
                st.page_link("app.py", label="Go to Home", icon="🏠")
            else:
                st.error(f"Failed to post item: {response.json()}")
        except Exception as e:
            st.error(f"An error occurred: {e}")