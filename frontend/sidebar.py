import streamlit as st
from jwt import decode
from streamlit_option_menu import option_menu

def get_user_info():
    try:
        token = st.session_state.get('access_token')
        if token:
            user = decode(token, options={"verify_signature": False})
            return user
    except Exception as e:
        print(f"Error decoding token in sidebar: {e}")
        if 'access_token' in st.session_state:
            del st.session_state['access_token']
        return None

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state['page'] = 'app.py' 
    st.switch_page("app.py")

def build_sidebar():
    user = get_user_info()
    
    with st.sidebar:
        st.image("logo.png", width=100)
        
        if user:
            st.subheader(f"Welcome, {user.get('username', 'User')}!")
        else:
            st.subheader("Welcome, Guest!")
            
        st.divider()

        search_query = st.text_input("Search items...")
        
        if search_query:
            st.query_params["search"] = search_query
        else:
            st.query_params.pop("search", None)

        if 'page' not in st.session_state:
            st.session_state.page = "app.py"

        icons_logged_out = {
            "Home": "house-door",
            "Login": "box-arrow-in-right",
            "Register": "person-plus"
        }
        
        icons_logged_in = {
            "Home": "house-door",
            "Post New Item": "plus-square",
            "My Items": "box-seam",
            "Conversations": "chat-dots",
        }
        
        def handle_page_switch(page_key):
            st.session_state.page = page_key
            st.switch_page(page_key)

        if user:
            pages = {
                "Home": "app.py",
                "Post New Item": "pages/3_Post_Item.py",
                "My Items": "pages/4_My_Items.py",
                "Conversations": "pages/5_Conversation.py"
            }
            
            current_page_file = st.session_state.get('page', 'app.py')
            current_page_index = 0
            try:
                current_page_index = list(pages.values()).index(current_page_file)
            except ValueError:
                pass 

            selected = option_menu(
                menu_title="Menu",
                options=list(pages.keys()),
                icons=list(icons_logged_in.values()),
                menu_icon="list", 
                default_index=current_page_index,
                key="nav_menu_logged_in"
            )
            
            if pages[selected] != st.session_state.page:
                handle_page_switch(pages[selected])

            st.button("Logout", on_click=logout, use_container_width=True, type="primary")
        
        else:
            pages = {
                "Home": "app.py",
                "Login": "pages/1_Login.py",
                "Register": "pages/2_Register.py"
            }
            
            current_page_file = st.session_state.get('page', 'app.py')
            current_page_index = 0
            try:
                current_page_index = list(pages.values()).index(current_page_file)
            except ValueError:
                pass
                
            selected = option_menu(
                menu_title="Menu",
                options=list(pages.keys()),
                icons=list(icons_logged_out.values()),
                menu_icon="list",
                default_index=current_page_index,
                key="nav_menu_logged_out"
            )
            
            if pages[selected] != st.session_state.page:
                handle_page_switch(pages[selected])
        