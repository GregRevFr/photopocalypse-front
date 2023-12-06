import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64
from PIL import Image
from io import BytesIO
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64


# Function to send file to server
def send_file_to_server(file):
    url = 'https://phurge-api-ieuwqkua2q-ew.a.run.app/upload-image/'
    files = {'file': (file.name, file, 'multipart/form-data')}
    response = requests.post(url, files=files)
    return response

# Function to convert image to base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to generate HTML content for a card
def card(title, text, image, styles):
    card_style = "; ".join(f"{key}: {value}" for key, value in styles.get("card", {}).items())
    text_style = "; ".join(f"{key}: {value}" for key, value in styles.get("text", {}).items())

    html_content = f"""
    <div style="{card_style}">
        <img src="{image}" alt="{title}" style="width: 100%; height: 100%; margin-top: 20px;">
    </div>
    """
            # <h3 style="{text_style}">{title}</h3>
        # <p style="{text_style}">{text}</p>
    return html_content

# Function to build the main page
def build_blurnotblur_page():
    # Custom CSS to hide the file uploader status
    st.markdown("""
        <style>
        /* This hides the uploaded file information in Streamlit */
        .st-emotion-cache-fqsvsg.e1b2p2ww9 {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color: #000099;'>Check if is blur</h1>", unsafe_allow_html=True)

    # Container for the file uploader
    with st.container():
        uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True,
                                          type=["txt", "csv", "pdf", "json", "png", "jpg", "svg", "jpeg"])


    # Check if files are uploaded before attempting to display them
    if uploaded_files:
        # Container to hold all image cards
        with st.container():
            # Create columns for the cards
            cols = st.columns(3)
            col_index = 0

            # Iterate over uploaded files and create cards
            for file in uploaded_files:
                # Send file to server and get response
                response = send_file_to_server(file)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    base64_image = image_to_base64(image)
                    image_sharpness = "Unknown"  # Replace with actual sharpness value if available

                    # Display the image card using the custom HTML and CSS
                    card_html = card(
                        title=file.name,
                        text=f"This image has a {image_sharpness}% of blur.",
                        image=f"data:image/png;base64,{base64_image}",
                        styles={
                            'card': {
                                "width": "100%",
                                "height": "auto",
                                "margin": "10px",
                                "border-radius": "10px",
                                "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                                "display": "flex",
                                "flex-direction": "column",
                                "align-items": "center"
                            },
                            'text': {
                                "font-family": "calibri"
                            }
                        }
                    )
                    # Using unsafe_allow_html to allow custom HTML
                    cols[col_index % 3].markdown(card_html, unsafe_allow_html=True)
                    col_index += 1

# Function to display a sidebar menu
def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="BLURBUSTER",
            options=["home", "blurnotblur"],
            icons=["house", "rocket"],
            menu_icon="cast",
            default_index=1,
            styles={
                "icon": {"color": "#0080FF", "font-size": "25px"},
                "nav-link-selected": {"background-color": "#000099"},
            }
        )
    if selected == "blurnotblur":
        build_blurnotblur_page()
    elif selected == "home":
        st.write("Welcome home!")  # Replace with actual home page content

# Call the sidebar menu function when the script runs
if __name__ == '__main__':
    sidebar_menu()
