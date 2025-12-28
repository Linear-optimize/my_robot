import discord
from discord.ext import commands
import os

from utils.updown_bilibili import Updown


class BilibiliCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updown = Updown()

    @commands.hybrid_command(name="bilibili", description="下载B站视频")
    async def bilibili(self, ctx, url: str):
        await ctx.defer()

        output_file = await self.updown.process_bili(url, ctx.author.id)

        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)
        print("删除原视频缓存")


async def setup(bot):
    await bot.add_cog(BilibiliCog(bot))
