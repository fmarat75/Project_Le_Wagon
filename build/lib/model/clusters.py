import pickle
import os
from sklearn.cluster import KMeans
import openai
from sklearn.metrics.pairwise import cosine_similarity
from model.params import *
import numpy as np
from google.cloud import storage
import io

def load_model():
    '''Load the fited kmeans cluster model'''

    if LOAD_MODEL == "gcp":
        # Specify your bucket name and file name
        bucket_name = BUCKET_NAME
        blob_name = 'km_model_OpenAi.pkl'

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
        model = pickle.load(in_memory_file)

    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "km_model_OpenAi.pkl")
        model = pickle.load(open(filepath,"rb"))

    return model


def get_embedding(ingredients_text):
    '''Get embedding of the ingredients text'''
    openai_model = "text-embedding-ada-002"
    openai.api_key = OPENAI_KEY
    igre_embedding = openai.Embedding.create(input = ingredients_text, model = openai_model)

    return np.array(igre_embedding["data"][0]["embedding"])


def get_cosine(igre_embedding):
    ''' Get cosine matrix vs. trained embeddings'''

    if LOAD_MODEL == "gcp":
        # Specify your bucket name and file name
        bucket_name = BUCKET_NAME
        blob_name = 'ten_embeddings_temp_array_nom.pkl'

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
        dataset_embeddings_10 = pickle.load(in_memory_file)

    else:
        parent_dir = os.getcwd()
        filepath = os.path.join(parent_dir, "raw_data", "ten_embeddings_temp_array_nom.pkl")
        dataset_embeddings_10 = pickle.load(open(filepath,"rb"))

    ingre_embedding_reshapped = igre_embedding.reshape(1, 1536)
    cos_sim_ingre_embed = cosine_similarity(ingre_embedding_reshapped, dataset_embeddings_10)

    return cos_sim_ingre_embed


def get_cluster(ingredients_text):
    '''Get Cluster based on ingredients'''

    #Load Model
    model = load_model()

    # Get embedding of the ingredients text
    ingre_embedding = get_embedding(ingredients_text)

    # Get cosine matrix vs. trained embeddings
    cos_sim_ingre_embed = get_cosine(ingre_embedding)

    # Get clusters
    cluster_label = model.predict(cos_sim_ingre_embed)

    print("\n✅ get_cluster() done \n")
    print(f"Cluster label for ingredients '{ingredients_text}' is {cluster_label[0]}\n")

    return cluster_label[0]
