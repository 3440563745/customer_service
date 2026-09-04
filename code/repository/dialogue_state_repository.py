import json
import asyncio

from code.domain.contexts import TaskContext
from code.domain.state import DialogueState
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from code.models.dialogue_state import DialogueStateRecord
from code.infrastructure import database

class DialogueStateRepository:
    def __init__(self,session:AsyncSession):
        self.session=session
    async def load_state(self, sender_id:str)->DialogueState:
        #从数据库中查对应的state数据
        sql=select(DialogueStateRecord).where(DialogueStateRecord.sender_id==sender_id)
        result=await self.session.execute(sql)
        row=result.fetchone()
        if row:
            state=row[0]
            dialogue_state:DialogueState=DialogueState.from_dict(json.loads(state.state_json))
            return dialogue_state
        else:
            return DialogueState(sender_id=sender_id)

    async def save_state(self, state:DialogueState):

        state_json:str=json.dumps(state.to_dict())
        insert_stmt=insert(DialogueStateRecord).values(
            sender_id=state.sender_id,state_json=state_json
        )
        upsert_stmt=insert_stmt.on_duplicate_key_update(
            state_json=insert_stmt.inserted.state_json
        )
        await self.session.execute(upsert_stmt)
        await self.session.commit()
if __name__=="__main__":
    async def main():
        database.create_db_engine()
        async with database.session_factory() as session:
            repo=DialogueStateRepository(session)
            # state=DialogueState(
            #     sender_id="test_sender",
            #     active_task=TaskContext(
            #         flow_id="flow_1",
            #         step_id="step_1",
            #         slots={"oder_id":"order_1"}
            #     )
            # )
            state=await repo.load_state(sender_id="test_sender")

            print(state)
        await database.close_db_engine()
    asyncio.run(main())
