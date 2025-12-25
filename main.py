import os
import discord
from discord.ext import commands
import json
import requests
from openai import OpenAI
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models


api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.bltcy.ai/v1")


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
    response = client.chat.completions.create(
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

    response = requests.get(url=url, headers=headers)

    json_image = json.loads(response.content)
    url_image = json_image["imgurl"]
    await ctx.send(url_image)


@bot.hybrid_command()
async def translate(ctx, source: str, target: str, phrase: str):
    await ctx.defer()
    cred = credential.Credential(secret_id=secretld, secret_key=secretkey)
    client = tmt_client.TmtClient(cred, "ap-beijing")

    req = models.TextTranslateRequest()
    req.SourceText = phrase
    req.Source = source
    req.Target = target
    req.ProjectId = 0

    resp = client.TextTranslate(req)
    data = json.loads(resp.to_json_string())
    result = data["TargetText"]

    await ctx.send(result)


@bot.hybrid_command()
async def weather(ctx, city: str):
    await ctx.defer()

    geo = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
        params={"q": city, "limit": 1, "appid": API_KEY},
    ).json()

    lat = geo[0]["lat"]
    lon = geo[0]["lon"]

    req = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "lang": "zh_cn",
        },
    ).json()

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
