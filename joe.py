import discord, asyncio, random, os
from discord.ext import commands
from urllib.parse import urlparse

JOKEMON_CHANNEL_ID = 762323041543258112
JOKEMON_BOT_ID = 722602188417007673

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

validFileTypes = ['png','jpg','mkv','mov','jpeg']

client = commands.Bot(command_prefix = '!')

async def add_joe(message, url):
    await message.author.send("{}".format(url))
    await message.author.send("What's the name of this Joe?")
    t = message.author
    joe_name = await get_joe_name(message, t)
    if joe_name:
        await message.author.send("Creating {}".format(joe_name.content.title()))
    # embed = discord.Embed(
    #     title =  joe_name,
    #     "
    # )

async def get_joe_name(message,t ):
    joe_name = await client.wait_for('message', check=lambda message: message.author == t, timeout=30)
    if ("joe" in joe_name.content.lower()):
        return joe_name
    else:
        await message.author.send("Invalid Joe name. Please try again.")
        joe_name = await get_joe_name(message, t)
        return joe_name
    #await message.author.send("No response or error. Scrapping this joe :(")

@client.event
async def on_message(message):
    if (((len(message.attachments) > 0 and message.attachments[0].filename[-5:].split('.')[-1] in validFileTypes) or (uri_validator(message.content) and str(message.content).split('?',1)[0][-7:].split('.')[-1] in validFileTypes)) and message.author.id != JOKEMON_BOT_ID and message.channel.id == JOKEMON_CHANNEL_ID):
        if len(message.attachments) > 0:
            url = message.attachments[0].url
        else:
            url = message.content
        await message.delete()
        await add_joe(message, url)

    elif (message.author.id == JOKEMON_BOT_ID or message.channel.id != JOKEMON_CHANNEL_ID):
        pass
    else:
        t = await message.channel.send("Invalid submission {}".format(message.author.mention))
        await asyncio.sleep(3)
        await message.delete()
        await t.delete()

client.run("NzIyNjAyMTg4NDE3MDA3Njcz.Xulduw.RpJnEnSfm88R0Mol9VjgY5P8630")