import discord, requests, time
from discord.ext import commands

"""
on_message(message)
    A discord event function that is called whenever there is a message in the server.
    This is used to check to see if the message is a guild application. This is done by
    checking if the message starts with "ign", and that the message comes from a channel
    under the "apply here" category. Once it gets the app, it sends it to #guild-apps
    and #deleted-apps.

on_guild_channel_create(channel)
    A discord event function that is called whenever a new channel is created. This is
    used to check when a new ticket channel has been created, and send a bot message to
    that channel (informing them about guild information).
"""

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message (self, message):
        guild_roles = [self.bot.recruit_role, self.bot.recruiter_role, self.bot.captain_role, self.bot.chief_role]

        # check to see if message starts with "ign", is in the apply here category and that the person doesn't have any guild roles
        if message.content.lower().startswith('ign') and message.channel.category.id == 632705662010523669 and [i for i in message.author.roles if i in guild_roles] == []:
            text = message.content.split()
            punctuation = r"!()-[]{}\"';:,<>./?@#$%^&*~"

            # change the person's discord name to match the ign they inputed
            if text[0].lower() == 'ign:':
                name = text[1].translate(str.maketrans('', '', punctuation))
                await message.author.edit(nick=name)
            else:
                name = (text[0].replace('IGN:', '')).translate(str.maketrans('', '', punctuation))
                await message.author.edit(nick=name)

            await message.channel.send(f'Thank you for your application {message.author.mention}, we will get back to you shortly.')
            # send app to #guild-apps and #deleted-apps
            app = await self.bot.guild_apps.send(f'{message.content} \n@here')
            await self.bot.deleted_apps.send(f'{message.content}')

            await app.add_reaction('✅')
            await app.add_reaction('❌')

            # add the message id to the file "apps.txt"
            f = open('apps.txt', 'r+')
            apps = f.read()

            if len(apps) == 0:
                apps = {}
            else:
                apps = eval(apps)

            apps[message.author.display_name] = app.id

            f.seek(0)
            f.truncate(0)
            f.write(str(apps))
            f.close()
    
    """@commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        time.sleep(1)
        rules_info = self.bot.get_channel(396145879301619722)

        if channel.category.name == 'apply here':
            new_member = 'User'
            for member in channel.members:
                if (self.bot.chief_role not in member.roles) and (self.bot.bot_role not in member.roles):
                    new_member = member.mention
                    break

            msg = await channel.send(f"Hello {new_member}!\n📢 HackForums is a **warring** guild, and we expect members to complete a war requirement every **2 weeks**.\n\
The requirement is as follows (based on rank):\n\n\
> Recruits - 10 wars\n\
> Recruiters - 25 wars\n\
> Captains - 40 wars\n\n\
Also, be sure to follow any additional rules outlined in {rules_info.mention}.\nClick ✅ if you agree with these terms, or ❌ if you disagree.\n")

            await msg.add_reaction('✅')
            await msg.add_reaction('❌')

            def check(reaction, user):
                return not user.bot

            res = await self.bot.wait_for('reaction_add', check=check)

            if res[0].emoji == '✅':
                await channel.send(f"Awesome, let's continue! Copy the application form below and replace each **X** with your answer.\n\
```IGN: X\n\
Preferred Nickname? X\n\
Highest Level Class (min lvl 75): X\n\
Age: X\n\
Will you help war? (Mandatory to help): X\n\
What is your discord profile ID (ie ABCD#1234)? X\n\
What is your forum name?: X\n\
Are you active? How often are you online and for how long?: X\n\
What time zone are you in? X\n\
Whats your first language? X\n\
What guilds were you previously in? X\n\
Why did you chose Hax? X\n\
Other: X```")
            elif res[0].emoji == '❌':
                await channel.send(f"We're sorry to hear that. Feel free to apply in the future if you ever change your mind. :slight_smile:")"""

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

# add the cog "Events" to the bot
def setup(bot):
    bot.add_cog(Events(bot))