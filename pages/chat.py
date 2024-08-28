__author__ = "Himanshu Sharma"
__copyright__ = "Copyright 2024, Personal"
__license__ = "GreymanAI ownership"
__version__ = "0.1"
__maintainer__ = "Himanshu Sharma"
__status__ = "Development"


import streamlit as st
import uuid
import json
from dotenv import load_dotenv
from utils import get_context, load_user_data
from PIL import Image

load_dotenv()

prompt = ("[SYSTEM] You are an expert customer support agent. Your role is:"
          "1. To understand the user's query and provide the most relevant response using the best available context "
          "in a concise manner."
          "2. Never provide anything apart from the answer based on the context."
          "3. To not answer irrelevant questions with respect to the context. Instead, respond with: \"This question "
          "is not relevant to the documents.\""
          "4. If you do not know the answer to the question, reply with: I am not aware of the answer at this "
          "moment and will raise a ticket for the admin to review."
          "[CONTEXT] {context}"
          "[CONVERSATION_HISTORY] {conversation_history}"
          "[USER] {user_query}")

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False
if 'user_details_entered' not in st.session_state:
    st.session_state.user_details_entered = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'contact_detail' not in st.session_state:
    st.session_state.contact_detail = ""


def chat():
    st.set_page_config(layout="wide", page_title="GREYMAN AI - Chat")
    if "agent_name" not in st.session_state or "org_name" not in st.session_state:
        st.error("Please fill out the Agent Information first.")
        st.stop()

    st.markdown("""
                <style>
                .user-message {
                    background-color: #333;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                    text-align: right;
                    float: right;
                    clear: both;
                    width: 30%;
                }
                .assistant-message {
                    background-color: #444;
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                    text-align: left;
                    float: left;
                    clear: both;
                    width: 30%;
                }
                .fixed-bottom {
                    background-color: #222;
                    padding: 5px;
                    border-top: 1px solid #555;
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                }
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

    st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Customer Support page</h2>', unsafe_allow_html=True)
    if not st.session_state.user_details_entered:
        st.session_state.user_name = st.text_input("Please enter your name:", key="user_name_input")
        st.session_state.contact_detail = st.text_input("Please enter your contact detail:", key="contact_detail_input")
        if st.button("Submit"):
            if st.session_state.user_name and st.session_state.contact_detail:
                st.session_state.user_details_entered = True
            else:
                st.warning("Please fill in both fields before submitting.")
    else:
        user_data = load_user_data()
        st.write(f"Hey, I am {st.session_state.agent_name} from {st.session_state.org_name}, how can I help you?")

        # Chat container
        chat_container = st.container()
        with chat_container:
            for sender, message in st.session_state.conversation:
                if sender == "User":
                    st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)

            st.markdown('<div class="fixed-bottom">', unsafe_allow_html=True)

            if st.session_state.clear_input:
                st.session_state.user_input = ""
                st.session_state.clear_input = False

            user_input = st.text_input("You: ", key="user_input")
            if st.button("Send"):
                if not user_input:
                    st.warning("Please enter a message before sending.")
                else:
                    st.session_state.user_query = user_input
                    context = get_context(st.session_state.username, user_input)
                    history = "\n".join([f"{role}: {message}" for role, message in st.session_state.conversation])
                    formatted_prompt = (prompt.replace("{context}", context)
                                        .replace("{user_query}", user_input)
                                        .replace("{conversation_history}", history) + "[ASSISTANT]")

                    # Ensure that st.session_state.llm is correctly initialized and has an invoke method
                    try:
                        print("Going into response")
                        response = st.session_state.llm.generate_content([formatted_prompt])
                        if ("I am not aware of the answer at this moment and will raise a ticket for the admin to "
                            "review.") in response.text:
                            ticket = {
                                "id": str(uuid.uuid4()),
                                "content": st.session_state.conversation,
                                "name": st.session_state.user_name,
                                "phone_number": st.session_state.contact_detail
                            }
                            try:
                                with open('../tickets.json', 'r') as file:
                                    tickets = json.load(file)
                            except (FileNotFoundError, json.JSONDecodeError):
                                tickets = []
                            tickets.append(ticket)

                            with open('../tickets.json', 'w') as file:
                                json.dump(tickets, file, indent=4)
                        # response = st.session_state.llm.invoke(formatted_prompt, max_length=1000, temperature=0.7)
                        st.session_state.conversation.append(("User", user_input))
                        st.session_state.conversation.append(("Agent", response.text))
                        st.session_state.clear_input = True
                        st.rerun()
                        # Set flag to clear the user input field

                    except Exception as e:
                        st.error(f"Error generating response: {e}")

                    # Update conversation history in a file
                    conversation_str = "\n".join(
                        [f"{role}: {message}" for role, message in st.session_state.conversation])
                    # Set flag to clear the user input field
                    st.session_state.clear_input = True

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    chat()
