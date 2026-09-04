from pydantic import BaseModel
#这里pydantic会把前端给的json数据自动转化为python对象

class ChatObject(BaseModel):
    type:str
    id:str
    title:str|None=None
    attributes:dict={}

class ChatRequest(BaseModel):
    sender_id:str
    text:str|None=None
    message_id:str|None=None
    object:ChatObject|None=None
#这里的text，object都是二选一，要么是请求/回复 text要么object对象，比如商品对象
class ChatBot_Message(BaseModel):
    text:str|None=None
    object:ChatObject|None=None
class ChatResponse(BaseModel):
    sender_id:str
    message_id:str
    messages:list[ChatBot_Message]
class HistoryObject(BaseModel):
    role:str
    text:str|None=None
    object:ChatObject|None=None

class HistoryResponse(BaseModel):
    sender_id:str
    messages:list[HistoryObject]