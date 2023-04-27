from .models.content.adapter import ContentGeneratorAdapter
from .impls.content.revChatGPT import RevChatGPTAdapter

from .models.content.elements import Element


__sessions__ = {}


class Session:
    name: str
    """会话名称"""

    adapter: ContentGeneratorAdapter

    def __init__(self, name: str):
        self.name = name
        
        # 初始化适配器
        self.adapter = RevChatGPTAdapter()

    async def get_reply(self, prompt: str) -> list[Element]:
        """获取回复"""
        return await self.adapter.generate(prompt=prompt)

    async def reset(self):
        """重置"""
        await self.adapter.reset()


def get_session_by_name(name: str) -> Session:
    """根据名称获取会话"""
    global __sessions__
    if name not in __sessions__:
        __sessions__[name] = Session(name=name)
    return __sessions__[name]
