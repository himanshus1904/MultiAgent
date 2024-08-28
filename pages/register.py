import streamlit as st
from agents import SQLAgent, WebsiteAgent, PDFAgent
from utils import combine_results, process_text, load_user_data, save_user_data
import os
import google.generativeai as genai
from PIL import Image


def register():
    # Set page configuration
    st.set_page_config(layout="wide", page_title="GREYMAN AI - Register")

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
            max-width: 600px;
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
        .register-button {
            background-color: #4CAF50;
        }
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    # Add the top band

    # Create three columns
    left_col, center_col, right_col = st.columns([1, 2, 1])

    # Left column: Logo
    with left_col:
        logo = Image.open("logo.jpg")
        st.image(logo, width=250)

    # Center column: Title and registration form
    with center_col:
        # Centered title
        st.markdown('<h1 class="centered-title">GREYMAN AI</h1>', unsafe_allow_html=True)

        # Create a form container
        with st.container():

            # Initialize session state for registration step
            if 'registration_step' not in st.session_state:
                st.session_state.registration_step = 1

            if st.session_state.registration_step == 1:
                with st.form("user_credentials_form"):
                    st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Register</h2>',
                                unsafe_allow_html=True)

                    new_username = st.text_input("Set your Username", key="register_username")
                    new_password = st.text_input("Set your Password", type="password", key="register_password")
                    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

                    submit_credentials = st.form_submit_button('Next', use_container_width=True)

                if submit_credentials:
                    user_data = load_user_data()
                    if new_username in user_data:
                        st.error("Username already exists")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        st.session_state.new_username = new_username
                        st.session_state.new_password = new_password
                        st.session_state.registration_step = 2
                        st.rerun()

            elif st.session_state.registration_step == 2:
                with st.form("agent_details_form"):
                    st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Build your Agent</h2>',
                                unsafe_allow_html=True)

                    agent_name = st.text_input("Agent Name")
                    org_name = st.text_input("Organization Name")
                    description = st.text_area("Organization Description")
                    sql_path = st.text_input("SQL Path")
                    table_name = st.text_input("Table Name")
                    website = st.text_input("Website (if any)")
                    documents = st.file_uploader("Upload Documents (PDFs)", type="pdf", accept_multiple_files=True)
                    sec_key = os.getenv("HUGGINGFACE_KEY")

                    submit_agent = st.form_submit_button('Register', use_container_width=True)

                if submit_agent:
                    user_data = load_user_data()
                    user_data[st.session_state.new_username] = {
                        'password': st.session_state.new_password,
                        'agent_name': agent_name,
                        'org_name': org_name
                    }
                    save_user_data(user_data)


                    # Set session state variables
                    st.session_state.page = "Login"
                    st.session_state.username = st.session_state.new_username
                    st.session_state.agent_name = agent_name
                    st.session_state.org_name = org_name
                    st.session_state.description = description
                    st.session_state.sql_path = sql_path
                    st.session_state.table_name = table_name
                    st.session_state.website = website
                    st.session_state.documents = documents
                    st.session_state.sec_key = sec_key
                    st.session_state.page = 'chat'

                    # Process agent data
                    sql_agent = SQLAgent()
                    website_agent = WebsiteAgent()
                    pdf_agent = PDFAgent()

                    sql_data = sql_agent.run(sql_path, table_name) if sql_path else []
                    website_data = website_agent.run(website) if website else ""
                    pdf_data = pdf_agent.run(documents) if documents else []

                    # Combine results and query LLM
                    combined_data = combine_results(sql_data, website_data, pdf_data)
                    process_text(st.session_state.new_username, combined_data)

                    st.session_state.llm = genai.GenerativeModel('gemini-1.5-pro-001')
                    st.success("Registration successful! Please login.")
                    st.switch_page("pages/login.py")

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    register()