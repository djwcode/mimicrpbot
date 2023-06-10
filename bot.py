import disnake
import os
from pymongo import MongoClient
from config import TOKEN, PREFIX, MONGO_URI
from disnake.ext import commands

bot = commands.Bot(command_prefix=PREFIX, intents=disnake.Intents.all())
cluster = MongoClient(MONGO_URI)
db = cluster["bze5ksolyt7no2d"]
warns_table = db["warns"]
bans_table = db["bans"]


@bot.event
async def on_ready():
    print("Бот запущен")
    await bot.change_presence(activity=disnake.Streaming(name="MimicRP | /help", url="https://twitch.tv/1111"))


@bot.event
async def on_member_join(member):
    warns = 0
    reason = str
    warn_data = {
        '_user_id': member.id,
        '_warns': warns,
        '_reason': reason
    }
    warns_table.insert_one(warn_data)
    bans_data = {
        '_id': member.id,
        '_reason': reason
    }
    bans_table.insert_one(bans_data)


@bot.event
async def on_member_remove(member):
    warns_table.delete_one({'_id': member.id})


for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")

bot.run(f"{TOKEN}")
