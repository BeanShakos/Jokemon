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

@client.event
async def on_message(message):
    if (((len(message.attachments) > 0 and message.attachments[0].filename[-5:].split('.')[-1] in validFileTypes) or (uri_validator(message.content) and str(message.content).split('?',1)[0][-7:].split('.')[-1] in validFileTypes)) and message.author.id != JOKEMON_BOT_ID and message.channel.id == JOKEMON_CHANNEL_ID):
        await message.channel.send("New Joe submission from {}".format(message.author.mention))
    elif (message.author.id == JOKEMON_BOT_ID or message.channel.id != JOKEMON_CHANNEL_ID):
        pass
    else:
        t = await message.channel.send("Invalid submission {}".format(message.author.mention))
        await asyncio.sleep(3)
        await message.delete()
        await t.delete()

client.run(os.getenv('BOT_TOKEN'))