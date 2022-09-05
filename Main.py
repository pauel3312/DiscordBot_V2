import discord
import xml.etree.ElementTree as Et
from random import choice

config_root = Et.parse("config.xml").getroot()
commands_root = Et.parse("commands.xml").getroot()

TOKEN = open("TOKEN", 'r').read()
GuildID = int(config_root.find("guildID").attrib["value"])
bark_on_startup = bool(int(config_root.find("bark").attrib["value"]))
activity_text = config_root.find('activity').attrib['value']

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')
    print(discord.utils.get(client.guilds))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=activity_text))
    guild = client.get_guild(GuildID)
    if bark_on_startup:
        for channel in guild.channels:
            if channel.name == "général" and type(channel) == discord.channel.TextChannel:
                await channel.send(config_root.find("bark").attrib["bark_message"])


@client.event
async def on_message(message):
    text = message.content.lower()
    if text.startswith("\\"):
        command = text.split()[0]\
            .strip("\\")
    else:
        command = None
    if command is not None:
        try:
            attributes = commands_root.find(command).attrib
            func = eval(attributes['exec'])
            if attributes['args'] != '':
                args = attributes['args']
            else:
                args = None
            if args is not None:
                to_send = func(args)
            else:
                to_send = func()
            await message.channel.send(to_send)
            await message.delete()

        except AttributeError:
            await message.channel.send("Mauvaise commande")


# -------------------Commands----------------------

def info():
    text = "Besoin d'aide?\nVoici mes commandes : \n"
    for command in commands_root:
        text = f'{text}\n\\{command.tag} : {command.attrib["about"]}'
    return text


def get_gif_from_list(arg):
    lst = eval(arg)
    return choice(lst)



client.run(TOKEN)
