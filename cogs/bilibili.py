import discord
from discord.ext import commands
import subprocess
import re
import requests
from pathlib import Path
import os
import asyncio
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "referer": "https://www.bilibili.com/",
}


class Updown:
    def get_request(self, url):
        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            print(f"Error fetching URL:Status Code is {response.status_code}")
            return None

        return response

    def get_video_data(self, url):
        response = self.get_request(url)

        audio_url = None
        video_url = None

        html_data_regex = re.compile(r"<script>window.__playinfo__=(.*?)</script>")
        html_data_match = html_data_regex.search(response.text)

        if html_data_match:
            html_data = html_data_match.group(1).strip()

            try:
                json_data = json.loads(html_data)
                audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
                video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error cased by JSON {e}")

        return {"videoUrl": video_url, "audioUrl": audio_url}

    def process_bili(self, url, usr_id):
        video_info = self.get_video_data(url)

        v_file = f"video_{usr_id}.m4s"
        a_file = f"audio_{usr_id}.m4s"
        out_file = f"output_{usr_id}.mp4"

        v_content = requests.get(url=video_info["videoUrl"], headers=headers)
        Path(v_file).write_bytes(v_content.content)

        a_content = requests.get(url=video_info["audioUrl"], headers=headers)
        Path(a_file).write_bytes(a_content.content)

        cmd = ["ffmpeg", "-i", v_file, "-i", a_file, "-c", "copy", "-y", out_file]
        subprocess.run(cmd, capture_output=True, check=True)
        print("视频合并")

        os.remove(v_file)
        print("v_file.m4s删除")
        os.remove(a_file)
        print("f_file.m4s删除")
        return out_file


class BilibiliCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updown = Updown()

    @commands.hybrid_command()
    async def bilibili(self, ctx, url: str):
        await ctx.defer()

        output_file = await asyncio.to_thread(
            self.updown.process_bili, url, ctx.author.id
        )
        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)
        print("删除原视频缓存")


async def setup(bot):
    await bot.add_cog(BilibiliCog(bot))
