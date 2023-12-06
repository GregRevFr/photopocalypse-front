import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64

st.set_page_config(page_title="BLURBUSTER",
                    page_icon=":bar_chart:",
                    layout="wide")

cards = []

def build_blurnotblur_page():

    st.markdown(
    f'<h1 style="color: {"#000099"};">Check if is blur</h1>',
    unsafe_allow_html=True
)
    uploaded_files = st.file_uploader("Choose a file",
                                    accept_multiple_files=True,
                                    type=["txt", "csv", "pdf", "json", "png", "jpg", "svg", "jpeg"])

    # Position the file uploader at the upper-left corner
    st.markdown(
        '<style>'
        'div[data-testid="stFileUploader"] { position: absolute; top: 0px; left: 0px; }'
        '</style>',
        unsafe_allow_html=True
    )

    for file in uploaded_files:
        # Check if the file is an image
        if 'image' in file.type:

            params = {
                'models': 'properties',
                'api_user': '1947745726',
                'api_secret': 'CjnMaFVutPnmaQHMSjuKD8rgbG'
            }
            files = {'media': file}
            r = requests.post('https://api.sightengine.com/1.0/check.json',
                              files=files, data=params)

            if r.status_code == 200:
                # st.success('API Called With success...Updating Cards Parameters')
                # Get the content of the uploaded file
                file.seek(0)

                file_content = file.read()

                file_extension = file.type.split("/")[-1]

                # Display the card with the uploaded image
                encoded = base64.b64encode(file_content)
                data = f"data:image/{file_extension};base64,{encoded.decode('utf-8')}"
                output = json.loads(r.text)
                image_sharpness = output.get('sharpness', 0)

                cards.append({
                    "title": "Image",
                    "text": f"This image has a {image_sharpness}% of blur.",
                    "image": data,
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
                st.markdown(
                '<style>'
                'div[data-testid="cards.append"] { position: absolute; top: 1000px; left: 0px; }'
                '</style>',
                unsafe_allow_html=True
                )

            else:
                st.warning('Something went wrong!')

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
    with st.sidebar:
        selected = option_menu(menu_title="BLURBUSTER",
                               options=["home","blurnotblur"],
                               icons=["house","rocket"],
                               menu_icon="cast",
                               default_index=1,
                               styles={
                                    "icon": {"color": "#0080FF", "font-size": "25px"},
                                    "nav-link-selected": {"background-color": "#000099"},
                                    #"nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                    #"container": {"padding": "0!important", "background-color": "#fafafa", "font-family": "Permanent Marker"},
                                })

    if selected == "blurnotblur":
        build_blurnotblur_page()
    elif selected == "home":
        pass

def image_logo():
    col1, col2, col3 = st.columns([1, 2, 3])

    # Leave the first and second column empty
    with col3:
        image_path = '/Users/mj/Desktop/Captura.png'
        print(f"Image Path: {image_path}")

        # Check if the file exists
        import os
        if os.path.exists(image_path):
            print("Image file exists.")
        else:
            print("Image file does not exist. Please check the file path.")

        st.markdown(
            f'<img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="position: absolute; top: 0px; right: 0px; max-width: 25%;">',
            unsafe_allow_html=True)

image_logo()

if __name__ == '__main__':
    sidebar_menu()
