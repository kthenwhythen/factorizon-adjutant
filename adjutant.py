import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
with open('online.png', 'rb') as f:
    icon_online = f.read()
with open('offline.png', 'rb') as f:
    icon_offline = f.read()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
server_guild = None
server_ip = "127.0.0.1"
server_status = "OFFLINE"
server_save = None


@bot.event
async def on_ready():
    global server_guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    server_guild = bot.get_guild(guild.id)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@bot.command(name="server", pass_context=True)
@commands.has_permissions(administrator=True)
async def server(ctx, action='', save=None):
    global server_status
    global server_save
    if action == "start":
        if save:
            await ctx.send(f"```fix\nStarting Factorio server with save: '{save}'\n```")
            server_save = save
            server_status = "ONLINE"
            await server_guild.edit(icon=icon_online)
            await ctx.send("```xl\n'SERVER ONLINE'\n```")
        else:
            await ctx.send("```prolog\nSave File Not Specified\n```")

    elif action == "stop":
        await ctx.send(f"```fix\nStopping Factorio server\n```")
        server_status = "OFFLINE"
        await server_guild.edit(icon=icon_offline)
        await ctx.send("```prolog\nSERVER OFFLINE\n```")

    elif action == "status":
        if server_status == "ONLINE":
            await ctx.send(f"```xl\n'Status: {server_status}, Ip: {server_ip}, Save: {server_save}'\n```")
        if server_status == "OFFLINE":
            await ctx.send(f"```prolog\nStatus: {server_status}, Ip: {server_ip}, Save: {server_save}\n```")

    else:
        await ctx.send(f"```prolog\nUndefined Command\n```")


@bot.event
async def on_member_join(member):
    await member.send(f"```\n1010101010000110011011111\n```")
    await member.send(f"```fix\nДобро пожаловать на Factorizon!\n```")
    await member.send(f"```fix\nДля соедниения с сервером используйте 'zerotier'\n```")
    await member.send(f"https://www.zerotier.com/download/")
    await member.send(f"```fix\nВ самом 'zerotier' вам следует подключиться к сети указав код ниже\n```")
    await member.send(f"```\na0cbf4b62a940d6c\n```")
    await member.send(f"```fix\nСтатус сервера можно узнать по цвету иконки Дискорд-сервера\n```")
    await member.send(f"```fix\nIP адрес сервера можно узнать через команду !status\n```")


@bot.command(name="status")
async def server(ctx):
    if server_status == "ONLINE":
        await ctx.send(f"```xl\n'Status: {server_status}, Ip: {server_ip}, Save: {server_save}'\n```")
    if server_status == "OFFLINE":
        await ctx.send(f"```prolog\nStatus: {server_status}, Ip: {server_ip}, Save: {server_save}\n```")






########## Fun
@bot.command(aliases=["vanyapidor"])
async def toxic(message):
    await message.channel.send(f"```fix\n{random.choice(['Agree', 'Yes', 'Exactly', '+'])}\n```")


@bot.command(aliases=["albertpidor"])
async def toxic_counter(message):
    await message.channel.send(f"```prolog\nProceeding To Ban User: '{message.author.name}'\n```")
    await asyncio.sleep(3)
    await message.channel.send("```fix\nin 1\n```")
    await asyncio.sleep(1)
    await message.channel.send("```fix\n2\n```")
    await asyncio.sleep(1)
    await message.channel.send("```fix\n3\n```")
    await asyncio.sleep(1)
    await message.channel.send("```Deactivated```")


bot.run(TOKEN)
