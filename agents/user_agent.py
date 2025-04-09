import sys
from typing import TYPE_CHECKING, Any, Callable, Awaitable, AsyncIterable

if sys.version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.functions import KernelArguments

from .custom_agent_base import CustomAgentBase, Services
from ..plugins.user_plugin import UserPlugin

if TYPE_CHECKING:
    from semantic_kernel.agents import AgentResponseItem, AgentThread
    from semantic_kernel.kernel import Kernel

INSTRUCTION = """You are a user interaction expert responsible for gathering feedback and requirements.
Your tasks include:
1. Asking questions to clarify user requirements
2. Providing feedback on generated Terraform configurations
3. Requesting changes or improvements
4. Ensuring configurations meet user needs
5. Validating final configurations

You have access to the following plugin functions:
- user.request_user_feedback: Request feedback from the user

Always ensure:
- Questions are clear and specific
- Feedback is constructive
- Requirements are well-understood
- Changes are properly documented
- User needs are met"""

DESCRIPTION = """Select me to interact with the user and gather feedback."""


class UserAgent(CustomAgentBase):
    def __init__(self):
        super().__init__(
            service=self._create_ai_service(Services.OPENAI),
            plugins=[UserPlugin()],
            name="UserAgent",
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
            additional_user_message="Now interact with the user and gather feedback.",
            **kwargs,
        ):
            yield response 