import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64
from PIL import Image
from io import BytesIO

# Function to send file to server
def send_file_to_server(file):
    """
    Sends a file to the server using a POST request.

    Args:
        file: The file to be sent.

    Returns:
        The response from the server.
    """
    url = 'https://phurge-api-ieuwqkua2q-ew.a.run.app/upload-image/'
    files = {'file': (file.name, file, 'multipart/form-data')}
    response = requests.post(url, files=files)
    return response

# Function to convert image to base64
def image_to_base64(image):
    """
    Convert an image to base64 encoding.

    Args:
        image: The image to be converted.

    Returns:
        The base64 encoded string representation of the image.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Function to build the main page
def build_blurnotblur_page():
    """
    Build the blur-not-blur page.

    This function creates a page where users can upload images and check if they are blurry or not.
    It displays the uploaded images along with their blur percentage.

    Returns:
        None
    """
    # Set the page title
    st.markdown(
        f'<h1 style="color: {"#000099"};">Check if is blur</h1>',
        unsafe_allow_html=True
    )

    # Allow users to upload files
    uploaded_files = st.file_uploader(
        "Choose a file",
        accept_multiple_files=True,
        type=["txt", "csv", "pdf", "json", "png", "jpg", "svg", "jpeg"]
    )

    # Position the file uploader at the upper-left corner
    st.markdown(
        '<style>'
        'div[data-testid="stFileUploader"] { position: absolute; top: 0px; left: 0px; }'
        '</style>',
        unsafe_allow_html=True
    )


    cards = [] # Initialize cards list

    # Process each uploaded file
    for file in uploaded_files:
        response = send_file_to_server(file)

        # if response.status_code == 200:
            # st.success(f'File {file.name} successfully uploaded and processed by server.')

        # Convert the response content to an image and then to base64
        image = Image.open(BytesIO(response.content))
        base64_image = image_to_base64(image)

        # Create a card with image details
        cards.append({
            "title": "Image",
            "text": "This image has a {image_sharpness}% of blur.",
            "image": f"data:image/png;base64,{base64_image}",
            "styles": {
                'card': {
                    "width": "250px",
                    "height": "280px",
                    "margin-right": "10px",
                    "margin-bottom": "30px",
                    "border-radius": "10px",
                    "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center"
                },
                'text': {
                    "font-family": "calibri"
                }
            },
            "position": {
                "top": "1000px",
                "left": "100px"
            }
        })

    # Display the cards
    display_columns(cards)

def card(title, text, image, styles, position=None):
    """
    Generate HTML content for a card.

    Args:
    title (str): The title of the card.
    text (str): The text of the card.
    image (str): URL or base64 encoded image for the card.
    styles (dict): Dictionary containing styles for the card.
    position (dict): Dictionary containing position properties (top, left) for the card.

    Returns:
    str: HTML content of the card.
    """
    card_style = "; ".join(f"{key}: {value}" for key, value in styles.get("card", {}).items())
    text_style = "; ".join(f"{key}: {value}" for key, value in styles.get("text", {}).items())

    html_content = f"""
    <div style="{card_style}">
        <h3 style="{text_style}">{title}</h3>
        <p style="{text_style}">{text}</p>
        <img src="{image}" alt="{title}" style="width: 70%; max-width: 70%; height: auto; margin-top: 20px;">
    </div>
    """
    return html_content

def display_columns(cards):
    """
    Display the given cards in multiple columns.

    Args:
        cards (list): A list of dictionaries representing the cards to be displayed.
            Each dictionary should have the following keys: "title", "text", "image", "styles".

    Returns:
        None
    """
    num_columns = 3
    num_cards = len(cards)

    # Calculate the number of rows needed
    num_rows = (num_cards + num_columns - 1) // num_columns

    # Create columns dynamically based on the number of cards
    columns = [st.columns(num_columns) for _ in range(num_rows)]

    # Iterate over cards and distribute them to columns
    card_index = 0
    for row in columns:
        for col in row:
            if card_index < num_cards:
                card_content = card(
                    title=cards[card_index]["title"],
                    text=cards[card_index]["text"],
                    image=cards[card_index]["image"],
                    styles=cards[card_index]["styles"],
                )
                col.markdown(card_content, unsafe_allow_html=True)
                card_index += 1

def sidebar_menu():
    """
    Function to display a sidebar menu with options and icons.
    The selected option determines which page to build.
    """
    with st.sidebar:
        selected = option_menu(
            menu_title="BLURBUSTER",
            options=["home","blurnotblur"],
            icons=["house","rocket"],
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
        pass

def image_logo():
    """
    Display the logo image on the webpage.

    This function displays the logo image on the webpage using the provided image path.
    It also checks if the image file exists and prints a message accordingly.

    Returns:
        None
    """
    col1, col2, col3 = st.columns([1, 2, 3])

    # Leave the first and second column empty
    with col3:
        image_path = 'photos/Captura.png'


        st.markdown(
            f'<img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="position: absolute; top: 0px; right: 0px; max-width: 25%;">',
            unsafe_allow_html=True
        )

image_logo()

if __name__ == '__main__':
    sidebar_menu()
