from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.agents.strategies.selection.selection_strategy import SelectionStrategy
from semantic_kernel.contents import ChatMessageContent

class CustomSelectionStrategy(SelectionStrategy):
    """Custom selection strategy for choosing the next agent to respond."""

    def __init__(self):
        """Initialize the custom selection strategy."""
        super().__init__()

    async def select_next_agent(
        self, agents: List[Agent], messages: List[ChatMessageContent]
    ) -> Agent:
        """Select the next agent to respond.

        Args:
            agents: List of available agents
            messages: List of messages in the conversation

        Returns:
            The selected agent
        """
        # Simple round-robin selection
        if not messages:
            return agents[0]
        
        last_agent_name = messages[-1].name
        current_index = next(
            (i for i, agent in enumerate(agents) if agent.name == last_agent_name), 0
        )
        next_index = (current_index + 1) % len(agents)
        return agents[next_index] 