import streamlit as st
from amerigo_py_files.amerigo_functions import *
from streamlit_extras.switch_page_button import switch_page
import subprocess
import os


__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


subprocess.run(['pip', 'install', '-e', '.'])

st.set_page_config(initial_sidebar_state="collapsed")
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
filepath = os.path.join(parent_dir, "background", "f_app-lewagon-project.png")
set_background(filepath)

# Custom CSS to center the header
st.markdown("""
<style>
.centered {
text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Use the custom class in your header
st.markdown('<h1 class="centered">WELCOME TO RECIPE GENERATOR!</h1>', unsafe_allow_html=True)

st.write(" ")
st.write(" ")
st.write(" ")

st.write('Find recipes that suits you based on:')
st.write('- the ingredients you have')
st.write('- your available time')
st.write('- and .... HOW YOU ARE FEELING! 🙂')

st.write(" ")
st.write(" ")
st.write(" ")

btn = st.button('Press here to start!')


if btn:
   switch_page('ingredients')
