import discord
from discord.ext import tasks, commands
from reap import Reap
from mongoengine import *
import datetime
from leaderboard import leaderboardEmbed

class PlayerCommands(commands.Cog, name='Player Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  
        return ctx.channel.category!=None and ctx.channel.category.name == 'Reaper' and (not ctx.author.bot)


    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        canClick = await self.cog_check(interaction)
        if not canClick: return
        g = interaction.guild_id
        a = str(interaction.author.id)
        if interaction.custom_id == 'reap':
            res = await self.reap(g,a)
            await interaction.send(res)
        elif interaction.custom_id == 'nextreap':
            await interaction.send(self.nextreap(g,a))
        elif interaction.custom_id == 'value':
            await interaction.send(self.value(g))
        elif interaction.custom_id == 'rank':
            await interaction.send(self.rank(g,a))
    
    #Is there an ongoing game in guild "g"?
    def activeGame(self,g):
        try:
            game = Reap.objects.get(guild=g)
            return game
        except:
            return None

    @commands.command(name='reap')
    async def reapCommand(self,ctx):
        res = await self.reap(ctx.guild.id,str(ctx.author.id))
        await ctx.send(res)

    async def reap(self,g,user):
        game = self.activeGame(g)
        if game==None:
            return "No active game."
        else:
            oldPoints = game.get_data(user,'p')
            m = game.reap(user)
            game.save()

            guild = self.bot.get_guild(g)
            reap = guild.get_channel(game.channel)
            msg = await reap.fetch_message(game.board)
            dis = discord.utils.get(guild.channels,name='reap-discussion')

            if m != 'WIN' and m >= 6:
                await dis.send(f'Wow, <@{user}> just got a {m}x reap{"!"*(m-5)}')

            if m=="WIN":
                await dis.send(f"Congratulations to <@{user}> on winning! The final leaderboard is displayed below.",embed=leaderboardEmbed(guild))
                await msg.delete()
                game.delete()
                return "You win!"
            elif m > 0:
                await msg.edit(embed=leaderboardEmbed(guild))
                return f"You just got {game.get_data(user,'p') - oldPoints} points from a {m}x reap! You now have {game.get_data(user,'p')} points."
            else:
                return f"Your reap is still on cooldown for {datetime.timedelta(seconds=game.nextreap(user))}."

    @commands.command(name='nextreap',help='Time until you can next reap.')
    async def nextreapCommand(self,ctx):
        await ctx.reply(self.nextreap(ctx.guild.id,str(ctx.author.id)))

    def nextreap(self,g,user):
        game = self.activeGame(g)
        if game == None: return "No active game."
        n = game.nextreap(user)
        if n == 0:
            return "You can reap!"
        else:
            return f"Your reap is still on cooldown for {datetime.timedelta(seconds=n)}."

    @commands.command(name='value',help='Value of the current reap')
    async def valueCommand(self,ctx):
        await ctx.reply(self.value(ctx.guild.id))
    
    def value(self,g):
        game = self.activeGame(g)
        if game != None:
            return f"The current reap is worth {game.value()} points."
        else:
            return "No active game."

    @commands.command(name='rank',help='Display your rank')
    async def rankCommand(self,ctx):
        await ctx.reply(self.rank(ctx.guild.id,str(ctx.author.id)))

    @commands.command(name='playerinfo',help='Display info about a player during a game')
    async def playerInfo(self,ctx):
        game = self.activeGame(ctx.guild.id)
        if game == None:
            await ctx.reply('No active game.')
            return
        if len(ctx.message.mentions)==0:
            user = str(ctx.author.id)
        else:
            user = str(ctx.message.mentions[0].id)
        info = game.reap_data(user)
        if info == None:
            await ctx.reply('This person has not reaped.')
        else:
            await ctx.reply(f'This person has made {info[1]} reaps with an average time of {datetime.timedelta(seconds=info[0])} per reap.')
        
    
    
    def rank(self,g,user):
        game = self.activeGame(g)
        if game != None:
            board = game.leaderboard()
            for i in range(len(board)):
                if board[i][1]==user:
                    return f"You have {round(board[i][0])} points. You are ranked {i+1} out of {len(board)} reapers."
            return "You haven't reaped yet!"
        else:
            return "No active game."

    @commands.command(name='faq',help='Display frequently asked questions.')
    @commands.cooldown(rate=1,per=5)
    async def faq(self,ctx):
        f = """__Frequently Asked Questions:__
Q: How does Reaper work?
A: The goal of *Reaper* is to efficiently collect points via reaps. Every time you reap, you gain a number of points equal to the difference (in seconds) between the time of your reap and the time of the last reap. However, your reap has a cooldown, so you need to reap wisely! Reap too early and you won't get many points, but wait for too long and someone else may snipe you.

Q: How do I play?
A: To reap, simply click the REAP button in `#reap`. Additional buttons tell you information about the value of the current reap.

Q: What's the inspiration for *Reaper*?
A: It's based on the game played on the AOPS website here: <https://artofproblemsolving.com/wiki/index.php/Reaper>

Q: Something's not working, where can I get help?
A: Join the reaper public server and post in the `#help` channel.
"""
        await ctx.send(f)

    @commands.command(name='servers',help='The number of servers The Reaper Bot is in.')
    async def servers(self,ctx):
        await ctx.reply(f"I'm in {len(self.bot.guilds)} servers.")

def setup(bot):
    bot.add_cog(PlayerCommands(bot))