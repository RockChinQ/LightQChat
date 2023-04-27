
import os
import shutil
import logging

import yaml
import json

from .singleton import Singleton

template = """
source:
  adapter:
    # 目前仅支持CAI框架登录
    type: cai
    # 【必修改】QQ号
    account: 1234567890
    # 【必修改】QQ密码
    password: abc123456
    # 在以下几个协议中选择：ANDROID_PAD, ANDROID_PHONE, ANDROID_WATCH, IPAD, MACOS
    # 若当前协议登录失败，请删除bot/目录所有文件，到此更换协议后重启bot
    # 重复此操作直到登录成功
    protocol: ANDROID_PAD
content:
  adapter:
    # 目前仅支持使用ChatGPT逆向库
    type: revChatGPT
    # 【必修改】ChatGPT网页版的access_token
    # 在浏览器登录ChatGPT后访问https://chat.openai.com/api/auth/session
    # 复制ey开头的access_token到这里
    access_token: eyxxxxxxxxxxxxxxx
"""


@Singleton
class Config:
    """配置文件宿主"""

    _file_path: str

    _config: dict

    def __init__(self, file_path: str, template_file_path: str):
        if not os.path.exists(file_path):
            # 如果配置文件不存在，则从模板文件中复制一份
            # shutil.copy(template_file_path, file_path)
            
            # 将模板文件写入配置文件
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(template)
            raise FileNotFoundError("配置文件不存在，已从模板文件中复制一份，请修改配置文件{}后重试".format(file_path))
        self._file_path = file_path

        # 加载配置文件
        self._config = yaml.safe_load(open(file_path, "r", encoding="utf-8"))
        logging.debug(json.dumps(self._config, indent=4, ensure_ascii=False))

        # 把属性添加到实例上
        for k, v in self._config.items():
            setattr(self, k, v)

    @property
    def cfg(self):
        return self._config