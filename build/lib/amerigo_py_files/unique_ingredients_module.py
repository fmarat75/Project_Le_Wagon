import pandas as pd
import ast
import string
from google.cloud import storage
import io
from model.params import *
import pickle


def remove_punctuation_and_capitalize(word_list):
    # Define a translation table to remove punctuation
    translation_table = str.maketrans('', '', string.punctuation)

    # Remove punctuation and capitalize for each word in the list
    cleaned_words = [word.translate(translation_table).capitalize() for word in word_list]

    return cleaned_words

def get_unique_ingredients():
    df = pd.read_csv('raw_data/RAW_recipes.csv')
    df['ingredients'] = df['ingredients'].apply(ast.literal_eval)

    # Create a set to store unique ingredients
    unique_ingredients = set()

    # Iterate through each row and add ingredients to the set
    for ingredients_list in df['ingredients']:
        unique_ingredients.update(ingredients_list)

    # Take out punctuation from text and capitalize
    unique_ingredients = remove_punctuation_and_capitalize(unique_ingredients)

    return unique_ingredients


def load_ingredient_list():

    if LOAD_MODEL == "gcp":
        # Specify your bucket name and file name
        bucket_name = BUCKET_NAME
        blob_name = 'element_list.pkl'

        # Initialize the client
        client = storage.Client()

        # Get the bucket and blob
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Download the blob to an in-memory file
        in_memory_file = io.BytesIO()
        blob.download_to_file(in_memory_file)
        in_memory_file.seek(0)  # Important: move back to the start of the file before reading

        # Load the model directly from the in-memory file
        ingredient_list = pickle.load(in_memory_file)

    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "element_list.pkl")
        ingredient_list = pickle.load(open(filepath,"rb"))

    return ingredient_list
