from disnake.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test(self, inter):
        await inter.response.send_message("Test")


def setup(bot):
    bot.add_cog(Test(bot))
