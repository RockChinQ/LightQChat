# Light QQ ChatGPT

轻量级、全异步的ChatGPT QQ机器人

- 基于[wyapx/CAI](https://github.com/wyapx/CAI)连接QQ，无需配置mirai/go-cqhttp等框架的连接

## 功能点

- 无需额外使用mirai/go-cqhttp等框架，直接使用QQ号登录
- 支持通过QQ与ChatGPT网页版文字对话
- 支持连续对话，回复符合前文

## 部署

### 要求

- Python 3.9+
- 已安装Git

### 安装

获取源码

```bash
git clone https://github.com/RockChinQ/LightQChat
cd LightQChat
```

安装依赖

```bash
pip install -r requirements.txt
```

启动一次生成配置文件

```bash
python main.py
```

### 配置

请根据`config.yaml`中的注释进行配置，完成后执行`python main.py`即可启动  
若是第一次登录，请根据提示进行QQ号登录

## 使用

直接跟机器人说话就行了

## 关于..

- 这是一个关于CAI框架、YAML配置文件、异步编程的概念验证项目
- 需要更多更丰富的功能可以查看[QChatGPT](https://github.com/RockChinQ/QChatGPT)
- 有任何问题请提issue