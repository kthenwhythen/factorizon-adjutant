import asyncio
import subprocess
import os
import sys
from dotenv import load_dotenv

import discord
from discord.ext import commands
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
server_ip = "172.26.254.246"
server_status = "OFFLINE"
server_save = None
server_instance = None


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
    global server_instance
    if action == "start":
        if save:
            await ctx.send(f"```fix\nStarting Factorio server with save: '{save}'\n```")
            server_instance = subprocess.Popen(f"..\\factorio.exe --start-server ..\\saves\\{save}.zip --server-settings .\\server-settings.json", shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            # server_instance = subprocess.Popen(["../factorio.exe", "--start-server", f"../saves/{save}.zip", "--server-settings", "./server-settings.json"], shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            # server_instance.poll()
            # (output, err) = server_instance.communicate()
            # print(output)
            await asyncio.sleep(9)
            print("Server Up")
            server_save = save
            server_status = "ONLINE"
            await server_guild.edit(icon=icon_online)
            await ctx.send("```xl\n'SERVER ONLINE'\n```")
        elif server_save:
            await ctx.send(f"```fix\nStarting Factorio server with save: '{server_save}'\n```")
            server_instance = subprocess.Popen(["../factorio.exe", "--start-server", f"../saves/{server_save}.zip", "--server-settings", "./server-settings.json"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # server_instance.poll()
            await asyncio.sleep(7)
            print("Server Up")
            server_status = "ONLINE"
            await server_guild.edit(icon=icon_online)
            await ctx.send("```xl\n'SERVER ONLINE'\n```")
        else:
            await ctx.send("```prolog\nSave File Not Specified\n```")

    elif action == "stop" and server_status == "ONLINE":
        await ctx.send(f"```fix\nStopping Factorio server\n```")
        server_instance.stdin.write(b'/c game.server_save()')
        server_instance.stdin.flush()
        await asyncio.sleep(2)
        server_instance.kill()
        print("Server Down")
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
    await member.send(f"```fix\nДобро пожаловать на Factorizon!\n```")
    await member.send(f"```fix\nДля соедниения с сервером используйте 'zerotier'\n```")
    await member.send(f"https://www.zerotier.com/download/")
    await member.send(f"```fix\nВ самом 'zerotier' вам следует подключиться к сети указав код ниже\n```")
    await member.send(f"```\na0cbf4b62a940d6c\n```")
    await member.send(f"```fix\nСтатус сервера можно узнать по цвету иконки Дискорд-сервера\n```")
    await member.send(f"```fix\nIP адрес сервера можно узнать через команду !status\n```")


@bot.command(aliases=["s"])
async def status(ctx):
    if server_status == "ONLINE":
        await ctx.send(f"```xl\n'Status: {server_status}, Ip: {server_ip}, Save: {server_save}'\n```")
    if server_status == "OFFLINE":
        await ctx.send(f"```prolog\nStatus: {server_status}, Ip: {server_ip}, Save: {server_save}\n```")


@bot.command(aliases=["c"], pass_context=True)
@commands.has_permissions(administrator=True)
async def console(ctx, *args):
    global server_instance
    if server_status == "ONLINE":
        server_instance.stdin.write(" ".join(list(args)).replace("'", '\"'))
        server_instance.stdin.flush()
    if server_status == "OFFLINE":
        await ctx.send(f"```prolog\nERROR: SERVER OFFLINE\n```")


@bot.command(aliases=["tp"], pass_context=True)
async def teleport(ctx, *args):
    global server_instance
    if server_status == "ONLINE":
        server_instance.stdin.write(f"/c game.players[\"{args[0]}\"]" + ".teleport({-15325, 9373})")
        server_instance.stdin.flush()
    if server_status == "OFFLINE":
        await ctx.send(f"```prolog\nERROR: SERVER OFFLINE\n```")

@bot.command(aliases=["l"])
async def log(ctx):
    global server_instance
    if server_status == "ONLINE":
        print("Logs created")

        for stdout_line in iter(server_instance.stdout.readline, ""):
            print(stdout_line) 
        # server_instance.stdout.close() 

    if server_status == "OFFLINE":
        await ctx.send(f"```prolog\nERROR: SERVER OFFLINE\n```")

bot.run(TOKEN)
