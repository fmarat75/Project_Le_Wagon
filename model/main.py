from model.clusters import get_cluster
from model.recipe import get_selected_recipe_link_list
from google.cloud import storage
from model.params import *
import io
import pandas as pd
import pickle

############################ Diogo Changes #####################################
from st_files_connection import FilesConnection

conn = st.connection('gcs', type=FilesConnection)
recipe_reviews_simple_np_from_gcp = conn.read("bucket-for-testing-madrid/recipe_reviews_simple.csv", input_format="csv", ttl=600).to_numpy()
recipe_reviews_simple_df_from_gcp = pd.DataFrame(recipe_reviews_simple_np_from_gcp, columns=["my_index", "recipe_id", "nb_reviews", "avg_rating"])
#################################################################################

def get_review_data(recipe_id_list):

    if LOAD_MODEL == "gcp":
        # # Specify your bucket name and file name
        # bucket_name = BUCKET_NAME
        # blob_name = 'recipe_reviews_simple.pkl'

        # # Initialize the client
        # client = storage.Client()

        # # Get the bucket and blob
        # bucket = client.get_bucket(bucket_name)
        # blob = bucket.blob(blob_name)

        # # Download the blob to an in-memory file
        # in_memory_file = io.BytesIO()
        # blob.download_to_file(in_memory_file)
        # in_memory_file.seek(0)  # Important: move back to the start of the file before reading

        # # Load the model directly from the in-memory file
        # recipe_reviews_simple_df = pickle.load(in_memory_file)

        recipe_reviews_simple_df = recipe_reviews_simple_df_from_gcp
    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "recipe_reviews_simple.pkl")
        recipe_reviews_simple_df = pickle.load(open(filepath,"rb"))


    return recipe_reviews_simple_df



def main(ingredient_text, user_prompt, time, selected_ingredients_list=[]):

    ingredient_text = ingredient_text.lower()
    selected_ingredients_list = [item.lower() for item in selected_ingredients_list]

    #predict function
    my_clust = get_cluster(ingredient_text)
    final_df, warning, message = get_selected_recipe_link_list(cluster_label=my_clust,
                                                                         query=user_prompt,
                                                                         time=time,
                                                                         ingredient_list=selected_ingredients_list)

    name_list = final_df["recipe_name"].to_list()
    recipe_id_list = final_df["recipe_id"].to_list()

    recipe_reviews_simple_df = get_review_data(recipe_id_list)
    recipe_reviews_simple_df["recipe_id"] = recipe_reviews_simple_df["recipe_id"].astype("object")
    final_df = final_df.merge(recipe_reviews_simple_df, how = "inner")
    final_df['recipe_name'] = pd.Categorical(final_df['recipe_name'], categories=name_list, ordered=True)
    final_df = final_df.sort_values('recipe_name')

    print("\n:white_check_mark: Main Executed \n")

    return final_df, warning, message
