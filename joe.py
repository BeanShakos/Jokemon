import discord, asyncio, random, os
from discord.ext import commands
from urllib.parse import urlparse

JOKEMON_CHANNEL_ID = 762323041543258112
JOKEMON_BOT_ID = 722602188417007673

rarity = [
    {
        "title":"Mythic",
        "color": 15401215
    },
    {
        "title":"Legendary",
        "color": 5375
    },
    {
        "title":"Rare",
        "color": 16711680
    },
    {
        "title":"Special",
        "color": 65321
    },
    {
        "title":"Fundamental",
        "color": 5127936
    },
]

rarity_weights = [
    0.05, # 5%
    0.1,  # 10%
    0.15, # 15%
    0.3,  # 30%
    0.4   # 40%
]

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
        stats = random.choices(population=rarity, weights=rarity_weights, k=1)[0]
        embed = discord.Embed(
            title = joe_name.content.title(),
            colour = stats["color"],
        )
        embed.set_footer(text=stats["title"])
        embed.set_image(url=url)
        await message.author.send(embed=embed)

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

client.run("NzIyNjAyMTg4NDE3MDA3Njcz.Xulduw.db1lqNY9NOLUgz0n_PBdr2yNdC8")