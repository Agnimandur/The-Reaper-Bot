import os
from discord_components import Button, ButtonStyle, Select, SelectOption, ComponentsBot, ActionRow
from params import Params
from reap import Reap
import discord

from mongoengine import *

bot = ComponentsBot("$",case_insensitive=True,intents=discord.Intents.all(),activity=discord.Game(name="Reaper"))

bot.author_id = 880558753064300545
INVITE = "https://discord.com/api/oauth2/authorize?client_id=965828385454563418&permissions=1237219404913&scope=bot"



@bot.event 
async def on_ready():
    print("I'm in")
    print(bot.user)
    connect(host=os.environ.get("MONGO_CONNECT"))



@bot.event
async def on_guild_join(guild):
    cat = await guild.create_category('Reaper')
    commands = await cat.create_text_channel('reap')
    await cat.create_text_channel('reap-discussion',slowmode_delay=1)
    role = await guild.create_role(name='reaper-admin')
    await guild.me.add_roles(role)

    server = Params(guild=guild.id,role=role.id)
    server.save()

    reap = Button(style=ButtonStyle.blue, custom_id="reap",label="REAP",emoji=bot.get_emoji(966044448653987911))
    nextreap = Button(style=ButtonStyle.blue, custom_id="nextreap",label="Nextreap",emoji=bot.get_emoji(971317210817626192))
    value = Button(style=ButtonStyle.blue, custom_id="value",label="Value",emoji=bot.get_emoji(971309692934557726))
    rank = Button(style=ButtonStyle.blue, custom_id="rank",label="Rank",emoji=bot.get_emoji(971281534923440148))
    begin = Button(style=ButtonStyle.green, custom_id="begin",label="Begin Game",emoji=bot.get_emoji(971311236392296488))
    end = Button(style=ButtonStyle.red, custom_id="end",label="End Game",emoji=bot.get_emoji(971284461356470292))
    server = Button(style=ButtonStyle.URL, custom_id="server",label="Reaper Public Server",url="https://discord.gg/9A5QVzQc8X")
    invite = Button(style=ButtonStyle.URL, custom_id="invite",label="Permanent Invite Link",url=INVITE)
    await commands.send(components=[reap])
    await commands.send(components=ActionRow([nextreap,value,rank]))
    await commands.send(components=ActionRow([begin,end]))
    await commands.send(components=ActionRow([server,invite]))

@bot.event
async def on_guild_remove(guild):
    server = Params.objects.get(guild=guild.id)
    server.delete()
    try:
        game = Reap.objects.get(guild=guild.id)
        game.delete()
    except: pass

@bot.event
async def on_member_remove(member):
    try:
        game = Reap.objects.get(guild=member.guild.id)
        game.removePlayer(str(member.id))
        game.save()
    except: pass



extensions = ['cogs.developer','cogs.error','cogs.admin','cogs.player','cogs.servermod','cogs.randomstuff']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

bot.run(os.environ.get("DISCORD_BOT_SECRET"))