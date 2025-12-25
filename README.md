# 一个简单的Discord机器人

## ✨功能特点
 - ✅ **AI问答** - 接入了**chatgpt**
 - ✅ **天气询问** - 使用OpenWeather的api
 - ✅ **随机图片** - 第三方api
 - ✅ **简单翻译** - tencent翻译api
 - ✅ **斜杠命令** - 支持支持 Hybrid Commands（同步后可在 Discord 直接输入 `/` 使用）

## 📦安装依赖
> pip
```bash
pip install openai discord.py aiohttp tencentcloud-sdk-python
```
> uv
```bash
uv add openai discord.py aiohttp tencentcloud-sdk-python
```

## 🚀快速开始
1. 在 **.env** 文件中配置你的 **DISCORD_BOT_TOKEN** ,**OPENAI_API_KEY** **Secretld**和**SecretKey**

2. 运行脚本(推荐uv)
>uv
```bash
uv run main.py
```

## 🚧改进点
- 未使用**Cogs**等架构封装,代码可维护性差
- 未做错误处理,安全性不高
