import streamlit as st
from streamlit_option_menu import option_menu
import requests
import os
import json
import base64
from PIL import Image
from io import BytesIO

# At the beginning of your Streamlit app script, add the following
# st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* Apply the styles to the body and Streamlit's main container */
    body, .stApp {
        background: linear-gradient(45deg, #bfe9ff, #ffffff) !important;
        width: 100vw !important;
        height: 100vh !important;
        margin: 0 !important;
        overflow: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hover effect
st.markdown(
    """
    <style>
    .card {
    transition: transform 0.2s; /* Smooth transition for the transform */
    /* Your existing card styles here */
    }
    .card:hover {
    transform: scale(1.05); /* Increase the scale slightly when hovered */
    }
    </style>
    """,
    unsafe_allow_html=True)

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
    <div class="card" style="{card_style}">
        <div style="height: {image_container_height};">
            <img src="{image}" alt="{title}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 7px;">
        </div>
    </div>
    """
    return html_content

def image_logo():
    col1, col2, col3 = st.columns([1, 2, 3])
    # Leave the first column empty
    # In the second column, add the image and apply CSS styling
    with col3:
        image_path = 'photos/logo.png'
        print(f"Image Path: {image_path}")

        # Check if the file exists
        if os.path.exists(image_path):
            print("Image file exists.")
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        # Display the image with custom CSS for positioning, size, rounded corners, and border
        st.markdown(
            f'<img src="data:image/png;base64,{encoded_image}" style="position: absolute; top: 0px; right: 0px; max-width: 37%; border-radius: 10px; border: 3px solid #012862;">',
            unsafe_allow_html=True)

# Function to display a sidebar menu
def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="BLURBUSTER",
            options=["Home", "BlurNotBlur"],
            icons=["house","rocket"],
            menu_icon="cast",
            default_index=1,
            styles={
                "container": {"padding": "0!important", "background-color": "#D5D5D8"},
                "icon": {"color": "#0080FF", "font-size": "25px"},
                "nav-link-selected": {"background-color": "#012862", "color": "#FFFFFF"},
            }
        )

        # Display the legend in the sidebar
        st.markdown("""
            <div style="position: fixed; bottom: 20px; left: 40px;">
                <h1 style='color: #012862; font-size: 20px; font-family: sans-serif;'>
                Legend:</h1>
                <p style ='font-size: 17px;'><span style="display: inline-block; width: 30px; height: 7px; background-color: red;"></span> Blur picture</p>
                <p style ='font-size: 17px;'><span style="display: inline-block; width: 30px; height: 7px; background-color: blue;"></span> Picture not blur</p>
            </div>
            """,
            unsafe_allow_html=True
            )

    if selected == "BlurNotBlur":
        build_blurnotblur_page()
    elif selected == "home":
        st.write("Welcome home!")

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

    st.markdown(
        """
        <h1 style='color: #012862; font-size: 36px; font-family: sans-serif; font-weight: bold;'>
            Blurbuster</h1>
        </h1>
        """,
        unsafe_allow_html=True
)

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
                            "border-width": "4px",
                            "transition": "transform 0.2s"# Ensure this is included in your card style

                        },
                        'text': {
                            "font-family": "calibri"
                        }
                    }
                )
                cols[col_index % 3].markdown(card_html, unsafe_allow_html=True)
                col_index += 1

if __name__ == '__main__':
    # Use the gradient class for the whole page
    st.markdown('<div class="gradient-background">', unsafe_allow_html=True)
    image_logo()
    sidebar_menu()
        # Close the div tag at the end of your content
    st.markdown('</div>', unsafe_allow_html=True)
