from code.domain.messages import UserMessage, ProcessResult
from code.domain.state import DialogueState


class DialogueEngine:
    async def process_state_message(self, state:DialogueState, user_message:UserMessage)->ProcessResult:
        pass