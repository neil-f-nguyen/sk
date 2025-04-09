from typing import List

from semantic_kernel.agents import Agent
from semantic_kernel.agents.termination_strategy import TerminationStrategy
from semantic_kernel.contents import ChatMessageContent

class CustomTerminationStrategy(TerminationStrategy):
    def __init__(self, agents: List[Agent]):
        super().__init__()
        self.agents = agents

    async def should_terminate(
        self,
        chat_history: List[ChatMessageContent],
    ) -> bool:
        # Cần ít nhất 3 messages để bắt đầu kiểm tra
        if len(chat_history) < 3:
            return False
        
        # Lấy 3 messages cuối cùng
        last_three_messages = chat_history[-3:]
        
        # Kiểm tra nếu có một chu kỳ hoàn chỉnh (Creation -> Validation -> User)
        if (
            last_three_messages[0].name == "TerraformCreationAgent"
            and last_three_messages[1].name == "TerraformValidationAgent"
            and last_three_messages[2].name == "UserAgent"
        ):
            # Nếu UserAgent không yêu cầu thay đổi, kết thúc
            user_feedback = last_three_messages[2].content.lower()
            if "thay đổi" not in user_feedback and "sửa" not in user_feedback:
                return True
        
        # Nếu có quá nhiều chu kỳ (ví dụ: 5 chu kỳ), kết thúc
        if len(chat_history) >= 15:  # 5 chu kỳ * 3 messages
            return True
        
        return False 