from typing import Optional
import disnake
from disnake.enums import TextInputStyle
from disnake.ext import commands
from config import CMD_SUC, CMD_LOG, CMD_DEF


class ReportModal(disnake.ui.Modal):
    def __init__(self, timeout=100) -> None:
        components = [
            disnake.ui.TextInput(
                label="Ваш никнейм | ID",
                placeholder="Пример: akyma | STEAM_1:0:601802717",
                custom_id="mynickname",
                min_length=5,
                max_length=200
            ),
            disnake.ui.TextInput(
                label="Никнейм | ID Администратора",
                placeholder="Пример: akyma | STEAM_1:0:601802717",
                custom_id="mynickname",
                min_length=5,
                max_length=200
            ),
            disnake.ui.TextInput(
                label="Причина",
                placeholder="",
                custom_id="reason",
                style=TextInputStyle.paragraph,
                min_length=10,
                max_length=500
            ),
            disnake.ui.TextInput(
                label="Доказательства",
                placeholder="",
                custom_id="screenshot",
                style=TextInputStyle.paragraph,
                min_length=5,               
                max_length=120
            ),            
        ]
        title = "Жалоба на администратора"
        super().__init__(title=title, components=components, custom_id="reportModal", timeout=timeout)

    async def callback(self, inter: disnake.ModalInteraction):
        mynickname = inter.text_values["mynickname"]
        nickname = inter.text_values["nicknameadmin"]
        reason = inter.text_values["reason"]
        screen = inter.text_values["screenshot"]
        embed = disnake.Embed(
            title="Вы отправили жалобу на администратора!",
            description=f"{inter.author.mention}, Ваша жалоба была **отправлена**!",
            color=CMD_SUC,
        )
        channel = inter.guild.get_channel(1116378862008410194)
        await inter.response.send_message(embed=embed, ephemeral=True)

        embed1 = disnake.Embed(
            description=f"<:profilemimic:1116460443658109078> {inter.author.mention}\n",
            colour=CMD_LOG
        )
        embed1.add_field(name="Ваш никнейм | ID :", value=mynickname, inline=False)
        embed1.add_field(name="Никнейм | ID нарушителя:", value=nickname, inline=False)
        embed1.add_field(name="Причина:", value=reason, inline=False)
        embed1.add_field(name="Доказательство:", value=screen, inline=False)
        embed1.set_thumbnail(url=inter.author.display_avatar)
        await channel.send(embed=embed1)
        await channel.send("<@&1114972511541674056>")


class ReportButton(disnake.ui.View):
    def __init__(self, timeout=300) -> None:
        super().__init__(timeout=timeout)

    @disnake.ui.button(label="Написать жалобу", style=disnake.ButtonStyle.blurple, custom_id="btnreport", emoji="<:sendmimic:1116461445866082414>")
    async def btnreport(self, button: disnake.ui.Button, inter):
        await inter.response.send_modal(modal=ReportModal())


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name="report")
    async def report(self, ctx):
        msg_id = ctx.message.id
        view = ReportButton()
        emb_rep = disnake.Embed(
            title="Жалоба на администрацию",
            description=f"<:staffmimic:1116460000504713328> Чтобы подать **жалобу на администрацию**, нужно нажать на кнопку ниже.\n\n"
                        f"<:editmimic:1116460446417944639> Все жалобы отправленные нам рассматриваются **наборными рангами St.Admin+**\n"
                        f"<:questionmimic:1116459807818391653> Если у вас нет этой кнопки, попробуйте обновить версию Discord\n",
            colour=CMD_DEF
        )
        emb_rep.add_field(name="", value="")
        emb_rep.set_footer(text="С уважением, Высшая Администрация проекта MimicRP",
                           icon_url=self.bot.user.display_avatar)
        await ctx.send(embed=emb_rep, view=view)


def setup(bot):
    bot.add_cog(Report(bot))
