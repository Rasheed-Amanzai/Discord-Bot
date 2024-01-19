import discord, random, requests, time
import datetime as dt
from datetime import date
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix = '*')
bot.remove_command("help")

# Helper Functions
def list_members(dict):
    temp_members = []

    for member in dict['members']:
        temp_members.append(member['name'])

    return temp_members

def most_wars(d):
    dict = {}

    for rank in d:
        for person in d[rank]:
            dict[d[rank][person]] = person

    return sorted(dict.keys(), reverse=True)

def sort_into_ranks(wars_per_person):
    general = bot.get_channel(278279447449305088)

    # Discord Guild Ranks
    recruit_role = discord.utils.get(general.guild.roles, name='Cadet')
    recruiter_role = discord.utils.get(general.guild.roles, name='Engineer')
    trial_role = discord.utils.get(general.guild.roles, name='Space Pilot')
    captain_role = discord.utils.get(general.guild.roles, name='Rocketeer')
    chief_role = discord.utils.get(general.guild.roles, name='Cosmonaut')
    owner_role = discord.utils.get(general.guild.roles, name='darkie')

    ranks = {'**Owner**': {},
             '**Cosmonaut**': {},
             '**Rocketeer**': {},
             '**Engineer**': {},
             '**Cadet**': {}}

    for person in wars_per_person:
        discord_acc = discord.utils.get(general.guild.members, display_name=person)

        if discord_acc is not None:
            if owner_role in discord_acc.roles:
                ranks['**Owner**'][person] = wars_per_person[person]
            elif chief_role in discord_acc.roles:
                ranks['**Cosmonaut**'][person] = wars_per_person[person]
            elif captain_role in discord_acc.roles:
                ranks['**Rocketeer**'][person] = wars_per_person[person]
            elif trial_role in discord_acc.roles:
                ranks['**Rocketeer**'][person] = wars_per_person[person]
            elif recruiter_role in discord_acc.roles:
                ranks['**Engineer**'][person] = wars_per_person[person]
            elif recruit_role in discord_acc.roles:
                ranks['**Cadet**'][person] = wars_per_person[person]

    return ranks


def get_activity(wars_per_person):
    activity = ''
    wars = sort_into_ranks(wars_per_person)

    war_leaderboard = most_wars(wars)

    for rank in wars:
        activity += f'{rank}\n'
        sorted_wars = sorted(wars[rank].items(), key=lambda item: item[1], reverse=True)

        for person in sorted_wars:
            if wars[rank][person[0]] == war_leaderboard[0]:
                activity += f'{person[0]}: {person[1]}🥇\n'
            elif wars[rank][person[0]] == war_leaderboard[1]:
                activity += f'{person[0]}: {person[1]}🥈\n'
            elif wars[rank][person[0]] == war_leaderboard[2]:
                activity += f'{person[0]}: {person[1]}🥉\n'
            else:
                activity += f'{person[0]}: {person[1]}\n'

        activity += '\n'

    return activity

@bot.event
async def on_ready():
    print('Bot is ready.')
    kick = False

