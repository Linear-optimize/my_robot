import discord
from discord.ext import commands


class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="weather", description="询问天气")
    async def weather(self, ctx, city: str):
        await ctx.defer()
        session = self.bot.http_session

        async with session.get(
            "http://api.openweathermap.org/geo/1.0/direct",
            params={"q": city, "limit": 1, "appid": self.bot.API_KEY},
        ) as req:
            geo = await req.json()

        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        async with session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": self.bot.API_KEY,
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


async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
