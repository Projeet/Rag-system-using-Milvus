import sys
sys.path.append("../")

import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from chunking.chunking import create_connection,create_collection
from nvidia_llm.large_language_model import get_llm_embeddings

import warnings
warnings.filterwarnings("ignore")

CLUSTER_ENDPOINT=os.getenv("CLUSTER_ENDPOINT")
TOKEN=os.getenv("TOKEN")

collection_name="chatbot_collection"
dimension=1024
create_connection(CLUSTER_ENDPOINT, TOKEN)

mc=create_collection(collection_name,dimension)

def fetch_query_result(query):
    query=get_llm_embeddings(query)
    results = mc.search(
    data=[query],
    anns_field="embeddings",
    output_fields=["disclosure_id","Text"], #optional return fields
    limit=5,
    param={}, #no params if using milvus defaults
    )
    df=pd.DataFrame(columns=["Text","Disclosure ID"])
    for r in results[0]:
        # print(r.distance)
        # print(r.entity.get('Text'),r.entity.get('disclosure_id'))
        df.loc[len(df.index)]=[r.entity.get('Text'),r.entity.get('disclosure_id')]
    return df.iloc[0,0]

# res=fetch_query_result("AT&T date")
# print(res)














