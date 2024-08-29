import streamlit as st
import uuid
import json
from dotenv import load_dotenv
from utils import get_context, load_user_data
from PIL import Image

load_dotenv()

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
if 'show_tickets' not in st.session_state:
    st.session_state.show_tickets = False
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

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


def load_tickets():
    """Load tickets from a JSON file."""
    try:
        with open('tickets.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tickets(tickets):
    """Save tickets to a JSON file."""
    with open('tickets.json', 'w') as file:
        json.dump(tickets, file, indent=4)


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
                .fixed-bottom {
                    background-color: #222;
                    padding: 10px;
                    border-top: 1px solid #555;
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    z-index: 1000;
                }
                .chat-container {
                    margin-bottom: 60px;  /* Adjust this value based on the height of your input box */
                }
                .modal-like {
                    position: fixed;
                    top: 10%;
                    left: 10%;
                    width: 80%;
                    height: 80%;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.3);
                    z-index: 1000;
                    padding: 20px;
                    overflow-y: auto;
                }
                .blur-background {
                    filter: blur(5px);
                }
                @keyframes slideInFromRight {
                    0% {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    100% {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }

                @keyframes fadeOut {
                    0% {
                        opacity: 1;
                    }
                    100% {
                        opacity: 0;
                    }
                }
                .welcome-message {
                    position: fixed;
                    top: 20%;
                    right: 0;
                    background-color: #6800b5;
                    color: white;
                    padding: 20px 40px;
                    border-radius: 30px 0 0 30px;
                    font-size: 24px;
                    text-align: right;
                    z-index: 1001;
                    box-shadow: -5px 0 15px rgba(0,0,0,0.1);
                    animation: slideInFromRight 1s ease-out forwards, fadeOut 1s ease-in 4s forwards;
                }
                .copyright {
                    position: fixed;
                    bottom: 15px;
                    right: 10px;
                    transform: translateX(-50%);
                    font-size: 20px;
                    color: #333;
                    text-align: right;
                    width: auto;
                    z-index: 1000;
                    font-weight: bold;
                }
                </style>
                """, unsafe_allow_html=True)

    # Create three columns
    left_col, center_col, right_col = st.columns([1, 2, 1])

    # Left column: View Tickets Button
    with left_col:
        if st.button("View Tickets"):
            st.session_state.show_tickets = True

    # Right column: Organization name
    with right_col:
        st.markdown(f'<h2 style="text-align: right; margin-bottom: 20px;">{st.session_state.org_name}</h2>',
                    unsafe_allow_html=True)

    # If the modal is active, blur the background
    if st.session_state.show_tickets:
        st.markdown("### Tickets")
        tickets = load_tickets()
        if tickets:
            for ticket in tickets:
                if ticket['organisation']==st.session_state.org_name:
                    st.write(f"Ticket ID: {ticket['id']}")
                    st.write(f"Name: {ticket['name']}")
                    st.write(f"Phone Number: {ticket['phone_number']}")
                    st.write("Conversation History:")
                    for role, message in ticket["content"]:
                        st.write(f"{role}: {message}")
                    st.markdown("---")
        else:
            st.warning("No tickets found.")
        if st.button("Close Tickets"):
            st.session_state.show_tickets = False
        st.stop()

        # Display the tickets in a modal-like overlay
    if st.session_state.get('show_tickets', False):
        st.markdown('<div class="modal-like">', unsafe_allow_html=True)
        st.markdown("### Tickets")
        if st.session_state.tickets:
            for ticket in st.session_state.tickets:
                st.write(f"Ticket ID: {ticket['id']}")
                st.write(f"Name: {ticket['name']}")
                st.write(f"Phone Number: {ticket['phone_number']}")
                st.write("Conversation History:")
                for role, message in ticket["content"]:
                    st.write(f"{role}: {message}")
                st.markdown("---")
        else:
            st.warning("No tickets found.")
        if st.button("Close", key="close_tickets"):
            st.session_state.show_tickets = False
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.show_welcome and st.session_state.user_details_entered:
        st.markdown(f'''
                <div class="welcome-message">
                    Welcome, {st.session_state.user_name}!<br>
                    How can I help you today?
                </div>
            ''', unsafe_allow_html=True)
    if not st.session_state.get('show_tickets', False):
        # Continue with the main chat UI
        if not st.session_state.user_details_entered:
            st.session_state.user_name = st.text_input("Please enter your name:", key="user_name_input")
            st.session_state.contact_detail = st.text_input("Please enter your contact detail:", key="contact_detail_input")
            if st.button("Submit"):
                if st.session_state.user_name and st.session_state.contact_detail:
                    st.session_state.user_details_entered = True
                else:
                    st.warning("Please fill in both fields before submitting.")
        else:
            # Chat container
            chat_container = st.container()
            with chat_container:
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for sender, message in st.session_state.conversation:
                    if sender == "User":
                        st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

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

                    try:
                        response = st.session_state.llm.generate_content([formatted_prompt])
                        if ("I am not aware of the answer at this moment and will raise a ticket for the admin to "
                            "review.") in response.text:
                            ticket = {
                                "id": str(uuid.uuid4()),
                                "organisation": st.session_state.org_name,
                                "content": st.session_state.conversation,
                                "name": st.session_state.user_name,
                                "phone_number": st.session_state.contact_detail
                            }
                            tickets = load_tickets()
                            tickets.append(ticket)
                            save_tickets(tickets)
                        st.session_state.conversation.append(("User", user_input))
                        st.session_state.conversation.append(("Agent", response.text))
                        st.session_state.clear_input = True
                        st.session_state.show_welcome = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating response: {e}")
            st.markdown(
                '<div class="copyright">© 2024 Powered by GreymanAI</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    chat()
