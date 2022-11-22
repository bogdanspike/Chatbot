import datetime
import discord
import os

from antispam import AntiSpamHandler, UnsupportedAction
from antispam.enums import Library
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="b.", intents=intents)
bot.handler = AntiSpamHandler(bot, library=Library.DPY)
restricted_channel = 'bot-commands'


@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----")


@bot.event
async def on_message(message):
    try:
        await bot.handler.propagate(message)
        await bot.process_commands(message)
    except UnsupportedAction as e:
        print(e)
        await message.author.timeout(datetime.timedelta(seconds=10))
        await message.author.send('Timed-out for spam!')


@bot.command(name='info')
async def info(message):
    if str(message.channel) == restricted_channel:
        await message.channel.send('Commands sent!')
        await message.author.send('```\n'
                                  'Commands:\n'
                                  'stats - [ADMIN-ONLY] -Info about a specific user: UserID, Role, Avatar \n'
                                  'clear - Specify the number of messages you want to clear\n'
                                  '```')
    else:
        await message.delete()
        await message.channel.send('Command restricted for bot-commands only!')


@bot.command(name='stats')
async def stats(message):
    isAdmin = [role.name == 'Admin' for role in message.author.roles]
    if isAdmin:
        if str(message.channel) == restricted_channel:
            await message.channel.send(message.author.roles[1])
            await message.channel.send(bot.user.id)
            await message.channel.send(bot.user.name)
            await message.channel.send(bot.user.avatar)
        else:
            await message.delete()
            await message.channel.send('Command restricted for bot-commands only!')
    else:
        await message.delete()
        message.channel.send('Unauthorized access')



@bot.command(name='clear')
async def clear(ctx, amount):
    if str(ctx.channel) == restricted_channel:
        await ctx.channel.purge(limit=int(amount))
    else:
        await ctx.delete()
        await ctx.channel.send('Command restricted for bot-commands only!')


if __name__ == '__main__':
    bot.run(os.environ['token'])