@bot.event
async def on_message(message):
    # Discord Channels
    general = bot.get_channel(278279447449305088)
    guild_apps = bot.get_channel(690657563125219328)
    deleted_apps = bot.get_channel(500043924887306241)

    # Discord Roles
    recruit_role = discord.utils.get(general.guild.roles, name='Cadet')
    recruiter_role = discord.utils.get(general.guild.roles, name='Engineer')
    captain_role = discord.utils.get(general.guild.roles, name='Rocketeer')
    chief_role = discord.utils.get(general.guild.roles, name='Cosmonaut')
    guild_roles = [recruit_role, recruiter_role, captain_role, chief_role]

    if message.content.startswith(('IGN', 'Ign', 'ign', 'GN', 'Gn' 'gn')) and message.channel.category.id == 632705662010523669 and [i for i in message.author.roles if i in guild_roles] == []:
        text = message.content.split()
        punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*~'''

        if text[0] == ('IGN:' or 'Ign:' or 'ign:' or 'GN:' or 'Gn:' or 'gn:'):
            name = text[1].translate(str.maketrans('', '', punctuation))
            await message.author.edit(nick=name)
        else:
            name = (text[0].replace('IGN:' or 'Ign:' or 'ign:' or 'GN:' or 'Gn:' or 'gn:', '')).translate(str.maketrans('', '', punctuation))
            await message.author.edit(nick=name)

        await message.channel.send(f'Thank you for your application {message.author.mention}, we will get back to you shortly.')
        app = await guild_apps.send(f'{message.content} \n@here')
        await deleted_apps.send(f'{message.content}')

        await app.add_reaction('✅')
        await app.add_reaction('❌')

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

    await bot.process_commands(message)

"""@bot.event
async def on_message(message):
    global CLAIMS, attack_counter

    general = bot.get_channel(278279447449305088)
    territory_log = bot.get_channel(483111114767335435)
    claim_log = bot.get_channel(696794398943346746)
    trial_role = discord.utils.get(general.guild.roles, name='Space Pilot')
    captain_role = discord.utils.get(general.guild.roles, name='Rocketeer')

    if message.channel == territory_log:
        enemy_guild = ""
        words = message.content.split()
        terr = message.content.split(":")[0]

        if terr in CLAIMS:
            for i in range(len(words)):

                if words[i] == "→" and words[i + 1].replace("*", "") != "HackForums":
                    print(words[i + 1])
                    print("ENEMY")
                    for j in range(i + 1, len(words)):
                        if "(" not in words[j] and "(" not in words[j + 1]:
                            enemy_guild += (words[j] + " ")
                        elif "(" not in words[j]:
                            enemy_guild += words[j]
                        else:
                            break

                    attack_counter += 1
                    break

                elif words[i] == "→" and words[i + 1].replace("*", "") == "HackForums":
                    print("HAX")
                    if attack_counter > 0:
                        attack_counter -= 1

                    break

        if attack_counter == 1:
            await claim_log.send(f'⚔️ **{enemy_guild}** has taken control of **{terr}** ⚔️\nPlease respond to the attack and reclaim our territory.')
            attack_counter = 0"""


@tasks.loop(seconds=1)
async def count_wars():
    await bot.wait_until_ready()

    f = open('time.txt', 'r+')
    recorded_time = dt.datetime.strptime(f.read().strip('\n'), '%Y-%m-%d %H:%M:%S.%f')
    current_time = dt.datetime.now()
    delta_time = current_time - recorded_time

    if delta_time.days >= 14:
        f.seek(0)
        f.truncate(0)
        f.write(str(current_time))
        f.close()

        guild_activity = bot.get_channel(396000464245882892)
        guild_activity2 = bot.get_channel(444064283890941952)
        time_since_date = current_time.utcnow() - dt.timedelta(days=14)
        wars_per_person = {}
        total_wars = 0

        async for message in guild_activity2.history(limit=None, after=time_since_date):
            total_wars += 1
            text = message.content.split()[3:-6]

            for person in text:
                if ',' in person:
                    person = person.replace(',', '')
                if '~' in person:
                    person = person.replace('~', '')
                if '\\' in person:
                    person = person.replace('\\', '')

                if person not in wars_per_person:
                    wars_per_person[person] = 1
                else:
                    wars_per_person[person] += 1

        for person in wars_per_person:
            general = bot.get_channel(278279447449305088)
            acc = discord.utils.get(general.guild.members, display_name=person)

            if acc is None:
                guild_chat = bot.get_channel(278284723153797143)

                try:
                    res1 = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{person}?at={int(time.time()) - 2592000}').json()

                    if 'id' not in res1:
                        raise ValueError

                    uuid = res1['id']
                    res2 = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names').json()
                    guild_members = []

                    for member in guild_chat.members:
                        guild_members.append(member.display_name)

                    for dict in res2:
                        print(dict['name'])
                        if dict['name'] in guild_members:
                            print(dict['name'], wars_per_person[dict['name']])
                            wars_per_person[dict['name']] += wars_per_person[person]
                            print(dict['name'], wars_per_person[dict['name']])
                            wars_per_person[person] = 0
                            break

                except ValueError:
                    pass

        recorded_time = recorded_time + dt.timedelta(days=1)
        await guild_activity.send(f'```Wars since {recorded_time.strftime("%B %d %Y")}\nTotal Wars: {total_wars}```\n\n')
        await guild_activity.send(get_activity(wars_per_person))
    else:
        f.close()

@tasks.loop(seconds=30)
async def check_members():
    await bot.wait_until_ready()
    # Discord Channels
    general = bot.get_channel(278279447449305088)
    member_log = bot.get_channel(679716463434924180)
    subguild_log = bot.get_channel(696793213658464366)

    global hax_members, kick
    request = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command=HackForums').json()

    # List of updated Hax members
    temp_members = list_members(request)

    if list(set(temp_members) - set(hax_members)) != []:
        new_members = list(set(temp_members) - set(hax_members))

        for person in new_members:
            # Searches for display_name in given channel
            print(person)
            discord_name = discord.utils.get(general.guild.members, display_name=person)
            chief_role = discord.utils.get(general.guild.roles, name='Cosmonaut')

            if discord_name is not None:
                await member_log.send(f'{discord_name.mention} has joined the guild.')
            else:
                await member_log.send(f'{person} has joined the guild.')

            hax_members.append(person)

            apply_here = (bot.get_channel(669047828949106702)).category

            for chan in apply_here.channels:
                for mem in chan.members:
                    if mem == discord_name and chief_role not in mem.roles:
                        async for message in chan.history(limit=1, oldest_first=True):
                            await message.add_reaction('🔒')
                            await chan.send(f'{discord_name.display_name} has successfully joined the guild.')

                            guild_chat = bot.get_channel(278284723153797143)
                            recruit_role = discord.utils.get(general.guild.roles, name='Cadet')
                            warping_role = discord.utils.get(general.guild.roles, name='WarPing')
                            roles = [recruit_role, warping_role]

                            await discord_name.add_roles(*roles)
                            await guild_chat.send(f'Welcome to HackForums {discord_name.mention}!')


            f = open('apps.txt', 'r+')
            apps = f.read()
            apps = eval(apps)

            if person in apps:
                guild_apps = bot.get_channel(690657563125219328)
                msg = await guild_apps.fetch_message(apps[discord_name.display_name])
                await msg.delete()
                apps.pop(discord_name.display_name, None)

            f.seek(0)
            f.truncate(0)
            f.write(str(apps))
            f.close()

    elif list(set(hax_members) - set(temp_members)) != []:
        past_members = list(set(hax_members) - set(temp_members))

        for person in past_members:
            discord_name = discord.utils.get(general.guild.members, display_name=person)

            if discord_name is not None:
                await member_log.send(f'{discord_name.mention} has left the guild.')

                if kick == True:
                    await discord_name.send("""You have been kicked from HackForums for being inactive and/or not completing your war requirements.
If you think your kick is a mistake, please let us know by contacting a Chief.
Feel free to apply again in the future if you become more active and interested in warring again.""")

                    await discord_name.remove_roles(*discord_name.roles[1:])
            else:
                await member_log.send(f'{person} has left the guild.')

            hax_members.remove(person)
    else:
        pass

class Haxbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Discord Channels
        self.general = bot.get_channel(278279447449305088)
        self.guild_chat = bot.get_channel(278284723153797143)
        self.member_log = bot.get_channel(679716463434924180)
        self.subguild_log = bot.get_channel(696793213658464366)
        self.guild_activity = bot.get_channel(396000464245882892)
        self.guild_activity2 = bot.get_channel(444064283890941952)
        self.guild_apps = bot.get_channel(690657563125219328)
        self.deleted_apps = bot.get_channel(500043924887306241)

        #Discord Roles
        self.recruit_role = discord.utils.get(self.general.guild.roles, name='Cadet')
        self.recruiter_role = discord.utils.get(self.general.guild.roles, name='Engineer')
        self.captain_role = discord.utils.get(self.general.guild.roles, name='Rocketeer')
        self.chief_role = discord.utils.get(self.general.guild.roles, name='Cosmonaut')
        self.commander_role = discord.utils.get(self.general.guild.roles, name='Commander')
        self.owner_role = discord.utils.get(self.general.guild.roles, name='darkie')
        self.bot_role = discord.utils.get(self.general.guild.roles, name='Robot')

        #Misc Variables
        res = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command=HackForums').json()
        self.hax_members = list_members(res)
        self.kick = False
        self.claims = ['Rodoroc', 'Crater Descent', 'Molten Heights Portal', 'Active Volcano', 'Volcanic Slope' 'Orc Road',
                       'Orc Lake', 'Green Camp', 'Red Camp', 'Black Camp', 'Meteor Crater', 'Bucie North West', 'Bucie North East',
                       'Bucie South West', 'Bucie South East', 'Llevigar Farm', 'Pre-Light Forest Transition']
        self.attack_counter = 0

    #Bot Commands
    @commands.command()
    async def help(ctx):
        embed=discord.Embed(title="Command List", color=0x800080)

        embed.add_field(name="***help**", value="Returns this help message.", inline=False)
        embed.add_field(name="***ping**", value="Returns the bot's latency in ms.", inline=False)
        embed.add_field(name="***togglekick**", value=f"A setting used for kicking multiple members from the guild.\
                                                   If a guild member gets kicked/leaves while this is on, it will send them a message saying\
                                                   they've been kicked from the guild and all of their roles will be removed.", inline=False)
        embed.add_field(name="***accept**", value="Sends a message informing the applicant that their application to the guild has been accepted.\
                                               Only use this command in the ticket channel.")
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(ctx):
        await ctx.send(f'Pong! `{int(round(bot.latency, 3) * 1000)} ms`')

    @commands.command()
    async def togglekick(ctx):
        global kick

        if kick == True:
            kick = False
            await ctx.send('Kick message is now **off**')
        else:
            kick = True
            await ctx.send('Kick message is now **on**')

    @commands.command()
    async def accept(ctx):
        await ctx.message.delete()

        for member in ctx.channel.members:
            if (self.chief_role not in member.roles) and (self.commander_role not in member.roles) and (self.bot_role not in member.roles):
                await ctx.send(f"Your application has been accepted! Whenever you're available,\
    please message a recruiter+ ingame to get a invite to the guild.\
    https://www.wynndata.tk/stats/guild/HackForums\n{member.mention}")
                break

check_members.start()
#count_wars.start()
bot.run('Njc3MjUzNjk4MTk5NjE3NTU5.XkRj0w.dPHlH73oQ_u-HeuSGlAnLouMRL0')
bot.add_cog(Haxbot(bot))
