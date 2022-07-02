from discord.ext import commands
from reap import Reap
from mongoengine import *
from time import time
from params import Params
import discord

class DevCommands(commands.Cog, name='Developer Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  
        return ctx.author.id == self.bot.author_id and ctx.channel.category!=None and ctx.channel.category.name == 'Reaper'
    
    @commands.command(name='gamedata')
    async def gamedata(self,ctx):
        try:
            t1 = time()
            r = Reap.objects.get(guild=ctx.guild.id)
            t2 = time()
            await ctx.send(f"{r}\n*Fetched in {round(1000*(t2-t1))}ms*")
        except:
            await ctx.send(f"No game in guild {ctx.guild.id}!")
    
    @commands.command(name='paramdata')
    async def paramdata(self,ctx):
        try:
            t1 = time()
            r = Params.objects.get(guild=ctx.guild.id)
            t2 = time()
            await ctx.send(f"{r}\n*Fetched in {round(1000*(t2-t1))}ms*")
        except Exception as err:
            await ctx.send(str(err))


def setup(bot):
    bot.add_cog(DevCommands(bot))