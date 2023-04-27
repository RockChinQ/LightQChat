from revChatGPT.V1 import AsyncChatbot
from ...models.content.adapter import ContentGeneratorAdapter

from ...utils.report import report
from ...utils.config import Config
from ...models.content.elements import Element, TextElement

import logging


class RevChatGPTAdapter(ContentGeneratorAdapter):
    """RevChatGPT适配器"""
    chatbot: AsyncChatbot = None

    conversation_id = None
    def __init__(self, **kwargs):
        rev_cfg = Config().cfg['content']['adapter']
        if 'type' in rev_cfg:
            del rev_cfg['type']
        self.chatbot = AsyncChatbot(
            config=rev_cfg
        )

    async def generate(self, **kwargs) -> list[Element]:
        """生成内容"""
        res = {}
        async_generator = self.chatbot.ask(
                            prompt=kwargs['prompt'],
                            conversation_id=self.conversation_id,
                            auto_continue=True,
                        )
        async for resp in async_generator:
            res = resp
            logging.debug(res)
        self.conversation_id = res['conversation_id']
        report(len(res['message']))
        return [
            TextElement(
                text=res['message']
            )
        ]
    
    async def reset(self):
        """重置"""
        self.conversation_id = None

