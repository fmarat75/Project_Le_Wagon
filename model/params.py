import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

#SECRETS_OR_ENV = "streamlit_secrets"
#SECRETS_OR_ENV = "local"

LOAD_MODEL = os.environ.get("LOAD_MODEL")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
LANGCHAIN_CLOSEST_DOCS = int(os.environ.get("LANGCHAIN_CLOSEST_DOCS"))
BUCKET_NAME = os.environ.get("BUCKET_NAME")

# if SECRETS_OR_ENV == "streamlit_secrets":
#     LOAD_MODEL = st.secrets['LOAD_MODEL']
#     OPENAI_KEY = st.secrets['OPENAI_KEY']
#     LANGCHAIN_CLOSEST_DOCS = int(st.secrets['LANGCHAIN_CLOSEST_DOCS'])
#     BUCKET_NAME = st.secrets['BUCKET_NAME']
#     WITH_FILTER = st.secrets['WITH_FILTER']

# else:
#     LOAD_MODEL = os.environ.get("LOAD_MODEL")
#     OPENAI_KEY = os.environ.get("OPENAI_KEY")
#     LANGCHAIN_CLOSEST_DOCS = int(os.environ.get("LANGCHAIN_CLOSEST_DOCS"))
#     BUCKET_NAME = os.environ.get("BUCKET_NAME")
#     WITH_FILTER = os.environ.get("WITH_FILTER")
