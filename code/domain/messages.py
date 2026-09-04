from dataclasses import dataclass,field
from enum import Enum
from typing import Any


class MessageType(Enum):
    TEXT="text"
    OBJECT="object"
# x=MessageType.TEXT
# print(x.value)
# print(type(x.value))
#里面的TEXT和OBJECT都是分别一个MessageType单例对象
@dataclass
class MessageObject:
    type:str
    id:str
    title:str|None=None
    attributes:dict=field(default_factory=dict)
    @classmethod
    def from_dict(cls,data:dict[str,Any])->"MessageObject":
        return cls(
            type=data["type"],
            id=data["id"],
            title=data["title"],
            attributes=data["attributes"]
        )
    def to_dict(self)->dict[str,Any]:
        return {
            "type":self.type,
            "id":self.id,
            "title":self.title,
            "attributes":self.attributes
        }
    #前面的schemas里面的这个属性不用加，因为pydantic里面的basemodel
    #会自动弄为dict，这里的话不是pydantic里的，所以要加一个field

#attributes:dict={} 不允许使用可变的字典类型，因为这个字典最底层
#当弄了一个实例对象的时候，底层会创建一个公共的空字典，这个对象里面attributes里面只是
#保存的字典的地址，然后当又创建了一个对象的时候，这个新的对象里的attributes属性里面的也是
#一个字典的地址，这个地址和刚刚那个地址不一样，但是指向的字典是一样的，所以
#当一个对象将字典里面的内容改变的时候，另外一个对象里面的字典的内容相应的也会改变
#因为他们地址指向的字典一样，我们显然不希望这样做，所以我们就要用一下field方法，当
#每一个对象创建的时候，那么里面的字典也就会创建一个新的，不会同时指向同一个字典
@dataclass
class UserMessage:
    sender_id:str
    message_id:str
    type:MessageType
    text:str|None=None
    object:MessageObject|None=None
    @classmethod
    def from_dict(cls,data:dict[str,Any])->"UserMessage":
        return cls(
            sender_id=data["sender_id"],
            message_id=data["message_id"],
            type=MessageType(value=data["type"]),
            text=data["text"],
            object=MessageObject.from_dict(data["object"])  if data["object"] else None
        )
    def to_dict(self)->dict[str,Any]:
        return {
            "sender_id":self.sender_id,
            "message_id":self.message_id,
            "type":self.type.value,
            "text":self.text,
            "object":self.object.to_dict() if self.object else None
        }
# usermessage=UserMessage("11","uu",type=MessageType.TEXT,text="")
@dataclass
class ProcessedMessage:
    text:str|None=None
    object:MessageObject|None=None
    @classmethod
    def from_dict(cls,data:dict[str,Any])->"ProcessedMessage":
        return cls(
            text=data["text"],
            object=MessageObject.from_dict(data["object"]) if data["object"] else None
        )
    def to_dict(self)->dict[str,Any]:
        return {
            "text":self.text,
            "object":self.object.to_dict() if self.object else None
        }
@dataclass
class ProcessResult:
    sender_id:str
    message_id:str
    messages:list[ProcessedMessage]