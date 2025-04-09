import sys
from typing import TYPE_CHECKING, Any, Callable, Awaitable, AsyncIterable

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.functions import KernelArguments

from .custom_agent_base import CustomAgentBase, Services
from ..plugins.terraform_file_plugin import TerraformFilePlugin
from ..plugins.terraform_execution_plugin import TerraformExecutionPlugin

if TYPE_CHECKING:
    from semantic_kernel.agents import AgentResponseItem, AgentThread
    from semantic_kernel.kernel import Kernel

INSTRUCTION = """You are a Terraform expert responsible for validating Terraform configurations.
Your tasks include:
1. Checking Terraform syntax and structure
2. Validating resource configurations
3. Ensuring best practices are followed
4. Checking for security issues
5. Verifying variable usage

You have access to the following Terraform plugin functions:
- terraform_file.read_file: Read an existing Terraform file
- terraform_execution.validate: Validate Terraform configuration
- terraform_execution.fmt: Format Terraform files

Always ensure configurations are:
- Syntactically correct
- Follow best practices
- Secure
- Well-documented
- Properly formatted"""

DESCRIPTION = """Select me to validate Terraform configurations."""


class TerraformValidationAgent(CustomAgentBase):
    def __init__(self):
        super().__init__(
            service=self._create_ai_service(Services.OPENAI),
            plugins=[TerraformFilePlugin(), TerraformExecutionPlugin()],
            name="TerraformValidationAgent",
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
        async for response in super().invoke(
            messages=messages,
            thread=thread,
            on_intermediate_message=on_intermediate_message,
            arguments=arguments,
            kernel=kernel,
            additional_user_message="Now validate the Terraform configurations.",
            **kwargs,
        ):
            yield response 