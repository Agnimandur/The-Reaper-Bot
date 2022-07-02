import discord
from discord.ext import tasks, commands
from reap import Reap
from params import Params
from mongoengine import *
from time import time
from leaderboard import leaderboardEmbed

class AdminCommands(commands.Cog, name='Reaper Admin Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        reaperadmin = ctx.guild.get_role(Params.objects.get(guild=ctx.guild.id).role)
        return ctx.channel.category!=None and ctx.channel.category.name == 'Reaper' and (not ctx.author.bot) and (ctx.author.id == self.bot.author_id or ctx.author.guild_permissions.manage_guild or reaperadmin in ctx.author.roles)


    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        canClick = await self.cog_check(interaction)
        if not canClick: return
        g = interaction.guild_id
        a = str(interaction.author.id)
        if interaction.custom_id == 'begin':
            res = await self.begingame(g)
            await interaction.send(res)
        elif interaction.custom_id == 'end':
            res = await self.endgame(g)
            await interaction.send(res)
    
    #Is there an ongoing game in guild "g"?
    def activeGame(self,g):
        try:
            game = Reap.objects.get(guild=g)
            return game
        except:
            return None

    @commands.command(name='begin',help='Begin the game. c=cooldown, p=point target.\nIf no parameter is provided, it uses the default from $parameters (8 hour reap times, first to a million points, night reaping enabled).\nExample: $begin c=80m p=8h would start a game with a cooldown of 80 minutes and a point target of 8 hours.')
    async def begingameCommand(self, ctx, *args):
        res = await self.begingame(ctx.guild.id,**self.parseArgs(args))
        await ctx.reply(res)

    async def begingame(self, g, **kwargs):
        def to_second(x):
            if x.isdigit(): return int(x)
            mul = {'s':1,'m':60,'h':3600,'d':86400}
            return mul[x[-1]]*int(x[:-1])
        
        if self.activeGame(g):
            return "Game in progress!"
        else:
            guild = self.bot.get_guild(g)
            reap = discord.utils.get(guild.channels,name='reap')
            
            server = Params.objects.get(guild=g)
            c = to_second(kwargs['c']) if 'c' in kwargs else server.cooldown
            p = to_second(kwargs['p']) if 'p' in kwargs else server.target

            msg = await reap.send(embed=leaderboardEmbed(guild,c,p))
            game = Reap(cooldown=c,target=p,guild=g,last=time(),channel=reap.id,board=msg.id)
            game.save()
            return "The game has begun!"

    @commands.command(name='end',help='Manually terminate the game.')
    async def endgameCommand(self,ctx):
        res = await self.endgame(ctx.guild.id)
        await ctx.reply(res)
    
    async def endgame(self, g):
        game = self.activeGame(g)
        if game==None:
            return "No active game."
        else:
            reap = await self.bot.fetch_channel(game.channel)
            msg = await reap.fetch_message(game.board)
            await msg.delete()
            game.delete()
            return "Game ended."

    def parseArgs(self,args):
        kwargs = {}
        for arg in args:
            i = arg.index('=')
            kwargs[arg[:i]] = arg[i+1:]
        return kwargs

    @commands.command(name='parameters',help='Set the default game parameters (this does NOT affect the ongoing game).\nExample: $parameters c=80m p=250000 n=False tz=-8\nc=_ (cooldown for the game, default is 12h)\np=_ (point target for the game, default is 1000000)\nn=[True or False] (night reaps are enabled by default)\ntz=_ (the timezone of the server in UTC (default is 0, EST is -5, PST is -8, etc)')
    async def parameters(self,ctx,*args):
        try:
            server = Params.objects.get(guild=ctx.guild.id)

            server.edit(**self.parseArgs(args))
            server.save()
            await ctx.reply(str(server))
        except Exception as err:
            await ctx.reply(f"{str(err)}\nTry `$help parameters`.")

def setup(bot):
    bot.add_cog(AdminCommands(bot))