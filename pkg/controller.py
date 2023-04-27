from .utils.singleton import Singleton
from .utils.config import Config
from .models.source.adapter import MessageSourceAdapter
from .impls.source.caibot import CaibotSourceAdapter

import asyncio
import logging
import traceback

from .models.source.events import Event, MessageReceivedEvent, PrivateMessageReceivedEvent, GroupMessageReceivedEvent
from .session import get_session_by_name, Session
from .models.content.elements import Element, TextElement, AtElement


async def process(controller, event: MessageReceivedEvent, session_name: str, message: str):
    """处理消息"""
    reply_elements = []
    try:
        session: Session = get_session_by_name(session_name)
        reply_elements = await session.get_reply(message)
    except Exception as e:
        reply_elements = [
            TextElement(
                text = "出错了: {}".format(e)
            )
        ]
        traceback.print_exc()

    try:
        await controller._msg_source_adapter.reply_msg(
            event,
            reply_elements
        )
    except:
        traceback.print_exc()


async def private_message_received(event: MessageReceivedEvent):
    """私聊消息接收事件"""
    if not isinstance(event.messages[0], TextElement):
        return
    await process(
        controller=Controller(),
        event=event,
        session_name="person_{}".format(event.source_id),
        message=event.messages[0].text
    )


async def group_message_received(event: MessageReceivedEvent):
    """群聊消息接收事件"""
    # 判断是否被at
    has_at = False
    content = ""
    for ele in event.messages:
        if isinstance(ele, AtElement):
            print(ele.target, Config().cfg['source']['adapter']['account'])
            if ele.target == Config().cfg['source']['adapter']['account']:
                has_at = True
        elif isinstance(ele, TextElement):
            content += ele.text
    if not has_at:
        return
    await process(
        controller=Controller(),
        event=event,
        session_name="group_{}".format(event.source_id),
        message=content
    )

@Singleton
class Controller:
    """流程总控制器"""

    _msg_source_adapter: MessageSourceAdapter
    """消息来源适配器"""
    def __init__(self) -> None:
        pass
    
    async def run(self):
        """运行"""
        loop = asyncio.get_running_loop()
        self._msg_source_adapter = CaibotSourceAdapter()
        await self._msg_source_adapter.login()

        await self._msg_source_adapter.register_event_handler(
            GroupMessageReceivedEvent,
            group_message_received
        )

        # 注册事件处理函数
        await self._msg_source_adapter.register_event_handler(
            PrivateMessageReceivedEvent,
            private_message_received
        )

        try:
            await self._msg_source_adapter.run()
        except Exception:
            logging.info("程序退出")