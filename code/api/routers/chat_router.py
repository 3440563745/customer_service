import uuid

from fastapi import APIRouter,Depends

from code.api.dependencies import get_dialogue_service
from code.service.dialogue_service import *
from code.api.schemas import ChatRequest,ChatResponse,HistoryResponse
from code.api.schemas import *
chat_router=APIRouter()





def _transfer_ChatRequest2_UserMessage(chat_request:ChatRequest)->UserMessage:
    return UserMessage(
        sender_id=chat_request.sender_id,
        message_id=chat_request.message_id if chat_request.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT if chat_request.text else MessageType.OBJECT,
        text=chat_request.text,
        object=MessageObject(
            type=chat_request.object.type,
            id=chat_request.object.id,
            title=chat_request.object.title,
            attributes=chat_request.object.attributes,
        ) if chat_request.object else None,
    )


def _transfer_ProcessResult2_ChatResponse(process_result:ProcessResult)->ChatResponse:
    return ChatResponse(
           sender_id=process_result.sender_id,
           message_id=process_result.message_id,
           messages=[ChatBot_Message(
               text=process_message.text,
               object=ChatObject(
                 type=process_message.object.type,
                 id=process_message.object.id,
                 title=process_message.object.title,
                 attributes=process_message.object.attributes
               )  if process_message.object else None,
           ) for process_message in process_result.messages],
    )


@chat_router.post("/api/chat")
async def chat(chat_request:ChatRequest,
               dialogue_service:DialogueService=Depends(get_dialogue_service)#按照规范，在dependencies里面写函数
               )->ChatResponse:
    user_message=_transfer_ChatRequest2_UserMessage(chat_request)
    process_result=await dialogue_service.process_message(user_message)
    return _transfer_ProcessResult2_ChatResponse(process_result)
    # return ChatResponse(
    #     sender_id=chat_request.sender_id,
    #     message_id=str(uuid.uuid4()),
    #     messages=[ChatBot_Message(
    #         text="我不知道"
    #     )]
    # )
#host:0.0.0.0和127.0.0.1的区别：每一个电脑有好几个网卡，每一个网卡都可以链接网络，比如a网卡和b网卡
#当a和b都分别链接到一个网络后，每一个网卡都会被对应网络分配一个对应的ip地址，如果host填的是a的地址，那么久就只可以
#链接到a网路，如果填的b地址，那么只可以链接到b网络，如果地址填的127.0.0.0那么a和b都不可以访问到，
#是本地回环网络，只可以在本地的浏览器中访问服务，那么如果填的0.0.0.0，主机，a，b都可以访问，某一个
#软件服务，监听到某一个ip后，只可以监听该网卡的网络请求
# 电脑有 a 网卡（IP: 192.168.1.5）和 b 网卡（IP: 10.0.0.2）。
# 如果 Web 服务绑定到 192.168.1.5：只能从 a 网卡所在的网络 访问。
# 如果绑定到 10.0.0.2：只能从 b 网卡所在的网络 访问。
# 如果绑定到 127.0.0.1：a 和 b 都无法访问，只能本机浏览器访问。
# 如果绑定到 0.0.0.0：a 和 b 都能访问（包括本机和其他网卡）。
#也就是在浏览器中输入http:127.0.0.1以及http:192.168.1.5，http:10.0.0.2都可以访问到服务，因为都监听了的
#拿如果是绑定127.1那个，那么浏览器就只可以输入那一个地址访问
@chat_router.get("/api/chat/history")
async def history(sender_id:str)->HistoryResponse:
    return HistoryResponse(
        sender_id=sender_id,
        messages=[
            HistoryObject(
                role="user",
                text="你好"
            ),
            HistoryObject(
                role="bot",
                text="我不好"
            )
        ]
    )