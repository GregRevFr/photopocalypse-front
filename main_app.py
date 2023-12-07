import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64
from PIL import Image
from io import BytesIO

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
    image_container_height = "200px"
    card_style = "; ".join(f"{key}: {value}" for key, value in styles.get("card", {}).items())
    text_style = "; ".join(f"{key}: {value}" for key, value in styles.get("text", {}).items())

    html_content = f"""
    <div style="{card_style}">
        <div style="height: {image_container_height};">
            <img src="{image}" alt="{title}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 7px;">
        </div>
    </div>
    """
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

    st.markdown("<h1 style='color: #000066;'>Check if is blur</h1>", unsafe_allow_html=True)

    # Container for the file uploader
    with st.container():
        uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True,
                                          type=["txt", "csv", "pdf", "json", "png", "jpg", "svg", "jpeg"])

    # Check if files are uploaded before attempting to display them
    if uploaded_files:
        image_cards = []
        for file in uploaded_files:
            response = send_file_to_server(file)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                base64_image = image_to_base64(image)
                image_sharpness = "Unknown"  # Replace with actual sharpness value if available
                headers = response.headers
                blurriness = headers.get("classification")
                border_color = "red" if blurriness and blurriness.startswith("This picture is blurry.") else "green"

                # Create a dictionary for each image with its details
                image_cards.append({
                    "file_name": file.name,
                    "base64_image": base64_image,
                    "border_color": border_color,
                    "sharpness": image_sharpness
                })

        # Sort the list of cards by border_color, green first then red
        image_cards.sort(key=lambda x: x['border_color'], reverse=True)

        # Display sorted cards
        with st.container():
            cols = st.columns(3)
            col_index = 0

            for image_card in image_cards:
                card_html = card(
                    title=image_card["file_name"],
                    text=f"This image has a {image_card['sharpness']}% of blur.",
                    image=f"data:image/png;base64,{image_card['base64_image']}",
                    styles={
                        'card': {
                            "width": "100%",
                            "height": "auto",
                            "margin": "10px",
                            "border-radius": "10px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                            "display": "flex",
                            "flex-direction": "column",
                            "align-items": "center",
                            "border-color": image_card["border_color"],
                            "border-style": "solid",
                            "border-width": "4px"
                        },
                        'text': {
                            "font-family": "calibri"
                        }
                    }
                )
                cols[col_index % 3].markdown(card_html, unsafe_allow_html=True)
                col_index += 1

# Function to display a sidebar menu
def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="BLURBUSTER",
            options=["home", "blurnotblur"],
            icons=["house","rocket"],
            menu_icon="cast",
            default_index=1,
            styles={
                "container": {"padding": "0!important", "background-color": "#F0F2F6"},
                "icon": {"color": "#0080FF", "font-size": "25px"},
                "nav-link-selected": {"background-color": "#000066", "color": "#FFFFFF"},
            }
        )
    if selected == "blurnotblur":
        build_blurnotblur_page()
    elif selected == "home":
        st.write("Welcome home!")

# Call the sidebar menu function when the script runs
if __name__ == '__main__':
    sidebar_menu()
