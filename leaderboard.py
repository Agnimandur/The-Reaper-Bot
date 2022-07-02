from reap import Reap
import discord
from datetime import timedelta

"""
WHEN CREATING A GAME: guild (object), cooldown (int), point target (int)
REAP IS MADE (UPDATE LEADERBOARD): guild (object)
"""
def leaderboardEmbed(*args):
    guild = args[0]
    if len(args)==3:
        board = []
        cool = timedelta(seconds=args[1])
        target = args[2]
        lastReap = "*None Yet*"
    else:
        game = Reap.objects.get(guild=guild.id)
        board = game.leaderboard()
        cool = timedelta(seconds=game.cooldown)
        target = game.target
        lastReap = f"<t:{game.last}>"
    emb = discord.Embed(color=0x71368a,title="**Leaderboard**",description=f"Reap Cooldown: {cool}\nPoint Target: {target}\nLast Reap: {lastReap}\n[Invite Me](https://discord.com/api/oauth2/authorize?client_id=965828385454563418&permissions=1237219404913&scope=bot) | [Join the Discord](https://discord.gg/9A5QVzQc8X) | [Github](https://github.com/Agnimandur/The-Reaper-Bot) | Vote on Top.gg").set_author(name='Reaper',url='https://artofproblemsolving.com/wiki/index.php/Reaper',icon_url='https://i.ibb.co/Y7PX3cG/scythe.png').set_footer(text="Made by Agnimandur#9256",icon_url="https://i.ibb.co/9sxH8GN/sorin.webp").add_field(name="**Rank**",value="`1.`\n`2.`\n`3.`\n`4.`\n`5.`\n",inline=True)
    names,points = "",""
    index = 1
    for p,user in board:
        member = guild.get_member(int(user))
        names += f"`{member.name}#{member.discriminator}`\n"
        points += f"`{p}`\n"
        index += 1
        if index==6: break
    if names=='':
        return emb
    return emb.add_field(name="**Players**",value=names,inline=True).add_field(name="**Points**",value=points,inline=True)
