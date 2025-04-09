from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.agents.selection_strategy import SelectionStrategy
from semantic_kernel.contents import ChatMessageContent

class CustomSelectionStrategy(SelectionStrategy):
    def __init__(self):
        super().__init__()

    async def select_next_agent(
        self,
        agents: List[Agent],
        chat_history: List[ChatMessageContent],
    ) -> Agent:
        # Nếu chưa có message nào, chọn TerraformCreationAgent đầu tiên
        if not chat_history:
            return next(agent for agent in agents if agent.name == "TerraformCreationAgent")
        
        # Lấy message cuối cùng
        last_message = chat_history[-1]
        
        # Nếu message cuối cùng là từ TerraformCreationAgent, chọn TerraformValidationAgent
        if last_message.name == "TerraformCreationAgent":
            return next(agent for agent in agents if agent.name == "TerraformValidationAgent")
        
        # Nếu message cuối cùng là từ TerraformValidationAgent, chọn UserAgent
        if last_message.name == "TerraformValidationAgent":
            return next(agent for agent in agents if agent.name == "UserAgent")
        
        # Nếu message cuối cùng là từ UserAgent, chọn TerraformCreationAgent
        if last_message.name == "UserAgent":
            return next(agent for agent in agents if agent.name == "TerraformCreationAgent")
        
        # Mặc định chọn TerraformCreationAgent
        return next(agent for agent in agents if agent.name == "TerraformCreationAgent") 