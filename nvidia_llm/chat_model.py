
from dotenv import load_dotenv
load_dotenv()

## Core LC Chat Interface
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import HumanMessage, SystemMessage


import warnings
warnings.filterwarnings("ignore")

def get_list_models():
    models=ChatNVIDIA.get_available_models()
    return models

def get_llm(model):
    llm = ChatNVIDIA(model=model)
    return llm

def get_bot_response(human_message,model="mistral_7b"):
    messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(content=human_message),
    ]
    llm=get_llm(model)
    return llm.invoke(messages).content

# res=get_bot_response("Hello")
# print(res)



