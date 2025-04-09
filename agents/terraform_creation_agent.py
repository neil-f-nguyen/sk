import sys
from typing import TYPE_CHECKING, Any, Callable, Awaitable, AsyncIterable

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from semantic_kernel.agents import Agent
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions import KernelArguments

from .custom_agent_base import CustomAgentBase, Services
from ..plugins.terraform_file_plugin import TerraformFilePlugin
from ..plugins.terraform_execution_plugin import TerraformExecutionPlugin

if TYPE_CHECKING:
    from semantic_kernel.agents import AgentResponseItem, AgentThread
    from semantic_kernel.kernel import Kernel

INSTRUCTION = """You are a Terraform expert responsible for creating high-quality Terraform configurations.
Your tasks include:
1. Creating Terraform files based on user requirements
2. Using best practices for Terraform configuration
3. Adding comprehensive comments
4. Using variables and locals for code reuse
5. Implementing security best practices

You have access to the following Terraform plugin functions:
- terraform_file.create_file: Create a new Terraform file
- terraform_file.read_file: Read an existing Terraform file
- terraform_file.list_files: List all Terraform files
- terraform_execution.validate: Validate Terraform configuration
- terraform_execution.fmt: Format Terraform files

Always ensure your configurations are:
- Well-documented
- Follow best practices
- Secure
- Reusable
- Maintainable"""

DESCRIPTION = """Select me to create or update Terraform configurations."""


class TerraformCreationAgent(CustomAgentBase):
    """Agent responsible for creating Terraform configurations."""

    def __init__(self):
        """Initialize the Terraform creation agent."""
        super().__init__(
            service=self._create_ai_service(Services.OPENAI),
            plugins=[TerraformFilePlugin(), TerraformExecutionPlugin()],
            name="TerraformCreationAgent",
            instructions=INSTRUCTION.strip(),
            description=DESCRIPTION.strip(),
        )

    @override
    async def invoke(
        self,
        *,
        messages: str | ChatMessageContent | list[str | ChatMessageContent] | None = None,
        thread: "AgentThread | None" = None,
        on_intermediate_message: Callable[[ChatMessageContent], Awaitable[None]] | None = None,
        arguments: KernelArguments | None = None,
        kernel: "Kernel | None" = None,
        **kwargs: Any,
    ) -> AsyncIterable["AgentResponseItem[ChatMessageContent]"]:
        """Invoke the agent.

        Args:
            messages: List of messages in the conversation
            thread: Optional agent thread
            on_intermediate_message: Optional callback for intermediate messages
            arguments: Optional kernel arguments
            kernel: Optional kernel
            **kwargs: Additional keyword arguments

        Yields:
            Stream of agent responses
        """
        async for response in super().invoke(
            messages=messages,
            thread=thread,
            on_intermediate_message=on_intermediate_message,
            arguments=arguments,
            kernel=kernel,
            additional_user_message="Now create or update Terraform configurations based on the requirements.",
            **kwargs,
        ):
            yield response 