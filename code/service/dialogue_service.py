from code.domain.messages import *
from code.engine.dialogue_engine import DialogueEngine
from code.repository.dialogue_state_repository import DialogueStateRepository
from code.domain.state import *

class DialogueService:
    def __init__(self,dialogue_state_repository:DialogueStateRepository,
                 dialogue_engine:DialogueEngine,
                 ):
        self.dialogue_state_repository=dialogue_state_repository
        self.dialogue_engine=dialogue_engine
    async def process_message(self,user_message:UserMessage)->ProcessResult:
        #在repository中加载state
        state:DialogueState=await self.dialogue_state_repository.load_state(user_message.sender_id)
        #在engine中处理state和新的消息
        process_result:ProcessResult=await self.dialogue_engine.process_state_message(state,user_message)
        #保存新的state
        await self.dialogue_state_repository.save_state(state)
        #返回结果
        return process_result