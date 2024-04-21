from nvidia_llm import chat_model
from search_vectordb import search


# human_msg="Tell me a joke on AI"

# response=chat_model.get_bot_response(human_msg)

# print(response)

query="How much BOA invests in property ?"

result=search.fetch_query_result(query)

print(result)