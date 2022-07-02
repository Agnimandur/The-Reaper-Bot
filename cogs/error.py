from discord.ext import commands

class ErrorHandler(commands.Cog):
	"""A cog for global error handling."""

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound) or ctx.channel.category.name != 'Reaper':
			return
		elif isinstance(error, commands.CommandOnCooldown):
			message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
		elif isinstance(error, commands.MissingPermissions):
			message = "You are missing the required permissions to run this command!"
		elif isinstance(error, commands.UserInputError):
			message = "Something about your input was wrong, please check your input and try again!"
		else:
			message = str(error)

		await ctx.reply(message) #don't delete error messsage


def setup(bot):
	bot.add_cog(ErrorHandler(bot))