import streamlit as st
from amerigo_py_files.amerigo_functions import *
from model.main import main
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

# Store a flag in session state to track button clicks
if "recipes_loaded" not in st.session_state:
    st.session_state["recipes_loaded"] = False


# Create a placeholder for the loading message
loading_message = st.empty()

# Display the loading message
loading_message.markdown("<br><br><br><br>Wait for it... 😊 We are working on the best recipes for you! 🍳👩‍🍳🥗", unsafe_allow_html=True)


# Load data for the Recipes page (if necessary)
if not st.session_state["recipes_loaded"]:

    parent_dir = os.getcwd()
    filepath = os.path.join(parent_dir, "background", "rsz_output-flat-lay-concept-clipboard.png")
    set_background(filepath)


    final_df, warning, message = main(ingredient_text= st.session_state.selected_ingredients_text,
                                                user_prompt= st.session_state.user_text,
                                                time= st.session_state.selected_time,
                                                selected_ingredients_list = st.session_state.selected_ingredients_list)

    st.session_state["recipes_loaded"] = True  # Mark data as loaded

    loading_message.empty()


    if len(final_df) == 0:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.write("Sorry, we couldn't indentify recipes suited to your request")
        st.markdown("<br><br><br>", unsafe_allow_html=True)
    else:
        st.markdown(" ")  # Adds a space
        st.markdown(" ")  # Adds a space
        st.markdown(" ")  # Adds a space
        st.header('Here are our suggested recipes!')
        st.markdown(" ")  # Adds a space
        st.markdown(warning)
        st.markdown(" ")  # Adds a space

        for i in range(len(final_df)):
            # Get the color based on the rating
            if final_df["similarity_score"][i] < 0.37:
                color = "green"
            elif final_df["similarity_score"][i] < 0.41:
                color = "orange"
            else:
                color = "red"

            # Time check
            time_color = "green" if final_df["time_ok"][i] == "yes" else "red"
            time_symbol = "✓" if final_df["time_ok"][i] == "yes" else "✗"

            # Combine everything into one markdown call
            st.markdown(f'''
                <div style="margin-bottom: 10px;">
                    {i+1}) <a href="{final_df["recipe_link"][i]}">{final_df["recipe_name"][i]}</a>: <span style="padding-left: 20px;">{final_df["avg_rating"][i]:.1f} ⭐ ({final_df["nb_reviews"][i]})</span>
                    <br>
                    <span style="padding-left: 20px;">Ingredients: {final_df["perc_ingre"][i]*100:.0f}%</span>
                    <span style="padding-left: 20px;">Feeling's affinity: <span style="color: {color}; font-size: 30px;">●</span></span>
                    <span style="padding-left: 20px;">Time: <span style="color: {time_color}; font-size: 30px;">{time_symbol}</span></span>
                    <br>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown(" ")  # Adds a space
        st.markdown(" ")  # Adds a space
        st.markdown("<span style=\'text-decoration: underline; font-style: italic;\'>Feeling's affinity legend:</span>", unsafe_allow_html=True)
        st.markdown(f'''
                    <div style="margin-bottom: 10px;">
                        <span style="padding-left: 5px;"><span style="color: green; font-size: 30px;">● </span>Good</span>
                        <br>
                        <span style="padding-left: 5px;"><span style="color: orange; font-size: 30px;">● </span>Average</span>
                        <br>
                        <span style="padding-left: 5px;"><span style="color: red; font-size: 30px;">● </span>Bad</span>
                        <br>
                    </div>
                ''', unsafe_allow_html=True)

    st.markdown(" ")  # Adds a space
    st.markdown(" ")  # Adds a space
    st.markdown(" ")  # Adds a space
    st.markdown(" ")  # Adds a space


btn2 = st.button('Restart')



if btn2:
    # Avoid reloading Recipes page if data is already loaded
    if st.session_state["recipes_loaded"]:
        st.session_state.clear()
        switch_page('Ingredients')
    else:
        st.warning("Recipes data is still loading. Please wait before restarting.")

# if btn2:
#     st.session_state.clear()
#     switch_page('Ingredients')
