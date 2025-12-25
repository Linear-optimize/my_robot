import os
import discord
from discord.ext import commands
import json
import aiohttp
from openai import AsyncOpenAI
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models


api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=api_key, base_url="https://api.bltcy.ai/v1")


token = os.getenv("DISCORD_BOT_TOKEN")

secretld = os.getenv("Secretld")
secretkey = os.getenv("SecretKey")

API_KEY = os.getenv("OPENWEATHER_API_KEY")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
@commands.has_permissions(administrator=True)
async def synccommands(ctx):
    await bot.tree.sync()
    await ctx.send("同步成功")


@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("pong")


@bot.hybrid_command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)


@bot.hybrid_command()
async def ask(ctx, question: str):
    await ctx.defer()
    response = await client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": question}]
    )

    answer = response.choices[0].message.content
    await ctx.send(answer)


@bot.hybrid_command()
async def draw(ctx):
    await ctx.defer()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }

    url = "https://www.98qy.com/sjbz/api.php?lx=dongman&format=json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            data = await response.json(content_type=None)

    url_image = data["imgurl"]

    embed = discord.Embed()
    embed.set_image(url=url_image)
    await ctx.send(embed=embed)


@bot.hybrid_command()
async def translate(ctx, source: str, target: str, phrase: str):
    await ctx.defer()

    cred = credential.Credential(secret_id=secretld, secret_key=secretkey)
    client_tencent = tmt_client.TmtClient(cred, "ap-beijing")

    req = models.TextTranslateRequest()
    req.SourceText = phrase
    req.Source = source
    req.Target = target
    req.ProjectId = 0

    resp = client_tencent.TextTranslate(req)
    data = json.loads(resp.to_json_string())
    result = data["TargetText"]

    await ctx.send(result)


@bot.hybrid_command()
async def weather(ctx, city: str):
    await ctx.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={"q": city, "limit": 1, "appid": API_KEY},
        ) as req:
            geo = await req.json()

    lat = geo[0]["lat"]
    lon = geo[0]["lon"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "zh_cn",
            },
        ) as reqs:
            req = await reqs.json()

    city_name = req["name"]
    desc = req["weather"][0]["description"]
    temp = req["main"]["temp"]
    humidity = req["main"]["humidity"]
    wind_speed = req["wind"]["speed"]

    embed = discord.Embed(
        title=f"🌤 {city_name} 当前天气",
        description=desc,
        color=0x4FC3F7,
    )

    embed.add_field(name="🌡 温度", value=f"{temp} °C", inline=True)
    embed.add_field(name="💧 湿度", value=f"{humidity} %", inline=True)
    embed.add_field(name="🌬 风速", value=f"{wind_speed} m/s", inline=True)

    embed.set_footer(text="数据来源：OpenWeatherMap")

    await ctx.send(embed=embed)


bot.run(token)
