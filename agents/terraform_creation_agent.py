from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.contents import ChatMessageContent, ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.author_role import AuthorRole

class TerraformCreationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TerraformCreationAgent",
            description="Agent responsible for creating and managing Terraform configuration",
        )
        self._system_message = ChatMessageContent(
            role=AuthorRole.SYSTEM,
            content="""You are a Terraform expert responsible for creating high-quality Terraform configurations.
Your tasks include:
1. Creating Terraform files with proper syntax and structure
2. Following Terraform best practices
3. Adding comprehensive comments
4. Using variables and locals for code reuse
5. Implementing security best practices

You have access to the following Terraform plugin functions:
- terraform_file.create_file: Create a new Terraform file
- terraform_file.read_file: Read an existing Terraform file
- terraform_file.list_files: List all Terraform files
- terraform_execution.validate: Validate Terraform configuration
- terraform_execution.fmt: Format Terraform files

Always ensure your configurations are secure, maintainable, and follow infrastructure as code best practices."""
        )

    async def invoke(self, history: ChatHistory) -> ChatMessageContent:
        system_message = self._system_message

        messages = [system_message] + history.messages
        response = await self._chat_completion_service.get_chat_message_contents(
            messages=messages,
            temperature=0.7,
            top_p=0.8,
        )

        # After getting the response, create the Terraform file
        if self._kernel:
            terraform_file_plugin = self._kernel.get_plugin("terraform_file")
            await terraform_file_plugin.create_file(
                filename="main.tf",
                content=response[0].content
            )

        return response[0] 