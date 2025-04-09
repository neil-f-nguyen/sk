from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.contents import ChatMessageContent, ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.author_role import AuthorRole

class TerraformValidationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TerraformValidationAgent",
            description="Agent responsible for validating Terraform configuration",
        )
        self._system_message = ChatMessageContent(
            role=AuthorRole.SYSTEM,
            content="""You are a Terraform validation expert responsible for ensuring the quality and correctness of Terraform configurations.
Your tasks include:
1. Validating Terraform syntax and structure
2. Checking for best practices compliance
3. Ensuring all necessary components are present
4. Verifying security configurations
5. Checking for potential issues

You have access to the following Terraform plugin functions:
- terraform_file.read_file: Read Terraform files
- terraform_execution.validate: Validate Terraform configuration
- terraform_execution.fmt: Format Terraform files

Always provide detailed feedback and suggestions for improvement."""
        )

    async def invoke(self, history: ChatHistory) -> ChatMessageContent:
        system_message = self._system_message

        messages = [system_message] + history.messages
        response = await self._chat_completion_service.get_chat_message_contents(
            messages=messages,
            temperature=0.7,
            top_p=0.8,
        )

        # After getting the response, validate the Terraform file
        if self._kernel:
            terraform_execution_plugin = self._kernel.get_plugin("terraform_execution")
            validation_result = await terraform_execution_plugin.validate("main.tf")
            if "success" not in validation_result.lower():
                response[0].content += f"\n\nValidation Result: {validation_result}"

        return response[0] 