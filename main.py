import os
import discord
from discord.ext import commands

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
    response= await client.chat.completions.create(
         model="gpt-4o",
         messages=[
             {"role":"user","content":question}
         ]
    )

    answer=response.choices[0].message.content
    await ctx.send(answer)


bot.run(token)    
    



