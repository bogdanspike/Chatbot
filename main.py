import datetime
import random

import people_also_ask

import discord
import os
from datetime import datetime
from antispam import AntiSpamHandler, UnsupportedAction
from antispam.enums import Library
from discord.ext import commands
from typing import Optional
from load_data import load_data
from discord import Embed, Member

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="b.", intents=intents)
bot.handler = AntiSpamHandler(bot, library=Library.DPY)
restricted_channel = 'bot-commands'

quotes = load_data()


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
async def stats(message,member: Optional[Member]):
    isAdmin = [role.name == 'Admin' for role in message.author.roles]
    if isAdmin:
        if str(message.channel) == restricted_channel:
            await message.channel.send(member.roles[1])
            await message.channel.send(member.id)
            await message.channel.send(member.name)
            await message.channel.send(member.status)

        else:
            await message.delete()
            await message.channel.send('Command restricted for bot-commands only!')
    else:
        await message.delete()
        message.channel.send('Unauthorized access')


@bot.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
async def user_info(message, target: Optional[Member]):
    try:
        embed = Embed(title="User information",
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar.url)

        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top role", target.top_role.mention, True),
                  ("Status", str(target.status).title(), True),
                  ("Activity",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}",
                   True),
                  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await message.send(embed=embed)
    except Exception as e:
        print(e)
        await message.channel.send('Nu avem')


@bot.command(name='clear')
async def clear(ctx, amount):
    if str(ctx.channel) == restricted_channel:
        await ctx.channel.purge(limit=int(amount))
    else:
        await ctx.delete()
        await ctx.channel.send('Command restricted for bot-commands only!')


@bot.command(name='quotes')
async def quotes_thing(message):
    quote = random.choice(quotes)
    message_to_send = quote.content
    if quote.author:
        message_to_send += f"\n{quote.author.replace('    ', '')}"
    await message.channel.send(message_to_send)


@bot.command(name='question')
async def quotes_thing(message):
    message_content = message.message.content.replace("b.question ", "")
    response = people_also_ask.get_answer(message_content)
    if response.get("has_answer", False):
        to_send = response.get("response") or "Unknown"
        if to_send == "Unknown":
            to_send = next(people_also_ask.generate_answer(message_content), "Unknown")
            if to_send.get("has_answer"):
                if to_send.get("related_questions"):
                    response = people_also_ask.get_answer(to_send.get("related_questions")[0])
                    to_send = response.get("response") or "Unknown"
        await message.channel.send(to_send)
    else:
        await message.channel.send("Unknown")


if __name__ == '__main__':
    bot.run(os.environ['token'])
