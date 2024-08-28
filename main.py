import streamlit as st
from PIL import Image


def main():
    # Set page configuration
    st.set_page_config(layout="wide", page_title="GREYMAN AI")

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
            padding-top: 50px;
            padding-bottom: 50px;
            font-size: 3em;
        }
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .full-width-button {
            width: 100%;
            height: 50px;
            margin: 10px 0;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: bold;
            color: white;
        }
        .login-button {
            background-color: #4CAF50;
        }
        .register-button {
            background-color: #008CBA;
        }
        </style>
        """, unsafe_allow_html=True)

    # Create three columns
    left_col, center_col, right_col = st.columns([1, 2, 1])

    # Left column: Logo
    with left_col:
        logo = Image.open("logo.jpg")
        st.image(logo, width=250)

    # Center column: Title and buttons
    with center_col:
        # Centered title
        st.markdown('<h1 class="centered-title">GREYMAN AI</h1>', unsafe_allow_html=True)

        # Create a form container
        with st.container():

            with st.form(key="selection_form"):
                st.markdown('<h2 style="text-align: center; margin-bottom: 20px;">Welcome</h2>', unsafe_allow_html=True)

                login_clicked = st.form_submit_button("LOGIN", use_container_width=True,
                                                      help="Click to log in to your account")
                register_clicked = st.form_submit_button("REGISTER", use_container_width=True,
                                                         help="Click to create a new account")

            st.markdown('</div>', unsafe_allow_html=True)

        # Handle button clicks
        if login_clicked:
            st.switch_page("pages/login.py")
        elif register_clicked:
            st.switch_page("pages/register.py")


if __name__ == "__main__":
    main()