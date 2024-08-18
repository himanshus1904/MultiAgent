__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"

import streamlit as st
from agents import SQLAgent, WebsiteAgent, PDFAgent
from utils import combine_results, process_text, load_user_data, save_user_data
import os
import google.generativeai as genai


def register():

    st.title("Build your Agent")
    new_username = st.text_input("Set your Username", key="register_username")
    new_password = st.text_input("Set your Password", type="password", key="register_password")
    user_data = load_user_data()
    agent_name = st.text_input("Agent Name")
    org_name = st.text_input("Organization Name")
    description = st.text_area("Organization Description")
    sql_path = st.text_input("SQL Path")
    table_name = st.text_input("Table Name")
    website = st.text_input("Website (if any)")
    documents = st.file_uploader("Upload Documents (PDFs)", type="pdf", accept_multiple_files=True)
    sec_key = os.getenv("HUGGINGFACE_KEY")

    if st.button("Submit"):
        if new_username in user_data:
            st.error("Username already exists")
        else:
            user_data[new_username] = {'password': new_password, 'agent_name': agent_name, 'org_name': org_name }
            save_user_data(user_data)
            st.success("Registration successful! Please login.")
            st.session_state.page = "Login"
            st.session_state.username = new_username
            st.session_state.agent_name = agent_name
            st.session_state.org_name = org_name
            st.session_state.description = description
            st.session_state.sql_path = sql_path
            st.session_state.table_name = table_name
            st.session_state.website = website
            st.session_state.documents = documents
            st.session_state.sec_key = sec_key
            st.session_state.page = 'chat'

            sql_agent = SQLAgent()
            website_agent = WebsiteAgent()
            pdf_agent = PDFAgent()

            sql_data = sql_agent.run(st.session_state.sql_path, st.session_state.table_name) if (
                st.session_state.sql_path) else []
            website_data = website_agent.run(st.session_state.website) if st.session_state.website else ""
            pdf_data = pdf_agent.run(st.session_state.documents) if st.session_state.documents else []

            # Combine results and query LLM
            combined_data = combine_results(sql_data, website_data, pdf_data)
            process_text(new_username, combined_data)

            # model = genai.GenerativeModel('gemini-pro')
            st.session_state.llm = genai.GenerativeModel('gemini-1.5-pro-001')
            # os.environ["HUGGINGFACEHUB_API_TOKEN"] = sec_key repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
            # st.session_state.llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7,
            # token=sec_key)
            st.session_state.page = 'chat'
