"""消息来源适配器"""
from ..content.elements import Element
from .events import Event, MessageReceivedEvent, PrivateMessageReceivedEvent, GroupMessageReceivedEvent

import typing


class MessageSourceAdapter:
    """消息来源适配器"""

    def __init__(self) -> None:
        pass

    async def send_msg(
        self,
        target_type: str,
        target_id: str,
        messages: list[Element]
    ):
        """发送消息"""
        pass

    async def login(self):
        pass

    async def reply_msg(
        self,
        message_received_event: MessageReceivedEvent,
        messages: list[Element],
        quote_origin: bool = False
    ):
        """回复消息"""
        pass

    async def register_event_handler(
        self,
        event_type: Event, 
        handler: typing.Callable[[Event], None]
    ):
        """注册事件处理器"""
        pass

    async def unregister_event_handler(
        self, 
        event_type: Event, 
        handler: typing.Callable[[Event], None]
    ):
        """注销事件处理器"""
        pass

    async def run(self):
        """运行"""
        pass

    async def close(self):
        """关闭"""
        pass