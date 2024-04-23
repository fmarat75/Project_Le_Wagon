import requests
import streamlit as st
from amerigo_py_files.unique_ingredients_module import get_unique_ingredients
import base64

def main_text_storage():
    user_text = st.text_input("Enter your text:")

    return user_text

def select_ingredients_interface():

    # Define your list of elements
    elements = get_unique_ingredients()

    selected_elements = st.multiselect("Select Elements", elements)

    return selected_elements

def select_time():
    # Display a slider for time selection
    selected_time = st.slider("Select Time (in minutes):", 0, 240, step=5, value=(0, 240))

    return selected_time

def preferences():
    """
    Section for preferences with a search box providing customized suggestions.
    """
    st.title("Select restriction🥩🧀")

    preferences = ["gluten free", "vegan", "vegetarian", "light", "healthy"]

    selected_preferences = st.multiselect("Select Elements", preferences)


    return selected_preferences

#background-color: #f0f2f6; /* Set your desired background color */

def background():
    # Set background color
    st.markdown(

        """
        <style>
            body {
            }
            /* Set background image */
            body::before {
                content: '';
                background-image: url('background.jpg');
                background-size: contain;
                background-position: center;
                background-repeat: no-repeat;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                z-index: -1;
                opacity: 0.5; /* Adjust the opacity of the background image */
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def save_text(text): #not used for now
    # Here you can implement the logic to save the text to a file or database
    # For demonstration, let's just append it to a text file
    with open("stored_text.txt", "a") as file:
        file.write(text + "\n")

import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("app.py")

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def check_links(urls):
    good_links = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            good_links.append(url)
    return good_links
