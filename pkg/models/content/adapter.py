"""内容生成器适配器"""
from .elements import Element


class ContentGeneratorAdapter:
    """内容生成器适配器"""

    def __init__(self, **kwargs):
        pass

    async def generate(self, **kwargs) -> list[Element]:
        """生成内容"""
        pass

    async def reset(self):
        """重置"""
        pass