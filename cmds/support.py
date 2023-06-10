import disnake
from disnake.ext import commands
from disnake.ui import View, Modal
from disnake.enums import TextInputStyle
from config import CMD_SUC, CMD_LOG, CMD_DEF
from pymongo import MongoClient


class SetSupportModal(Modal):
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
                label="Ваш возраст",
                placeholder="Ограничение: 14+ (есть исключения)",
                custom_id="myage",
                style=TextInputStyle.single_line,
                max_length=2
            ),
            disnake.ui.TextInput(
                label="Есть ли у вас рабочий микрофон?",
                placeholder="+ или -",
                custom_id="mymicrophone",
                style=TextInputStyle.single_line,
                max_length=1
            ),
            disnake.ui.TextInput(
                label="Какая у вас привилегия?",
                placeholder="",
                custom_id="mydonate",
                style=TextInputStyle.paragraph,
                max_length=10
            ),
            disnake.ui.TextInput(
                label="Сколько наигранных часов?",
                placeholder="",
                custom_id="myhours",
                style=TextInputStyle.paragraph,
                max_length=3
            ),
        ]
        title = "Подать заявку на саппорта"
        super().__init__(title=title, components=components, custom_id="reportModal", timeout=timeout)
        self.cluster = MongoClient("mongodb://uyumhytfkemxo4tzukda:GDRqH4Im8knhNWddnFHk@n1-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017,n2-c2-mongodb-clevercloud-customers.services.clever-cloud.com:27017/bt5coevctrqzgw4?replicaSet=rs0")
        self.db = self.cluster["bt5coevctrqzgw4"]
        self.collection = self.db["tickets"]

    async def callback(self, inter: disnake.ModalInteraction):
        mynickname = inter.text_values["mynickname"]
        myage = inter.text_values["myage"]
        mymicro = inter.text_values["mymicrophone"]
        mydonate = inter.text_values["mydonate"]
        myhours = inter.text_values["myhours"]

        self.collection.insert_one({
            '_nickname': mynickname,
            '_age': myage,
            '_micro': mymicro,
            '_donate': mydonate,
            '_hours': myhours
        })

        embed = disnake.Embed(
            title="Вы отправили свою заявку на саппорта!",
            description=f"{inter.author.mention}, Ваша анкета была **отправлена**!",
            color=CMD_SUC,
        )
        channel = inter.guild.get_channel(1116470302445154414)
        await inter.response.send_message(embed=embed, ephemeral=True)

        embed1 = disnake.Embed(
            description=f"<:profilemimic:1116460443658109078> {inter.author.mention}\n",
            colour=CMD_LOG
        )
        embed1.add_field(name="<:profilemimic:1116460443658109078> Никнейм | ID :", value=mynickname, inline=False)
        embed1.add_field(name="<:agemimicrp:1116472182005047356> Возраст:", value=myage, inline=False)
        embed1.add_field(name="<:microphonemimicrp:1116471994909732984> Микрофон:", value=mymicro, inline=False)
        embed1.add_field(name="<:rankmimicrp:1116472779068412065> Привилегия:", value=mydonate, inline=False)
        embed1.add_field(name="<:hoursmimicrp:1116472998376001566> Часов:", value=myhours, inline=False)
        embed1.set_thumbnail(url=inter.author.display_avatar)
        await channel.send(embed=embed1)
        await channel.send("<@&1114972511541674056>")


class SetSupportButton(View):
    def __init__(self, timeout=300) -> None:
        super().__init__(timeout=timeout)

    @disnake.ui.button(label="Подать заявку", style=disnake.ButtonStyle.blurple, custom_id="btnsetsup")
    async def btnsetsup(self, button: disnake.ui.Button, inter):
        await inter.response.send_modal(SetSupportModal())


class SetSupport(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        msg_id = ctx.message.id
        view = SetSupportButton()
        emb_rep = disnake.Embed(
            title="Набор на хелпера",
            description=f"<:staffmimic:1116460000504713328> Чтобы подать свою анкету на **вакансию Хелпера**, нужно нажать на кнопку ниже.\n\n"
                        f"<:editmimic:1116460446417944639> Все анкеты отправленные нам, рассматриваются **наборным рангом - Founder**\n"
                        f"<:hoursmimicrp:1116472998376001566> Повторно подать свою анкету можно будет через **3 дня**.\n"
                        f"<:questionmimic:1116459807818391653> Если у вас нет этой кнопки, попробуйте **обновить версию Discord**\n",
            colour=CMD_DEF
        )
        emb_rep.set_thumbnail(url=ctx.guild.icon)
        emb_rep.add_field(name="", value="")
        emb_rep.set_footer(text="С уважением, Высшая Администрация проекта MimicRP",
                           icon_url=self.bot.user.display_avatar)
        await ctx.send(embed=emb_rep, view=view)


def setup(bot):
    bot.add_cog(SetSupport(bot))