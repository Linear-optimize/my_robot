import subprocess
import re

from pathlib import Path
import os
import aiohttp
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "referer": "https://www.bilibili.com/",
}


class Updown:
    async def get_request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as req:
                if req.status != 200:
                    print(f"Error fetching URL:Status Code is {req.status}")
                    return None

                response = await req.text()

                return response

    async def get_video_data(self, url):
        response = await self.get_request(url)

        audio_url = None
        video_url = None

        html_data_regex = re.compile(r"<script>window.__playinfo__=(.*?)</script>")
        html_data_match = html_data_regex.search(response)

        if html_data_match:
            html_data = html_data_match.group(1).strip()

            try:
                json_data = json.loads(html_data)
                audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
                video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error cased by JSON {e}")

        return {"videoUrl": video_url, "audioUrl": audio_url}

    async def process_bili(self, url, usr_id):
        video_info = await self.get_video_data(url)

        v_file = f"video_{usr_id}.m4s"
        a_file = f"audio_{usr_id}.m4s"
        out_file = f"output_{usr_id}.mp4"

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(video_info["videoUrl"]) as req:
                v_content = await req.read()
                Path(v_file).write_bytes(v_content)

            async with session.get(video_info["audioUrl"]) as req:
                a_content = await req.read()
                Path(a_file).write_bytes(a_content)

        cmd = ["ffmpeg", "-i", v_file, "-i", a_file, "-c", "copy", "-y", out_file]
        subprocess.run(cmd, capture_output=True, check=True)
        print("视频合并")

        os.remove(v_file)
        print("v_file.m4s删除")
        os.remove(a_file)
        print("f_file.m4s删除")
        return out_file
