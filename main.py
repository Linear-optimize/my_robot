import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.api_key = os.getenv("OPENAI_API_KEY")
bot.secretld = os.getenv("secretld")
bot.secretkey = os.getenv("secretkey")
bot.API_KEY = os.getenv("API_KEY")

token = os.getenv("DISCORD_BOT_TOKEN")


@bot.command()
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send("同步成功")


async def load_cogs():
    cogs = ["cogs.fun", "cogs.ai", "cogs.translate", "cogs.weather"]
    for cog in cogs:
        await bot.load_extension(cog)


@bot.event
async def on_ready():
    if not hasattr(bot, "http_session"):
        bot.http_session = aiohttp.ClientSession()
    await load_cogs()
    for guild in bot.guilds:  # 如果你只想同步到某个服务器
        await bot.tree.sync(guild=guild)
    print(f"{bot.user} 已上线！")


if __name__ == "__main__":
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("程序已手动停止")
