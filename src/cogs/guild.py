import discord
from discord import app_commands
from discord.ext import commands



#The front-end...
class Reception(commands.Cog):
	def __init__(self):
		pass

	#accepting a given mission..
	@commands.command(name='accept')
	async def acceptmission(self,ctx,*,missionName):
		if 'real' and 'available' in Manager.queryMission(missionName):
			Manager.assignMission(missionName,ctx.author.name)
			await ctx.send("Success! You have " + Manager.getDeadline(missionName) + " days to complete your mission!")
		else:
			await ctx.send("That mission is either not real or already taken by someone else!")

	@commands.command(name='check')
	async def checkmissions(self,ctx,missionName):
		infoembed = Manager.missionEmbed(missionName)
		await ctx.send(embed=infoembed)

	@commands.command(name='submit')
	async def submitmission(self,ctx,missionName):
		if Manager.checkReal(missionName) == False:
			await ctx.send("That mission does not exist!")
			return

		if Manager.checkClaimed(missionName,ctx.author.name) == True:
			await Manager.review(missionName)
			await ctx.send("Added to the queue! A guild representative will verify your mission's progress as soon as possible.")
			queueEm = discord.Embed(title=f"Mission Review.",description=f"Player Name: {ctx.author.name}\nPlayer ID: {ctx.author.id}\nSubmitted Mission Name: {missionName}.\nSubmitted Mission ID: {Manager.getID(missionName)}",color=discord.Color.blue())
		
		else:
			await ctx.send("This mission is claimed by someone else!")

#Below are the guild-representative only-s.

	@commands.command(name='reward',description="Confirms a mission to be done and awards the player.")
	@commands.dm_only()
	@commands.is_owner()
	async def confirmMission(self,missionID):
		#returns an embed to send, different from giveAP in that AP amt is auto-determined along with userID. AP is awarded automatically.
		awardem = Manager.missionDone(missionID)
		await bot.get_user(userid).send(embed=awardem)
		await ctx.send("Success! Player has been awarded!")
		
	@confirmMission.error
	async def handleconfirmerror(self,ctx,error):
		if isinstance(error, commands.PrivateMessageOnly):
			await ctx.reply("This command can only be used in DMs. To wipe sensitive information, your message was deleted.")
			await ctx.message.delete()
		else:
			em = discord.Embed(title="Uknown Error Encountered.",description=f"Error checks: \n```Error check: commands.PrivateMessageOnly FAILED.```\n Could not perform auto-correction. \nOutput log: ```{error}```.",color=discord.Color.red())
			await ctx.send(embed=em)