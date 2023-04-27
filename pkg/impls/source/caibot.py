from ...models.source.adapter import MessageSourceAdapter
from ...models.source.events import Event, MessageReceivedEvent, PrivateMessageReceivedEvent, GroupMessageReceivedEvent
from ...utils.config import Config
from ...utils.singleton import Singleton

import typing
import asyncio

import cai
from cai.client import Event as caiEvent
from cai.settings.protocol import Protocols
from cai.contrib.login_resolver import LoginResolver
from cai.client.events.common import PrivateMessage as caiPrivateMessage, GroupMessage as caiGroupMessage

from ...models.content import elements as ele
from cai.client.message_service import models as caiele


def get_protocol(protocol: str):
    """获取协议"""
    _dict = {
        "ANDROID_PAD": Protocols.Android.PAD,
        "ANDROID_PHONE": Protocols.Android.PHONE,
        "ANDROID_WATCH": Protocols.Android.WATCH,
        "IPAD": Protocols.IPAD,
        "MACOS": Protocols.MACOS,
    }

    if protocol not in _dict:
        raise ValueError(f"不支持的协议, 请检查配置文件: {protocol}")
    
    return _dict[protocol]


def get_cai_messages(messages: list[ele.Element]) -> typing.Sequence[caiele.Element]:
    """将本程序的消息转换成CAI的消息"""
    if not messages:
        return []

    result = []
    for message in messages:
        if isinstance(message, ele.TextElement):
            result.append(
                caiele.TextElement(
                    content = message.text
                )
            )
        elif isinstance(message, ele.ImageElement):
            result.append(
                caiele.ImageElement(
                    url = message.url
                )
            )
    
    return result
    

def get_messages(messages: typing.Sequence[caiele.Element]) -> list[ele.Element]:
    """将CAI的消息转换成本程序的消息"""
    if not messages:
        return []

    result = []
    for message in messages:
        if isinstance(message, caiele.TextElement):
            element = ele.TextElement()
            element.text = message.content
            result.append(element)
        elif isinstance(message, caiele.ImageElement):
            element = ele.ImageElement()
            element.url = message.url
            result.append(element)
        elif isinstance(message, caiele.AtElement):
            element = ele.AtElement(target=message.target)
            result.append(element)

    return result


# cai事件到本程序事件的映射
event_mapping: dict[str, Event] = {
    "private_message": PrivateMessageReceivedEvent,
    "group_message": GroupMessageReceivedEvent,
}


def get_event(event: caiEvent) -> Event:
    """将cai事件对象转换成本程序事件对象"""
    if isinstance(event, caiPrivateMessage):
        return PrivateMessageReceivedEvent(
            source_id = event.from_uin,
            sender_id = event.from_uin,
            message_id = event.seq,
            messages = get_messages(event.message)
        )
    elif isinstance(event, caiGroupMessage):
        return GroupMessageReceivedEvent(
            source_id = event.group_id,
            sender_id = event.from_uin,
            message_id = event.seq,
            messages = get_messages(event.message)
        )
    

@Singleton
class CaibotSourceAdapter(MessageSourceAdapter):
    """CAI登录框架适配器"""
    __client: cai.Client
    handlers: dict[str, list[typing.Callable[[Event], None]]] = {}

    async def _event_handler(self, client: cai.Client, event: caiEvent):
        """事件处理器"""
        if event.type not in event_mapping:
            return
        
        if event_mapping[event.type].type not in self.handlers:
            return
        
        # 调用事件处理器
        converted_event = get_event(event)
        for handler in self.handlers[event_mapping[event.type].type]:
            await handler(converted_event)

    def __init__(self) -> None:
        source_cfg = Config().cfg['source']
        acc = source_cfg['adapter']['account']
        pwd = source_cfg['adapter']['password']
        protocol = get_protocol(source_cfg['adapter']['protocol'])
        self.__client = cai.Client(acc, pwd, protocol)
        self.__client.add_event_listener(self._event_handler)
        self.handlers = {}

    async def login(self):
        await LoginResolver(self.__client).login()

    async def send_msg(
        self,
        target_type: str,
        target_id: str,
        messages: list[ele.Element]
    ):
        """发送消息"""
        if target_type == "private":
            await self.__client.send_friend_msg(
                target_id,
                get_cai_messages(messages)
            )
        elif target_type == "group":
            await self.__client.send_group_msg(
                target_id,
                get_cai_messages(messages)
            )

    async def reply_msg(
        self,
        message_received_event: MessageReceivedEvent,
        messages: list[ele.Element],
        quote_origin: bool = False
    ):
        """回复消息"""
        if isinstance(message_received_event, PrivateMessageReceivedEvent):
            await self.send_msg(
                "private",
                message_received_event.source_id,
                messages
            )
        elif isinstance(message_received_event, GroupMessageReceivedEvent):
            await self.send_msg(
                "group",
                message_received_event.source_id,
                messages
            )
    
    async def register_event_handler(
        self,
        event_type: Event, 
        handler: typing.Callable[[Event], None]
    ):
        """注册事件处理器"""
        if not event_type.type in self.handlers:
            self.handlers[event_type.type] = []
        self.handlers[event_type.type].append(handler)

    async def unregister_event_handler(
        self, 
        event_type: Event, 
        handler: typing.Callable[[Event], None]
    ):
        """注销事件处理器"""
        self.handlers[event_type].remove(handler)

    async def run(self):
        """运行"""
        await self.__client.session.wait_closed()

    async def close(self):
        """关闭"""
        await self.__client.close()
