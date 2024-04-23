import streamlit as st
from amerigo_py_files.unique_ingredients_module import get_unique_ingredients
from amerigo_py_files.amerigo_functions import *
from streamlit_extras.switch_page_button import switch_page

import os

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

parent_dir = os.getcwd()
filepath = os.path.join(parent_dir, "background", "f_text-lewagon-project.png")
set_background(filepath)

st.title("😋 What do you feel like having? 🍽️")
st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space
st.markdown("A few examples:")
st.markdown("""*- I would like a warm meal on this cold winter night*""")
st.markdown("""*- I need an easy recipe for my kids*""")
st.markdown("""*- I am in a bad mood, I need something that cheers me up!*""")
st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space

# Text input box for the user
st.session_state.user_text = st.text_input("Enter your feelings:")

st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space

# Create two columns for the buttons
col1, spacer, col2 = st.columns([1, 2, 1])


# Place the first button in the first column
with col1:
    backbtn = st.button('Back: Ingredients')
    if backbtn:
        switch_page('Ingredients')


# Place the second button in the second column
with col2:
    btn = st.button('Next: Cooking Time')
    if btn:
        switch_page('Time')

st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space

st.markdown('<span style="text-decoration: underline; font-style: italic;">Selected Ingredients:</span>', unsafe_allow_html=True)
if st.session_state.selected_ingredients_text:
    text_to_display = f"""*{st.session_state.selected_ingredients_text}*"""
    st.markdown(text_to_display)
else:
    st.markdown("No ingredients selected yet.")  # Or a custom message
