import discord, asyncio, random, os, json
from pymongo import MongoClient
from discord.ext import commands
from urllib.parse import urlparse

mongo = MongoClient("mongodb+srv://thomas:{DB_PASSWORD}@cluster0.640kn.mongodb.net/jokemon?retryWrites=true&w=majority".format(DB_PASSWORD=os.getenv("DB_PASSWORD")))
db = mongo.jokemon

JOKEMON_CHANNEL_ID = 762323041543258112
JOKEMON_BOT_ID = 722602188417007673

rarity = [
    {
        "title":"Joesus Christ",
        "color":0
    },
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
    0.0001,
    0.0499,
    0.1, 
    0.15,
    0.3,
    0.4 
]

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

validFileTypes = ['png','jpg','jpeg','gif']

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
        new_jokemon = {
            "title": joe_name.content.title(),
            "rarity": stats,
            "image_url": url
        }
        result = db.jokemon.insert_one(new_jokemon)
        await message.author.send("New Joe added!")

async def get_joe_name(message,t ):
    joe_name = await client.wait_for('message', check=lambda message: message.author == t, timeout=30)
    if ("joe" in joe_name.content.lower()):
        return joe_name
    else:
        await message.author.send("Invalid Joe name. Please try again.")
        joe_name = await get_joe_name(message, t)
        return joe_name
    #await message.author.send("No response or error. Scrapping this joe :(")

@client.command(aliases=['unbox'])
async def lootbox(ctx):
    embed = discord.Embed(
        title = "Unboxing New Joe...",
        colour = 16711792,
    )
    embed.set_author(name="@{name}".format(name=ctx.message.author.name))
    embed.set_image(url="https://media.discordapp.net/attachments/647626975011405835/762411097705152522/joes.gif?width=676&height=676")
    t = await ctx.channel.send(embed=embed)
    query = random.choices(population=rarity, weights=rarity_weights, k=1)[0]
    options = []
    joes = db.jokemon.find({"rarity":{"title":query["title"],"color":query["color"]}})
    for joe in joes:
        options.append(joe)
    newJoe = random.choice(options)
    embed = discord.Embed(
        title = newJoe['title'],
        colour = newJoe['rarity']['color'],
    )
    embed.set_author(name="@{name} - You got a new Joe!".format(name=ctx.message.author.name))
    embed.set_footer(text=newJoe['rarity']["title"])
    embed.set_image(url=newJoe['image_url'])
    await asyncio.sleep(5)
    await t.edit(embed=embed)

@client.command(aliases=['joes'])
async def fetch(ctx):
    t = await ctx.send("Fetching Joes...")
    joes = db.jokemon.find()
    joesus = ''
    mythic = ''
    legendary = ''
    rare = ''
    special = ''
    fundamental = ''
    for joe in joes:
        if joe['rarity']['title'] == 'Mythic':
            mythic += '- ' + joe['title'] + '\n'
        elif joe['rarity']['title'] == 'Legendary':
            legendary += '- ' + joe['title'] + '\n'
        elif joe['rarity']['title'] == 'Rare':
            rare += '- ' + joe['title'] + '\n'
        elif joe['rarity']['title'] == 'Special':
            special += '- ' + joe['title'] + '\n'
        elif joe['rarity']['title'] == 'Fundamental':
            fundamental += '- ' + joe['title'] + '\n'
        elif joe['rarity']['title'] == 'Joesus Christ':
            joesus += '- ' + '?'*len(joe['title'].split(' ')[0]) + ' ' + joe['title'].split(' ')[1] + '\n'

    text = '''```Joesus Christ:
{JOESUS_JOES}
Mythic:
{MYTHIC_JOES}
Legendary:
{LEGENDARY_JOES}
Rare:
{RARE_JOES}
Special:
{SPECIAL_JOES}
Fundamental:
{FUNDAMENTAL_JOES}
```'''.format(JOESUS_JOES=joesus,MYTHIC_JOES=mythic,LEGENDARY_JOES=legendary,RARE_JOES=rare,SPECIAL_JOES=special,FUNDAMENTAL_JOES=fundamental)
    await t.edit(content=text)

@client.event
async def on_message(message):
    if (((len(message.attachments) > 0 and message.attachments[0].filename[-5:].split('.')[-1].lower() in validFileTypes) or (uri_validator(message.content) and str(message.content).split('?',1)[0][-7:].split('.')[-1].lower() in validFileTypes)) and message.author.id != JOKEMON_BOT_ID and message.channel.id == JOKEMON_CHANNEL_ID):
        if len(message.attachments) > 0:
            url = message.attachments[0].url
        else:
            url = message.content
        await message.delete()
        await add_joe(message, url)

    elif (message.author.id == JOKEMON_BOT_ID or message.channel.id != JOKEMON_CHANNEL_ID):
        await client.process_commands(message)
    else:
        t = await message.channel.send("Invalid submission {}".format(message.author.mention))
        await asyncio.sleep(3)
        await message.delete()
        await t.delete()

@client.event
async def on_ready():
    print("Ready")

client.run(str(os.getenv("DISCORD_TOKEN")))