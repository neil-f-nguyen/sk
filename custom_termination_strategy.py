from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.contents import ChatMessageContent


class CustomTerminationStrategy(TerminationStrategy):
    """Custom termination strategy for determining when to end the conversation."""

    def __init__(self, agents: List[Agent]):
        """Initialize the custom termination strategy.

        Args:
            agents: List of agents in the conversation
        """
        super().__init__()
        self._agents = agents

    async def should_terminate(
        self, messages: List[ChatMessageContent]
    ) -> bool:
        """Determine if the conversation should terminate.

        Args:
            messages: List of messages in the conversation

        Returns:
            True if the conversation should terminate, False otherwise
        """
        if not messages:
            return False

        # Terminate if we've gone through all agents at least once
        if len(messages) >= len(self._agents):
            last_message = messages[-1]
            if last_message.name == self._agents[-1].name:
                return True

        return False 