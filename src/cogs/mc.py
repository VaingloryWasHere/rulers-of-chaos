import httpx
import asyncio
import discord
from discord.ext import	commands
from discord import app_commands
from discord.ext import tasks, commands
import asyncpg

guild = discord.Object(id=1124865430134202468)

#actual server
class server:
	def __init__(self):
		self.online = False
		self.players = 0
		self.playerlist = []
		self.update_status()

	@staticmethod
	async def background_update(serv):
		serv.update_status()
		print("status updated!")
		await asyncio.sleep(2)


	def update_status(self):
		url = 'https://eu.mc-api.net/v3/server/ping/77.68.126.40:19200'
		try:
			response = httpx.get(url)
			#if status code fine!
			if response.status_code == 200:
				data = response.json()  # Use .json() method to parse the response content

				if data.get('online', False): #if online.
					playerdata = data.get('players', {})
					players = playerdata['online']
					self.online=True
					self.players = players
					self.playerlist = playerdata['sample']
				else: #if  not online.
					self.online = False
			else: #strange response code given.
				print(f"Failed to get server status. HTTP status code: {response.status_code}")
		
		except httpx.RequestError as e:
			print(f"Error occurred while making the request: {e}")

	async def loop(self):
		while True:
			print("server loop called.")
			await self.update_status()
			await asyncio.sleep(60)

#cog containing related commands.
class mcserver(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.server = bot.server
		self.background_update.add_exception_type(asyncpg.PostgresConnectionError)
		self.background_update.start()

	@commands.hybrid_command(name='status', with_app_command=True, description="Fetch the minecraft server's status.")
	@app_commands.guilds(guild)
	async def status(self, ctx):
		#server attribute instantised on on_ready()
		server = self.server
		server.update_status()
		embed = discord.Embed(title=f"Server status: rulersofchaos.mcpe.lol:19200",description=f"Online: {server.online}\nPlayers: {server.players} \nPlayer list: ",color=discord.Color.red())
		for playerinfo in server.playerlist:
			embed.add_field(name=f"Name: {playerinfo['name']}", value=f"ID:{playerinfo['id']}")
		await ctx.send(embed=embed)
		return

	@tasks.loop(seconds=60.0)
	async def background_update(self):
		self.server.update_status()
		print("Updated!")

	@background_update.before_loop
	async def before_printer(self):
		print('waiting for bot to get ready before starting loop...')
		await self.bot.wait_until_ready()
		print("Task ready!")


	@commands.command()
	async def sync(self, ctx: commands.Context):
		await self.bot.tree.sync(guild = discord.Object(id=1124865430134202468))
