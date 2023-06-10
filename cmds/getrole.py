import disnake
from disnake.ext import commands
from disnake.ui import View, Button
from disnake.enums import ButtonStyle
from config import CMD_DEF, CMD_SUC, CMD_LOG, CMD_ERR


class GetRole(View):
    def __init__(self):
        super().__init__(timeout=600)

    @disnake.ui.button(label="", style=ButtonStyle.blurple, custom_id="get_role")
    async def get_role(self, button: disnake.Button, inter):
        role = inter.guild.get_role(1116701992941789265)
        if role in inter.author.roles:
            await inter.author.remove_roles(role)
        else:
            await inter.author.add_roles(role)
        await inter.response.defer()


class GetRoleCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.has_permissions(administrator=True)
    @commands.command(name="role")
    async def role(self, ctx):
        view = GetRole()
        emb = disnake.Embed(
            title="Получение роли",
            description="Нажми на кнопку для получения роли"
        )
        await ctx.send(embed=emb, view=view)


def setup(bot):
    bot.add_cog(GetRoleCmd(bot))
