
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore")

api_key=os.getenv("NVIDIA_API_KEY")
def get_llm_embeddings(input):

    invoke_url = "https://ai.api.nvidia.com/v1/retrieval/nvidia/embeddings"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    payload = {
    "input": input,
    "input_type": "query",
    "model": "NV-Embed-QA"
    }
    session = requests.Session()
    response = session.post(invoke_url, headers=headers, json=payload)

    response.raise_for_status()
    response_body = response.json()

    return response_body['data'][0]['embedding']



# emb=get_llm_embeddings("What is the GPU memory bandwidth of H100 SXM?")
# print(emb)