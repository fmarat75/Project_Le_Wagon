import streamlit as st
from amerigo_py_files.unique_ingredients_module import load_ingredient_list
from amerigo_py_files.amerigo_functions import *
from streamlit_extras.switch_page_button import switch_page
import subprocess
import os

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

#subprocess.run(['pip', 'install', '-e', '.'])

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
filepath = os.path.join(parent_dir, "background", "f_ingredients-fruits-and-vegetable-lewagon-project.png")
set_background(filepath)

st.title("🥒🍗🥕 Ingredients 🍅🍤🥬")
st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space

# Define your list of elements
elements = load_ingredient_list()

st.session_state.selected_ingredients_list = 'No ingredients selected so far'
st.session_state.selected_ingredients_list = st.multiselect("Select ingredients", elements)
st.session_state.selected_ingredients_text = " ".join(st.session_state.selected_ingredients_list)

st.markdown(" ")  # Adds a space
st.markdown(" ")  # Adds a space

# Create two columns for the buttons
col1, spacer, col2 = st.columns([1, 2, 1])

if not st.session_state.selected_ingredients_list:
    disable_button = True
else:
    disable_button = False

# Place the second button in the second column
with col2:
    btn = st.button('Next: Your mood', disabled=disable_button)
    if btn:
        switch_page('Feelings')
