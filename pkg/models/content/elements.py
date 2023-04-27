"""内容生成器返回的内容组件元素"""

from typing import List, Optional


class Element:
    type: str

    def __init__(self, **kwargs):
        # 将参数都设置到实例上
        for k, v in kwargs.items():
            setattr(self, k, v)


class TextElement(Element):
    """文本元素"""
    type: str = "text"
    text: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ImageElement(Element):
    """图片元素"""
    type: str = "image"
    url: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AudioElement(Element):
    """音频元素"""
    type: str = "audio"
    url: str
    

class AtElement(Element):
    """At元素"""
    type: str = "at"
    target: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
