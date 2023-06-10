import disnake
from disnake.ext import commands
from pymongo import MongoClient
from config import CMD_DEF, CMD_SUC, CMD_LOG, MONGO_URI, CMD_ERR
from disnake.ui import View
from disnake.enums import ButtonStyle


class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=150)

    @disnake.ui.button(emoji="<:true:1117159248946811021>", label="Подтвердить", custom_id="verifybtn", style=ButtonStyle.primary)
    async def verifybtn(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        role = interaction.guild.get_role(1117163177113821294)
        if role in interaction.author.roles:
            await interaction.author.add_roles(role)
            await interaction.send(embed=disnake.Embed(
                description=f"Вы уже прошли верификацию!", colour=CMD_ERR), delete_after=5.0, ephemeral=True)
        else:
            await interaction.author.add_roles(role)
            await interaction.send(embed=disnake.Embed(
                description=f"Вы прошли верификацию, успешно!", colour=CMD_SUC), delete_after=5.0, ephemeral=True)
        await interaction.response.defer()


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command(name="verify")
    async def verify(self, ctx):
        view = VerifyView()
        emb = disnake.Embed(
            title="Верификация",
            description="Чтобы пройти верификацию, вам необходимо нажать на кнопку.\n"
                        "Нажимая кнопку 'Подтвердить', вы получаете доступ к использованию сервера\n",
            colour=CMD_DEF
        )
        await ctx.send(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Verify(bot))
