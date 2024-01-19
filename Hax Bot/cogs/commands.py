import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Bot Commands
    @commands.command()
    @commands.has_role('Cosmonaut')
    async def help(self, ctx):
        embed=discord.Embed(title="Command List", color=0x800080)

        embed.add_field(name="***help**", value="Returns this help message.", inline=False)
        embed.add_field(name="***ping**", value="Returns the bot's latency in ms.", inline=False)
        """embed.add_field(name="***togglekick**", value=f"A setting used for kicking multiple members from the guild.\
                                                   If a guild member gets kicked/leaves while this is on, it will send them a message saying\
                                                   they've been kicked from the guild and all of their roles will be removed.", inline=False)"""
        embed.add_field(name="***accept**", value="Sends a message informing the applicant that their application to the guild has been accepted.\
                                               Only use this command in the ticket channel.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role('Cosmonaut')
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{int(round(self.bot.latency, 3) * 1000)} ms`')

    """@commands.command()
    @commands.has_role('Cosmonaut')
    async def togglekick(self, ctx):

        if self.bot.kick_status == True:
            self.bot.kick_status = False
            await ctx.send('Kick message is now **off**')
        else:
            self.bot.kick_status = True
            await ctx.send('Kick message is now **on**')"""

    @commands.command()
    @commands.has_role('Cosmonaut')
    async def accept(self, ctx):
        await ctx.message.delete()

        for member in ctx.channel.members:
            # check to make sure the member doesn't have chief and bot role
            if (self.bot.chief_role not in member.roles) and (self.bot.manager_role not in member.roles) and (self.bot.bot_role not in member.roles):
                await ctx.send(f"Your application has been accepted! Whenever you're available,\
please message a recruiter+ ingame to get a invite to the guild. \
https://www.wynndata.tk/stats/guild/HackForums {member.mention}")
                break
    
    @commands.command()
    @commands.has_role('Cosmonaut')
    async def test(self, ctx):
        try:
            msg = await self.bot.test_channel.fetch_message(800825510862258197)
            print(msg)
            await msg.delete()
        except discord.errors.NotFound:
            print('ERROR')

def setup(bot):
    bot.add_cog(Commands(bot))