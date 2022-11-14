import discord, os


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if (message.author.bot == False):
            channel = message.channel.name
            restricted_channels = ['bot-commands']

            prefix = "b."
            if message.content.startswith(prefix):
                if channel in restricted_channels:
                    command = message.content[len(prefix):]
                    isAdmin = [role.name == 'Admin' for role in message.author.roles]

                    if command == 'help':
                        await message.reply('Done')
                        await message.author.send('```\n'
                                                  'Commands:\n'
                                                  'help - This is the help command\n'
                                                  'stats - This is the status command\n'
                                                  '```')
                    if command == 'stats':
                        members = len([member for member in self.users])
                        print(members)
                        if isAdmin:
                            await message.channel.send('The stats were sent!')
                            await message.author.send(members)
                        else:
                            await message.channel.send('You have no access to this command.')

                    else:
                        await message.channel.send('This command does not exist.')

                else:
                    await message.delete()
                    await message.channel.send('PyHelper is restricted for bot-commands channel.')
        else:
            await message.delete()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = MyClient(intents=intents)
client.run(os.environ['token'])
