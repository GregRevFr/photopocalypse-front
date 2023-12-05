import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json
import base64
from streamlit_card import card

st.set_page_config(page_title="BLURBUSTER",
                    page_icon=":bar_chart:",
                    layout="wide")

def build_blurnotblur_page_single():

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
        # Display the resized logo in the sidebar
        print(file)
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
            print(r.status_code)

            if r.status_code == 200:
                st.success('API Called With success...Updating Cards Parameters')
                # Get the content of the uploaded file
                print(file)
                file.seek(0)

                file_content = file.read()
                print('FILE CONTENT:', file_content)

                file_extension = file.type.split("/")[-1]
                # Display the card with the uploaded image
                encoded = base64.b64encode(file_content)
                print('ENCODED',encoded)
                data = f"data:image/{file_extension};base64,{encoded.decode('utf-8')}"
                print(data)
                output = json.loads(r.text)
                image_sharpness = output.get('sharpness', 0)

                res = card(
                    title="Image Blur",
                    text=f"This image has a {image_sharpness}% of blur.",
                    image=data,
                    styles={
                        "card": {
                            "width": "500px",
                            "height": "500px",
                            "border-radius": "60px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
                        },
                        "text": {
                            "font-family": "serif"
                        }
                    }
                )
                # Display the card
                # st.write(res)
            else:
                st.warning('Something went wrong!')


def build_blurnotblur_page_multiple():

    st.title("Check if is blur")
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

     # List to store cards
    cards = []

    for file in uploaded_files:
        # Display the resized logo in the sidebar
        print(file)
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
            print(r.status_code)

            if r.status_code == 200:
                st.success('API Called With success...Updating Cards Parameters')
                # Get the content of the uploaded file
                print(file)
                file.seek(0)

                file_content = file.read()
                print('FILE CONTENT:', file_content)

                file_extension = file.type.split("/")[-1]
                # Display the card with the uploaded image
                encoded = base64.b64encode(file_content)
                print('ENCODED',encoded)
                data = f"data:image/{file_extension};base64,{encoded.decode('utf-8')}"
                print(data)
                output = json.loads(r.text)
                image_sharpness = output.get('sharpness', 0)

                res = card(
                    title="Image Blur",
                    text=f"This image has a {image_sharpness}% of blur.",
                    image=data,
                    styles={
                        "card": {
                            "width": "250px",
                            "height": "250px",
                            "border-radius": "30px",
                            "box-shadow": "0 0 10px rgba(0,0,0,0.5)"
                        },
                        "text": {
                            "font-family": "serif"
                        }
                    }
                )
                cards.append(res)

                # Display the card
                # st.write(res)
            else:
                st.warning('Something went wrong!')

    return cards

    """
    # Display cards side by side
    col1, col2 = st.columns(2)
    with col1:
        st.write('text_1')
    with col2:
        st.write('text_2')
    """
def display_columns(cards):
    col1, col2 = st.columns(2)
    for i, card_item in enumerate(cards):
        if i % 2 == 0:
            col1.write(card_item)
            col1.write('text_1')
        else:
            col2.write(card_item)
            col2.write('text_2')

def sidebar_menu():
    with st.sidebar:
        selected = option_menu(menu_title="BLURBUSTER",
                               options=["home","blurnotblur","blurnotblur_multiple"],
                               icons=["house","rocket","rocket"],
                               menu_icon="cast",
                               default_index=1,
                               styles={
                                    "icon": {"color": "#0080FF", "font-size": "25px"},
                                    "nav-link-selected": {"background-color": "#000099"},
                                    #"nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                    #"container": {"padding": "0!important", "background-color": "#fafafa", "font-family": "Permanent Marker"},
                                })

    if selected == "blurnotblur":
        build_blurnotblur_page_single()
    elif selected == "home":
        pass

    if selected == "blurnotblur_multiple":
        cards = build_blurnotblur_page_multiple()
        display_columns(cards)
    elif selected == "home":
        pass

def main():
    pass

def image_logo():
    col1, col2,col3 = st.columns([1, 2, 3])
    # Leave the first column empty
    # In the second column, add the image and apply CSS styling
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
            f'<img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="position: absolute; top: 0px; right: 0px; max-width: 35%;">',
            unsafe_allow_html=True)

image_logo()

if __name__ == '__main__':
    main()
    sidebar_menu()
