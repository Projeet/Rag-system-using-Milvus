# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from nvidia_llm import chat_model
from search_vectordb import search
import warnings
warnings.filterwarnings("ignore")

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        human_msg=turn_context.activity.text
        context=search.fetch_query_result(human_msg)

        new_query = f"""
                    User: {human_msg}

                    Context: {context}

                    please generate a response to the user's question based on the provided context. If the context is not relevant to the question, respond with "I do not have enough context to answer your question.

                    """
                    
        response=chat_model.get_bot_response(new_query)
        await turn_context.send_activity(f"{response}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
