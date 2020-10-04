import discord, asyncio, random
from discord.ext import commands

songs = ["banakula.mp3", "com.mp3"]

joe_srcs = [
    ["https://images-ext-1.discordapp.net/external/O9RxXwXY8q_RVZNlyOnRMgFnaAEFDWN6d_SPv-lFUic/%3Fwidth%3D312%26height%3D676/https/media.discordapp.net/attachments/696261211829829676/762163831383916554/image0.jpg","Safety Joe"],
    ["https://media.discordapp.net/attachments/696261211829829676/762167703267311616/image0.png?width=369&height=676","Lightskin Joe"],
    ["https://images-ext-1.discordapp.net/external/Qfx42uw3LQdqvle5cOud9JSjsgDQi-BksoeEvMj_sqs/%3Fwidth%3D329%26height%3D676/https/media.discordapp.net/attachments/696261211829829676/762163831648026635/image1.jpg","Cool Joe"],
    ["https://images-ext-2.discordapp.net/external/WN9SxxT7-OLRM6IbnoaeP6_UDL5SlAFf46nuY9Js3g4/%3Fwidth%3D507%26height%3D675/https/media.discordapp.net/attachments/696261211829829676/762163976141930526/image0.jpg","Hood Joe"],
    ["https://media.discordapp.net/attachments/696261211829829676/762166555479638027/image0.jpg?width=507&height=676","Snake Joe"],
    ["https://images-ext-1.discordapp.net/external/HUUcQbkMx2hb3HHFdGC6BKwnysqCVTAF9jocijHW8sA/https/images-ext-1.discordapp.net/external/1rrGEIZMK4m9K3ORRFa5aDoxKOPGPjVIf6zOnkE9zC8/https/media.discordapp.net/attachments/696261211829829676/753999039930040390/unknown.png","Sleepy Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762168229699256351/lol_2.PNG","Happy Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762168401770315796/Snapchat-321023290.jpg?width=380&height=676","Folded Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762168539141505044/unknown-3.png","Strong Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762168636554215434/83D6C3E9-9ADC-4228-B20D-7377C93601C7.JPG?width=480&height=675","Chad Joe"],
    ["https://cdn.discordapp.com/attachments/762167797346205707/762168669563650099/video0.mov","Fire Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762168736899137576/unknown.png?width=960&height=540","Sexy Mama Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762169095981891644/image0.png?width=312&height=675","Trippin Joe (Ft. Spaceman)"],
    ["https://media.discordapp.net/attachments/762167797346205707/762169281768980480/image0.png?width=697&height=676","Baby Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762169447367704586/image0.png?width=312&height=675","Chef Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762169585201709066/image0.png?width=489&height=676","Chillin Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762169989607194645/Snapchat-1051403639.jpg?width=960&height=488","Beach Episode Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762170025594585088/38DyP8AXeVvyt4DZqEAAAAASUVORK5CYII.png?width=329&height=676","Cursed Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762170075456471040/Snapchat-402471993.jpg?width=506&height=676","Shoota Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762170190883979284/betterjoe.gif","Dancing Joe"],
    ["https://media.discordapp.net/attachments/384046473991684099/746271387664121879/image0.jpg?width=380&height=676","Undie Joes"],
    ["https://media.discordapp.net/attachments/758877710213709866/758881630092918816/image0.jpg?width=380&height=676","Boku No Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762170766237368380/image0.png?width=380&height=676","Bald Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171017857728542/image0.png","Noir Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171049591963659/image0.png?width=312&height=675","Fresh Cut Joe (Ft. Priya/Mr. Thachet)"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171073432125450/image0.png","Shredded Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171091481264148/image0.png?width=474&height=676","Banana Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171220417708032/kliLugYFL7y392A7hZKTbgWF-Am1_mxDJtXjjAnjIBI_EBLKK1p3i40go-rDUXs9wubfr-y2xQg1qNKwY-QcPm6PtMQjkAxvK1DL.png?width=329&height=676","Sophomore Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171264927399947/Wcun3HkBwavMFblCFYseT-Ke7qR_mFULVmhSQdAnwYmdk9T6G-cK5e5PyoHgiMw1w57-nO6vDG7dCfRLEptn_sA4cV1sRYHMe2JN.png?width=507&height=676","Pog Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171470544764968/20200911_215429.jpg?width=960&height=467","Horizontal Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171554523512832/20200911_215004.jpg?width=960&height=467","Vertical Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171610018218020/unknown.png","Father Joe (Ft. Mother Aiden)"],
    ["https://cdn.discordapp.com/attachments/762167797346205707/762171698157322260/video0.mov","TikTok Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762171974004768788/Mywv9gAAAAASUVORK5CYII.png?width=480&height=675","Inverted Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762172114022563850/unknown.png","Shlumped Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762172275952189450/unknown.png","Paint Brush Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762172929953366046/Snapchat-1066108102.jpg?width=343&height=676","Swimsuit Joe"],
    ["https://media.discordapp.net/attachments/762167797346205707/762173066545201162/vbRgPZza-DbqRlzieg9R2iROZBi2ClH4Dx9NprAbm35-wT20rh9Js03GKpk1CxZHCG3x6OYi4ntxtLsNfLoqQMjixYCUxG-jaSZB.png","Muslim Joe"]
]

client = commands.Bot(command_prefix = '.')

# @client.command(pass_context=True)
# async def leave(ctx):
#     server = ctx.message.guild
#     voice = server.voice_client
#     esci = voice.disconnect()
#     test = asyncio.run_coroutine_threadsafe(esci, client.loop)
#     print(test.result())

# @client.event
# async def on_voice_state_update(member, before, after):
#     if(str(member.id) == "722602188417007673"):
#         pass
#     elif(str(member.id) == "284112758000320512"):
#         joeFound = False
#         if after.channel:
#             for member in after.channel.members:
#                 if (str(member.id) == "284112758000320512"):
#                     joeFound = True
        
#         if(joeFound == True):
#             def my_after(error):
#                 coro = vc.disconnect(force=True)
#                 fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
#                 try:
#                     fut.result()
#                 except:
#                     pass
#             vc = await after.channel.connect()
#             print("JOE HYPE")
#             vc.play(discord.FFmpegPCMAudio("com.mp3"), after=my_after)
#         else:
#             pass

@client.event
async def on_message(message):
    if ("joe" in message.content.lower() and message.author.id != 722602188417007673):
        temp = random.choice(joe_srcs)
        await message.channel.send("{name} says {greeting}!".format(name=temp[1],greeting=random.choice(['hi','hello','hey','what\'s up','what\'s good','long time no see','what\'s cookin good lookin','yo','howdy','sup','whazzup'])))
        await message.channel.send("{link}".format(link=temp[0]))

client.run("NzIyNjAyMTg4NDE3MDA3Njcz.XuldzQ.jIylnbE_oxszNwz4tIK-QGiT8Wc")