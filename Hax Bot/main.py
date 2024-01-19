import discord, requests, time
import datetime as dt
from datetime import date
from discord.ext import commands, tasks

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '*', intents=intents)
bot.remove_command("help")

"""
list_members(dict)
    This is a helper function that takes in a guild's information as a dictionary
    (from the API) and returns a list of all members in that guild.

startup()
    The main method that handles all the work that needs to be done during the bot's
    startup sequence. It initializes multiple varibles and loads in the extensions (cogs)
    from the cogs folder.

on_ready()
    A discord event function that is called whenever the bot is ready (when it's done with internal work).
    This function then proceeds to call the startup() function, and prints out "Bot is ready." once it's
    done with its startup tasks.
"""

def list_members(dict):
    temp_members = []

    for member in dict['members']:
        temp_members.append(member['name'])

    return temp_members

async def startup():
    # Discord Channels
    bot.general = bot.get_channel(768676139064492033)
    bot.guild_chat = bot.get_channel(740381703201226883)
    bot.member_log = bot.get_channel(679716463434924180)
    bot.subguild_log = bot.get_channel(696793213658464366)
    bot.guild_activity = bot.get_channel(396000464245882892)
    bot.guild_activity2 = bot.get_channel(444064283890941952)
    bot.guild_apps = bot.get_channel(690657563125219328)
    bot.deleted_apps = bot.get_channel(500043924887306241)
    bot.test_channel = bot.get_channel(754478164679458886)

    # Discord Roles
    bot.guild_separator = discord.utils.get(bot.general.guild.roles, name='⁣       ◅ ◁  Guild  ▷ ▻        ⁣')
    bot.event_separator = discord.utils.get(bot.general.guild.roles, name='⁣     ◅ ◁  Event Pings  ▷ ▻       ⁣')
    bot.profile_separator = discord.utils.get(bot.general.guild.roles, name='⁣       ◅ ◁  Profile  ▷ ▻        ⁣')
    bot.bot_role = discord.utils.get(bot.general.guild.roles, name='Robot')
    bot.manager_role = discord.utils.get(bot.general.guild.roles, name='Discord Manager')
    bot.passengers_role = discord.utils.get(bot.general.guild.roles, name='Passengers')
    bot.warping_role = discord.utils.get(bot.general.guild.roles, name='WarPing')
    bot.recruit_role = discord.utils.get(bot.general.guild.roles, name='Cadet')
    bot.recruiter_role = discord.utils.get(bot.general.guild.roles, name='Rocketeer')
    bot.captain_role = discord.utils.get(bot.general.guild.roles, name='Pilot')
    bot.chief_role = discord.utils.get(bot.general.guild.roles, name='Cosmonaut')
    bot.commander_role = discord.utils.get(bot.general.guild.roles, name='Commander')
    bot.owner_role = discord.utils.get(bot.general.guild.roles, name='darkie')

    # Misc Variables
    res = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command=HackForums').json()
    bot.hax_members = list_members(res)
    bot.kick_status = False

    extensions = ['cogs.commands'] #['cogs.commands', 'cogs.events', 'cogs.tasks']

    # loads in the extensions
    for ext in extensions:
        bot.load_extension(ext)

@bot.event
async def on_ready():
    await startup()
    print('Bot is ready.')

bot.run('Njc3MjUzNjk4MTk5NjE3NTU5.XkRj0w.dPHlH73oQ_u-HeuSGlAnLouMRL0')
#2020-12-17 19:07:04.543493