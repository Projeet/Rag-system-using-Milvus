import sys
sys.path.append('../')

import os
from dotenv import load_dotenv
load_dotenv()
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

from tqdm.notebook import tqdm

from nvidia_llm.large_language_model import get_llm_embeddings

import warnings
warnings.filterwarnings("ignore")


CLUSTER_ENDPOINT=os.getenv("CLUSTER_ENDPOINT")
TOKEN=os.getenv("TOKEN")
def create_connection(CLUSTER_ENDPOINT, TOKEN):
    try:
        client = connections.connect(
            uri=CLUSTER_ENDPOINT, # Cluster endpoint obtained from the console
            token=TOKEN # API key or a colon-separated cluster username and password
        )
        print("Connection created successfully")

    except Exception as e:
        print("Error connection to Milvus",e)

# create_connection(CLUSTER_ENDPOINT,TOKEN)
# # Step 1: Load
# loaders = [
#  WebBaseLoader("https://en.wikipedia.org/wiki/AT%26T"),
#  WebBaseLoader("https://en.wikipedia.org/wiki/Bank_of_America")
# ]
# data = []
# for loader in loaders:
#     data.extend(loader.load())

# # Step 2: Transform (Split)
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[
#                                                "\n\n", "\n", "(?<=\. )", " "], length_function=len)
# docs = text_splitter.split_documents(data)
# print('Split into ' + str(len(docs)) + ' docs')


def create_collection(collection_name,dimension,already_exists=False):

    if already_exists:
        fields = [
            FieldSchema(name="disclosure_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="Text", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dimension)
        ]

        schema = CollectionSchema(
        fields,
        enable_dynamic_field=True,
        )

        try:

            mc = Collection(collection_name, schema)

            index_params = {
                    "metric_type":"COSINE",
                    "index_type":"IVF_FLAT",
                    "params":{"nlist":1024}
                    }

            mc.create_index(
            field_name="embeddings",
            index_params=index_params
            ) 
            print("Collection created successfully")
            return mc
        
        except Exception as e:
            print("Error creating collection",e)
        
    else:
        mc=Collection(collection_name)
        return mc

    return None

    

# mc=create_collection("chatbot_collection",1024)

# emb=get_llm_embeddings("What is the GPU memory bandwidth of H100 SXM?")


def insert_embeddings(mc):
    vector_data=[]
    for d in docs:
        # embedding=embedder.get_text_embedding(d.page_content)
        embedding=get_llm_embeddings(d.page_content)
        data={"Text":d.page_content,"embeddings":embedding}
        vector_data.append(data)
    mc.insert(vector_data)
    print("Data inserted successfully")

# insert_embeddings(mc)

