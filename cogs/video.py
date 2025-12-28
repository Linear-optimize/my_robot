import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os


class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="video", description="从支持的网站下载视频")
    async def video(self, ctx, url: str):
        await ctx.defer()

        save_path = f"video_{ctx.author.id}.mp4"

        DOWNLOAD_OPTIONS = {
            "format": "best[ext=mp4][filesize<25M]/worst[ext=mp4]",
            "outtmpl": save_path,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
        }

        with yt_dlp.YoutubeDL(DOWNLOAD_OPTIONS) as ydl:
            await asyncio.to_thread(ydl.download, [url])

        file = discord.File(save_path)
        await ctx.send(content="视频播放开始", file=file)
        os.remove(save_path)


async def setup(bot):
    await bot.add_cog(VideoCog(bot))
