__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pages.register import load_user_data
from PIL import Image
load_dotenv()


def login():
    # Set page configuration
    st.set_page_config(layout="wide", page_title="GREYMAN AI - Login")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .top-band {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 10px;
            background-color: #6800b5;
            z-index: 999;
        }
        .centered-title {
            text-align: center;
            padding-top: 60px;
            padding-bottom: 30px;
            font-size: 3em;
        }
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .custom-button {
            width: 80%;
            height: 50px;
            margin: 10px auto;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: bold;
            color: white;
            display: block;
        }
        .login-button {
            background-color: #4CAF50;
        }
        .register-button {
            background-color: #008CBA;
        }
        .stTextInput > div > div > input {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)


    # Create three columns
    left_col, center_col, right_col = st.columns([1, 2, 1])

    # Left column: Logo
    with left_col:
        logo = Image.open("logo.jpg")
        st.image(logo, width=200)

    # Center column: Title and login form
    with center_col:
        # Centered title
        st.markdown('<h1 class="centered-title">GREYMAN AI</h1>', unsafe_allow_html=True)

        # Create a form container
        with st.container():

            with st.form("login_form"):
                st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Login</h2>', unsafe_allow_html=True)

                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                submit = st.form_submit_button('Login', use_container_width=True)

            user_data = load_user_data()
            if submit:
                if username in user_data and user_data[username]['password'] == password:
                    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
                    st.success("Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.agent_name = user_data[username]['agent_name']
                    st.session_state.org_name = user_data[username]['org_name']
                    st.session_state.llm = genai.GenerativeModel('gemini-1.5-flash')
                    st.session_state.page = "Chat"
                    st.switch_page("pages/chat.py")
                else:
                    st.error("Invalid username or password")

            st.markdown('<p style="text-align: center; margin-top: 20px;">New to the platform?</p>',
                        unsafe_allow_html=True)
            if st.button("Register", key="register_button", use_container_width=True):
                st.switch_page("pages/register.py")

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    login()
    # genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    # llm = genai.GenerativeModel('gemini-1.5-flash')
    # print(llm.generate_content("Hi what is the capital of France?"))