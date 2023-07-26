import discord
from discord.ext import commands
import os
import confuse
import asyncio

class redeem(commands.Cog):
	def __init__(self, bot):
		self.bot=bot
		current_dir = os.path.dirname(os.path.abspath(__file__))
		# Construct the absolute path to artifacts.yaml
		config_path = os.path.join(current_dir, '../artifacts.yaml')
		#Establish a way of reading the config file.
		self.itemfile = confuse.Configuration('FictionalAppLol')
		self.itemfile.set_file(config_path)

	@commands.command(name='redeem')
	@commands.dm_only()
	async def redeem(self,ctx,*,item):
		#if item name in Artifacts list.
		if item in self.itemfile['Artifacts'].get():
			#get artifact data.
			artinfo = self.itemfile[item].get()
			#if item arg lowered is equal to identifier, prompt user.
			if item.lower() == artinfo['identifier']:
				await ctx.send("Enter redeem key!")

				try:
					key = await self.bot.wait_for('message',check=lambda x: x.author == ctx.author and x.channel == ctx.channel,timeout=20.0)

				except asyncio.TimeoutError:
					await ctx.reply("Timed out!")

				else:
					if key.content.lower() == artinfo['verify']:
						#simulate verification.
						async with ctx.channel.typing():
							await asyncio.sleep(3)

						await key.reply("Success! The item has been claimed succesfully; its effects will be made visible soon!")
						infoembed = discord.Embed(title=f"Artifact claimed", description=f"Artifact ID: {item} was claimed by user '{ctx.author.name}'",color=discord.Color.blue())
						await self.bot.get_user(self.bot.owner_id).send(embed=infoembed)
					else:
						async with ctx.channel.typing():
							await asyncio.sleep(3)
						await key.reply("Incorrect key given!")



	@redeem.error
	async def handleredeemerror(self,ctx,error):
		if isinstance(error, commands.PrivateMessageOnly):
			await ctx.reply("This command can only be used in DMs. To wipe sensitive information, your message was deleted.")
			await ctx.message.delete()
		else:
			em = discord.Embed(title="Uknown Error Encountered.",description=f"Error checks: \n```Error check: commands.PrivateMessageOnly FAILED.```\n Could not perform auto-correction. \nOutput log: ```{error}```.",color=discord.Color.red())
			em.set_footer(text="Inform the owner of this error if possible along with context on what actions led to it.")
			await ctx.send(embed=em)
			print(error)


