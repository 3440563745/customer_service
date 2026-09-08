from code.domain.messages import MessageType, MessageObject, UserMessage
from code.domain.state import Turn


class HistoryBuilder:
    @staticmethod
    def build(turns:list[Turn])->str:
        messages:list[str]=[]
        for turn in turns:
            user_message=turn.user_message
            if user_message.type ==MessageType.TEXT:
                messages.append(f"USER: {user_message.text.strip()}")
            else:
                messages_object=HistoryBuilder._render_object_message(user_message.object)
                messages.append(f"USER: {messages_object}")
            processed_messages=turn.ProcessedMessages
            for processed_message in processed_messages:
                if processed_message.text:
                    messages.append(f"BOT: {processed_message.text.strip()}")
                else:
                    messages_object_from_bot=HistoryBuilder._render_object_message(processed_message.object)
                    messages.append(f"BOT: {messages_object_from_bot}")
        return "\n".join(messages)
    @staticmethod
    def _render_object_message(object:MessageObject|None)->str:
        #返回类型为str[类型名称，id=aaa，title=dd，key1=value1 ]
        label="订单类型" if object.type =="order" else "商品类型"
        id=object.id
        title=object.title
        attributes=object.attributes
        attributes_list=[f"{key}={value}" for key,value in attributes.items()]
        str1=",".join(attributes_list)
        return f"[{label},id={id},title={title}],{str1}"
    @staticmethod
    def _render_object_and_normal_message(user_message:UserMessage):
        if user_message.type ==MessageType.TEXT:
            return user_message.text.strip()
        else:
            HistoryBuilder._render_object_message(user_message.object)