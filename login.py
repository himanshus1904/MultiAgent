__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"


import streamlit as st
import google.generativeai as genai
from register import load_user_data


# Function to render the login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    user_data = load_user_data()

    if st.button("Login"):
        if username in user_data and user_data[username]['password'] == password:
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.agent_name = user_data[username]['agent_name']
            st.session_state.org_name = user_data[username]['org_name']
            st.session_state.llm = genai.GenerativeModel('gemini-1.5-pro-001')
            st.session_state.page = "Chat"
        else:
            st.error("Invalid username or password")

    st.write("New to the platform?")
    if st.button("Register"):
        st.session_state.page = "Register"


if __name__ == '__main__':
    login()

