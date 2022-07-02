import discord
from discord.ext import tasks, commands
from discord_components import Button, ButtonStyle, Select, SelectOption, ComponentsBot, ActionRow
from params import Params
from mongoengine import *

class ServerModCommands(commands.Cog, name='Server Mod Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.channel.category.name == 'Reaper' and (not ctx.author.bot) and (ctx.author.id == self.bot.author_id or ctx.author.guild_permissions.manage_guild)

    @commands.command(name='adminify',help='Toggle the reaper-admin role on a list of mentioned users.')
    async def adminify(self,ctx):
        reaperadmin = ctx.guild.get_role(Params.objects.get(guild=ctx.guild.id).role)
        if len(ctx.message.mentions)==0:
            trb = discord.utils.get(ctx.guild.roles,name='The Reaper Bot')
            await ctx.reply(f"reaper-admin role has position {reaperadmin.position}. This needs to be lower than {trb.position} for the bot to work!")
            #await ctx.reply('No members mentioned.')
            return
        for person in ctx.message.mentions:
            if reaperadmin in person.roles:
                await person.remove_roles(reaperadmin)
            else:
                await person.add_roles(reaperadmin)
        await ctx.reply('Adminify successful!')

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.custom_id=='kick' and interaction.author.guild_permissions.manage_guild:
            cat = interaction.channel.category
            channels = [c for c in interaction.guild.channels if c.category==cat]
            for c in channels:
                await c.delete()
            reaperadmin = interaction.guild.get_role(Params.objects.get(guild=interaction.guild.id).role)
            await reaperadmin.delete()
            await cat.delete()
            await interaction.guild.leave()
    
    @commands.command(name='kick',help='Kick the reaper bot from your server cleanly.')
    async def kick(self,ctx):
        kick = Button(style=ButtonStyle.red, custom_id="kick",label="Yes",emoji=self.bot.get_emoji(971906600170315787))
        await ctx.send('Are you sure you want to kick The Reaper Bot from this server?',components=[kick], delete_after = 5)


def setup(bot):
    bot.add_cog(ServerModCommands(bot))