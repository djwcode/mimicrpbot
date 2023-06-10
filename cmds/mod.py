import asyncio
import disnake
from disnake.ext import commands
from pymongo import MongoClient
from config import CMD_SUC, CMD_LOG, MONGO_URI
from datetime import datetime


class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient(MONGO_URI)
        self.db = self.cluster["bze5ksolyt7no2d"]
        self.collection = self.db["warns"]
        self.ban_table = self.db["bans"]

    @commands.command(name="dataload")
    async def db_load(self, ctx):
        warns = 0
        reason = ''
        guild = self.bot.get_guild(1114909034093486102)
        for member in guild.members:
            user = member.id
            data = {
                "_user_id": user,
                "_warns": warns,
                '_reason': reason
            }
            self.collection.insert_one(data)
            if self.collection.count_documents({"_user_id": user}) == 0:
                self.collection.insert_one(data)

    @commands.has_guild_permissions(administrator=True)
    @commands.slash_command(name="очистить", description="позволяет очистить чат")
    async def clear(self, inter, amount: int = commands.Param(name="количество")):
        if amount > 250:
            await inter.response.send_message("Нельзя больше 250")

        await inter.channel.purge(limit=amount + 1)
        emb = disnake.Embed(
            description=f"Очищено {amount} сообщений",
            colour=CMD_SUC
        )
        await inter.send(embed=emb, delete_after=5.0)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="бан", description="позволяет забанить участника")
    async def ban(self, inter, member: disnake.Member = commands.Param(name="участник"),
                  reason: str = commands.Param(name="причина", default="причина")):
        channel = inter.guild.get_channel(1116835474053529600)
        role = inter.guild.get_role(1116478759424512063)
        emb = disnake.Embed(
            description=f"<:profilemimic:1116460443658109078> {member.mention} получил бан\n"
                        f"<:handcuffs:1117153303411822633> Причина: {reason}\n\n"
                        f"<:moderator:1117148597746667540> Модератор: {inter.author.mention}\n"
                        f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n",
            colour=CMD_LOG
        )
        await member.add_roles(role)
        await channel.send(embed=emb)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)
        self.ban_table.insert_one({
            '_id': member.id,
            '_reason': reason
        })

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="разбан", description="позволяет разбанить участника")
    async def unban(self, inter, member: disnake.Member = commands.Param(name="участник")):
        channel = inter.guild.get_channel(1116835474053529600)
        role = inter.guild.get_role(1116478759424512063)
        emb = disnake.Embed(
            description=f"<:moderator:1117148597746667540> Модератор {inter.author.mention} разбанил {member.mention}\n"
                        f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n",
            colour=CMD_LOG
        )
        await member.remove_roles(role)
        await channel.send(embed=emb)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)

        reason = None
        self.ban_table.delete_one({
            '_id': member.id,
            '_reason': reason
        })

    @commands.has_permissions(administrator=True, manage_roles=True, moderate_members=True, mute_members=True)
    @commands.slash_command(name="мут", description="позволяет заглушить участника")
    async def mute(self, inter,
                   member: disnake.Member = commands.Param(name="участник"),
                   time: str = commands.Param(name="время", description="с, м, ч, д"),
                   reason: str = commands.Param(name="причина", default="не указана")):

        time_conversion = {"с": 1, "м": 60, "ч": 3600, "д": 86400}
        mute_time = int(time[:-1]) * time_conversion[time[-1]]
        channel = inter.guild.get_channel(1116835554764533840)
        guild = inter.guild
        mute_rolemute = disnake.utils.get(guild.roles, name="Мут")
        if not mute_rolemute:
            mute_rolemute = await guild.create_role(name="Мут", color=disnake.Color.dark_gray)
            for channel in guild.channels:
                await channel.set_permissions(mute_rolemute, speak=False, send_messages=False,
                                              read_message_history=True,
                                              read_messages=False)
        if mute_rolemute in member.roles:
            await inter.send(f"{member.mention} уже заглушен!", delete_after=5.0)
        else:
            await member.add_roles(mute_rolemute)
            muted_embed = disnake.Embed(colour=CMD_LOG,
                                        title="Мут",
                                        description=f"<:profilemimic:1116460443658109078> {member.mention} получил мут\n"
                                                    f"<:handcuffs:1117153303411822633> Причина: {reason}\n\n"
                                                    f"<:moderator:1117148597746667540> Модератор: {inter.author.mention}\n"
                                                    f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n")
            await channel.send(embed=muted_embed)
            await asyncio.sleep(mute_time)
            await member.remove_roles(mute_rolemute)
            await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                              delete_after=5.0)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="размут")
    async def unmute(self, inter, member: disnake.Member):
        guild = inter.guild
        mute_rolemute = disnake.utils.get(guild.roles, name="Мут")
        channel = inter.guild.get_channel(1116835554764533840)
        unmute_embed = disnake.Embed(colour=CMD_LOG,
                                     title="Размут",
                                     description=f"<:moderator:1117148597746667540> Модератор: {inter.author.mention} размьютил {member.mention}\n"
                                                 f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n")
        await channel.send(embed=unmute_embed)
        await member.remove_roles(mute_rolemute)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)

    @commands.has_permissions(administrator=True, manage_roles=True, moderate_members=True, mute_members=True)
    @commands.slash_command(name="таймаут", description="позволяет замьютить участника")
    async def timeout(self, inter,
                      member: disnake.Member = commands.Param(name="участник"),
                      time: str = commands.Param(name="время", description="с, м, ч, д"),
                      reason: str = commands.Param(name="причина", default="не указана")):

        channel = inter.guild.get_channel(1116835554764533840)
        time_conversion = {"с": 1, "м": 60, "ч": 3600, "д": 86400}
        mute_time = int(time[:-1]) * time_conversion[time[-1]]
        time_end = mute_time + datetime.now().timestamp()

        await member.timeout(duration=mute_time)
        muted_embed = disnake.Embed(colour=CMD_LOG,
                                    title="Тайм-аут",
                                    description=f"<:profilemimic:1116460443658109078> {member.mention} получил мут\n"
                                                f"<:handcuffs:1117153303411822633> Причина: {reason}\n\n"
                                                f"<:moderator:1117148597746667540> Модератор: {inter.author.mention}\n"
                                                f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n")
        await channel.send(embed=muted_embed)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)
        await inter.response.defer()

    @commands.has_permissions(administrator=True, manage_roles=True, moderate_members=True, mute_members=True)
    @commands.slash_command(name="антаймаут", description="позволяет размьютить участника")
    async def untimeout(self, inter,
                        member: disnake.Member = commands.Param(name="участник")):
        channel = inter.guild.get_channel(1116835554764533840)
        await member.timeout(reason=None, until=None)
        muted_embed = disnake.Embed(colour=CMD_LOG,
                                    description=f"Был размьючен {member.mention} администратором {inter.author.mention}")
        await channel.send(embed=muted_embed)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="варн", description="позволяет выдать варн участнику")
    async def warn_command(self, inter, user: disnake.Member = commands.Param(name="участник"),
                           reason: str = commands.Param(name="причина", default="не указана")):
        channel = inter.guild.get_channel(1116835618396307526)
        warn_count = self.collection.find_one({'_user_id': user.id})['_warns']
        emb = disnake.Embed(
            description=f"<:profilemimic:1116460443658109078> {user.mention} получил варн\n"
                        f"<:handcuffs:1117153303411822633> Причина: {reason}\n\n"
                        f"<:moderator:1117148597746667540> Модератор: {inter.author.mention}\n"
                        f"<:hoursmimicrp:1116472998376001566> Время: <t:{int(datetime.now().timestamp())}:f>\n",
            colour=CMD_LOG
        )

        self.collection.update_one({'_user_id': user.id}, {'$set': {'_warns': warn_count + 1, '_reason': reason}})
        await channel.send(embed=emb)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="чекварн")
    async def warnings(self, inter, user: disnake.Member = commands.Param(name="участник")):
        channel = inter.guild.get_channel(1116835618396307526)
        if self.collection.find_one({'_user_id': user.id})['_warns'] == 0 or 5 or 6 or 7 or 8 or 9 or 10:
            emb = disnake.Embed(
                description=f"{user.mention} имеет {self.collection.find_one({'_user_id': user.id})['_warns']} варнов",
                colour=CMD_LOG
            )
            return await channel.send(embed=emb)
        if self.collection.find_one({'_user_id': user.id})['_warns'] == 1:
            emb1 = disnake.Embed(
                description=f"{user.mention} имеет {self.collection.find_one({'_user_id': user.id})['_warns']} варн",
                colour=CMD_LOG
            )
            return await channel.send(embed=emb1)
        if self.collection.find_one({'_user_id': user.id})['_warns'] == 2 or 3 or 4:
            emb2 = disnake.Embed(
                description=f"{user.mention} имеет {self.collection.find_one({'_user_id': user.id})['_warns']} варна",
                colour=CMD_LOG
            )
            return await channel.send(embed=emb2)
        await inter.response.send_message(embed=disnake.Embed(description="Успешно, выполнил!", colour=CMD_SUC),
                                          delete_after=5.0)


def setup(bot):
    bot.add_cog(Moderator(bot))
