import os
import discord
from discord.ext import commands
import json
import requests
from openai import OpenAI



api_key=os.getenv('OPENAI_API_KEY')

client=OpenAI(
    api_key=api_key,
    base_url="https://api.bltcy.ai/v1"
)


token=os.getenv('DISCORD_BOT_TOKEN')

intents=discord.Intents.default()
intents.message_content= True

bot =commands.Bot(command_prefix="!",intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def synccomands(ctx):
    await bot.tree.sync()
    await ctx.send("同步成功")

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("pong")

@bot.hybrid_command()
async def add(ctx,a:int,b:int):
    await ctx.send(a+b)

@bot.hybrid_command()
async def ask(ctx,question:str):
    await ctx.defer()
    response=  client.chat.completions.create(
         model="gpt-4o",
         messages=[
             {"role":"user","content":question}
         ]
    )

    answer=response.choices[0].message.content
    await ctx.send(answer)

@bot.hybrid_command()
async def draw(ctx):
    await ctx.defer()

    headers={
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }

    url="https://www.98qy.com/sjbz/api.php?lx=dongman&format=json"

    response=requests.get(headers=headers,url=url)

    json_image=json.loads(response.content)
    url_image=json_image['imgurl']
    await ctx.send(url_image)


bot.run(token)    
    



