import discord
from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="ping命令")
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.hybrid_command(name="add", description="加法")
    async def add(self, ctx, a: int, b: int):
        await ctx.send(a + b)

    @commands.hybrid_command(name="draw", description="图片")
    async def draw(self, ctx):
        await ctx.defer()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        }

        url = "https://www.98qy.com/sjbz/api.php?lx=dongman&format=json"
        session = self.bot.http_session

        async with session.get(url=url, headers=headers) as response:
            data = await response.json(content_type=None)

        url_image = data["imgurl"]
        embed = discord.Embed()
        embed.set_image(url=url_image)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FunCog(bot))
