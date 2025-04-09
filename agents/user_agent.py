from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.contents import ChatMessageContent, ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.author_role import AuthorRole

class UserAgent(Agent):
    def __init__(self):
        super().__init__(
            name="UserAgent",
            description="Agent representing the user in the Terraform configuration process",
        )
        self._system_message = ChatMessageContent(
            role=AuthorRole.SYSTEM,
            content="""You are a user interface agent responsible for interacting with the user.
Your tasks include:
1. Asking questions to clarify requirements
2. Providing feedback on generated Terraform configurations
3. Requesting changes or improvements
4. Ensuring the final configuration meets user needs

You have access to the following plugin functions:
- user.request_user_feedback: Get feedback from the user

Always be clear and specific in your communications."""
        )

    async def invoke(self, history: ChatHistory) -> ChatMessageContent:
        system_message = self._system_message

        messages = [system_message] + history.messages
        response = await self._chat_completion_service.get_chat_message_contents(
            messages=messages,
            temperature=0.7,
            top_p=0.8,
        )

        # Get user feedback if this is a validation response
        if self._kernel and "validation" in response[0].content.lower():
            user_plugin = self._kernel.get_plugin("user")
            user_feedback = await user_plugin.request_user_feedback(response[0].content)
            response[0].content += f"\n\nUser Feedback: {user_feedback}"

        return response[0] 