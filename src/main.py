import discord
from discord.ext import commands
from cogs.redeem import redeem
import confuse
from cogs.mc import server, mcserver
import asyncio
#instan..?? da server

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
bot.owner_id = 718710286596702220


@bot.event
async def on_ready():
	bot.server = server()
	#register cogs.
	await bot.add_cog(redeem(bot))
	await bot.add_cog(mcserver(bot))
	print("logged in.")



tokenfile = confuse.Configuration('FictionalAppLol')
tokenfile.set_file('../token.yaml')

bot.run(token=tokenfile['Token'].get())