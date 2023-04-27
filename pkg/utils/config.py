
import os
import shutil
import logging

import yaml
import json

from .singleton import Singleton


@Singleton
class Config:
    """配置文件宿主"""

    _file_path: str

    _config: dict

    def __init__(self, file_path: str, template_file_path: str):
        if not os.path.exists(file_path):
            # 如果配置文件不存在，则从模板文件中复制一份
            shutil.copy(template_file_path, file_path)
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