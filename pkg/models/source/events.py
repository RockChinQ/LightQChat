"""通用的事件类型"""
from ..content.elements import Element


class Event:
    type: str


class MessageReceivedEvent(Event):
    """消息接收事件"""
    type = "MessageReceivedEvent"

    source_id: str
    """来源id"""

    sender_id: str
    """发送者id"""

    message_id: str
    """消息id"""

    messages: list[Element]
    """消息内容"""

    def __init__(self, **kwargs):
        # 将参数都设置到实例上
        for k, v in kwargs.items():
            setattr(self, k, v)


class PrivateMessageReceivedEvent(MessageReceivedEvent):
    """私聊消息接收事件"""
    type = "PrivateMessageReceivedEvent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GroupMessageReceivedEvent(MessageReceivedEvent):
    """群聊消息接收事件"""
    type = "GroupMessageReceivedEvent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
