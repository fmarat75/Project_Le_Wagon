import numpy as np
import pandas as pd
import ast
import os
import pickle
from model.params import *
from google.cloud import storage
import io

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document

from st_files_connection import FilesConnection

conn = st.connection('gcs', type=FilesConnection)
preprocessed_data = conn.read("bucket-for-testing-madrid/preprocessed_data.csv", input_format="csv", ttl=600)
preprocessed_data_with_ingredients = conn.read("bucket-for-testing-madrid/preprocessed_data_with_ingredients.csv", input_format="csv", ttl=600)


def load_preprocessed_dataset():
    '''Load the preprocessed dataset'''

    if LOAD_MODEL == "gcp":
        # # Specify your bucket name and file name
        # bucket_name = BUCKET_NAME
        # blob_name = 'preprocessed_data.pkl'

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
        # preprocessed_dataset = pickle.load(in_memory_file)
        preprocessed_dataset = preprocessed_data
    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "preprocessed_data.pkl")
        preprocessed_dataset = pickle.load(open(filepath,"rb"))

    print("\n✅ preprocessed_dataset loaded \n")

    return preprocessed_dataset


def load_preprocessed_dataset_with_ingredients():
    '''Load the preprocessed dataset with ingredients'''

    if LOAD_MODEL == "gcp":
        # # Specify your bucket name and file name
        # bucket_name = BUCKET_NAME
        # blob_name = 'preprocessed_data_with_ingredients.pkl'

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
        # preprocessed_dataset_with_ingredients = pickle.load(in_memory_file)
        preprocessed_dataset_with_ingredients = preprocessed_data_with_ingredients
    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "preprocessed_data_with_ingredients.pkl")
        preprocessed_dataset_with_ingredients = pickle.load(open(filepath,"rb"))

    print("\n✅ preprocessed_dataset_with_ingredients loaded \n")

    return preprocessed_dataset_with_ingredients


def run_ingredient_filter(ingredient_list, preprocessed_dataset, cluster_label):
        selected_data = preprocessed_dataset
        message = ""
        for ingredient in ingredient_list:
            selected_data = selected_data.loc[selected_data['ingredients'].str.contains(ingredient)]
            print("Filtering this ingredient: "+ ingredient+". Nb left: "+str(len(selected_data)))
            message = message + "\nFiltering this ingredient: "+ ingredient+". Nb left: "+str(len(selected_data))

        print("Number of recipes selected after filter: "+str(len(selected_data))+" (it will be capped at 6600)")
        message = message + "\nNumber of recipes selected after filter: "+str(len(selected_data))+" (it will be capped at 6600)"
        selected_data = selected_data.iloc[:6600]

        if len(selected_data) < 50:
            warning = "No recipe matches your combination of ingredients, we selected recipes in the spirit of your ingredients...."
            message = message + "\nNo recipe matches your combination of ingredients, we selected recipes in the spirit of your ingredients...."
            print(warning)
            selected_data = preprocessed_dataset[preprocessed_dataset["cluster_label"]==cluster_label]
            print("Number of recipes selected via cluster: "+ str(len(selected_data)))

        return selected_data, message



def get_selected_recipe_link_list(cluster_label, query, time, ingredient_list = []):

    ingredient_list = [item.lower() for item in ingredient_list]

    ######### Filter by Ingredients ##########
    warning = ""
    ingredient_list = [item.lower() for item in ingredient_list]

    preprocessed_dataset = load_preprocessed_dataset_with_ingredients()
    selected_data, message = run_ingredient_filter(ingredient_list, preprocessed_dataset, cluster_label)

    ######### Filter by Time ##########
    temporary_selected_data = selected_data[(selected_data["minutes"]>=time[0]) & (selected_data["minutes"]<=time[1])]
    if len(temporary_selected_data) > 10:
        selected_data = temporary_selected_data
        print("Filtering by time range "+ str(time)+". Nb left: "+str(len(selected_data)))
        message = message + "\nFiltering by time range "+ str(time)+". Nb left: "+str(len(selected_data))
    else:
        time_warning = "We did not use the time filtering, as otherwise very few recipes were left"
        message = message + "We did not use the time filtering, as otherwise very few recipes were left"
        warning = warning + "\n"+time_warning
        print(time_warning)


    ######### Langchain process ##########
    nb_recipe_selected = len(selected_data)
    print("Final number of recipes selected: "+ str(nb_recipe_selected))

    if nb_recipe_selected > 0:
        ## Create langchain list of documents

        docs = []
        for row in range(len(selected_data)):
            docs.append(Document(page_content=selected_data["final_text"].iloc[row], metadata={"source": "local"}))

        ## Set up Chroma vector
        vector_db = Chroma.from_documents(docs,
                                        OpenAIEmbeddings(openai_api_key = OPENAI_KEY,
                                                        model="text-embedding-ada-002"))

        # Querying the data
        total_query = "Can you find the recipe the most adapted to a person that indicated me: "+query

        selected_docs = vector_db.similarity_search_with_score(total_query, k = min(LANGCHAIN_CLOSEST_DOCS,nb_recipe_selected))
        print("Number of selected docs in Langchain: "+ str(len(selected_docs)))
        message = message + "\nNumber of selected docs in Langchain: "+ str(len(selected_docs))

        recipe_id_list = []
        recipe_link_list = []
        name_list = []
        similarity_score_list = []
        for doc in selected_docs:
            search_string = doc[0].page_content

            filtered_df = selected_data.loc[selected_data['final_text'].str.contains(search_string)]
            recipe_id_list.append(filtered_df["recipe_id"].tolist())
            recipe_link_list.append(filtered_df["link"].tolist())
            name_list.append(filtered_df["name"].tolist())
            similarity_score_list.append([float(doc[1])]*len(filtered_df["name"].tolist()))

        recipe_id_list = [item for sublist in recipe_id_list for item in sublist]
        name_list = [item for sublist in name_list for item in sublist]
        recipe_link_list = [item for sublist in recipe_link_list for item in sublist]
        similarity_score_list = [item for sublist in similarity_score_list for item in sublist]
        print("Number of matched docs between Langchain selection & original data: "+ str(len(name_list)))
        message = message + "\nNumber of matched docs between Langchain selection & original data: "+ str(len(name_list))

        vector_db.delete_collection()

    else:
        recipe_id_list = []
        name_list = []
        recipe_link_list = []


    print("\n✅ name_list is \n")
    print(name_list)

    ### Get % of ingredients present & time validated ###
    perc_ingre_list = []
    time_ok_list = []
    for recipe_id in recipe_id_list:
        count = 0

        recipe_df_select = preprocessed_dataset[preprocessed_dataset["recipe_id"]==recipe_id]

        for ingre in ingredient_list:
            if ingre in recipe_df_select["ingredients"].iloc[0]:
                count = count + 1
        perc_ingre_list.append(count/len(ingredient_list))

        time_ok = "no"
        if (recipe_df_select["minutes"].iloc[0]>=time[0]) and (recipe_df_select["minutes"].iloc[0]<=time[1]):
            time_ok = "yes"
        time_ok_list.append(time_ok)


    final_df = pd.DataFrame(data = {'recipe_id': recipe_id_list,
                                    'recipe_name':name_list,
                                    'recipe_link':recipe_link_list,
                                    'similarity_score': similarity_score_list,
                                    'perc_ingre':perc_ingre_list,
                                    'time_ok':time_ok_list})

    final_df = final_df.drop_duplicates(subset=['recipe_name'], keep='first')

    return final_df, warning, message
