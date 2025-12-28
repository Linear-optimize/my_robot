from discord.ext import commands
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models
import json


class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="translate", description="翻译")
    async def translate(self, ctx, source: str, target: str, phrase: str):
        await ctx.defer()

        cred = credential.Credential(
            secret_id=self.bot.secretld, secret_key=self.bot.secretkey
        )
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


async def setup(bot):
    await bot.add_cog(TranslateCog(bot))
