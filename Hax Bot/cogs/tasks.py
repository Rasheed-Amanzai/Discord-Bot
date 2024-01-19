import datetime as dt
import time, pickle
from datetime import date

import discord
import requests
from discord.ext import commands, tasks

"""
add_prefix(name)
    Takes in a username and returns the name with their rank prefix added to it.
    If the username (with the prefix) is not a member in the discord server, it will
    instead return None.

remove_prefix(name)
    Takes in a discord name, checks to see if it has a rank prefix,
    and then removes it.

list_members(dict)
    This is a helper function that takes in a guild's information as a dictionary
    (from the API) and returns a list of all members in that guild.

most_wars(dict)
    This is a helper function that sorts every guild member into most wars to least wars.

sort_into_ranks(dict)
    This is a helper function that takes in a dictonary containing each guild member and their
    amount of wars, and then sorts them into their designated ranks.

get_activity(dict)
    Gets the guild's war activity over the past 2 weeks, and sorts everyone into their ranks and the amount of wars
    they've done (using the other helper functions). Returns all of the information once compiled.

count_wars()
    This is one of the main task functions in this file. This function handles all the processes for the biweekly war activity.
    The function first checks to see if 14 days has passed, and once it has, it will start by counting up all the wars done, sort
    everyone into their respective ranks, list everyone from highest to lowest wars, and finally send the information to #guild-activity.

check_wars()
    Another main task function that detects whenever a person joins or leaves the guild. If the person is in the discord server, it will tag
    them. If not, then it will just post their username.
"""

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0 # attack counter
        self.prefixes = ['Commander', 'Commandress', 'Cosmonaut', 'Strategist', 'Pilot', 'Engineer',
                         'Rocketeer', 'Cadet', '🏅 Top Gunner', '🏅 The Architect', '🏅 Cosmic Traveler']

        #self.count_wars.start()
        self.check_members.start()
    
    # Helper Functions
    def add_spaces(self, num):
        spaces = ''

        for i in range(num):
            spaces += ' '
        
        return spaces

    def add_prefix(self, name):        
        for prefix in self.prefixes:
            updated_name = ''
            updated_name = prefix + ' ' + name
            
            for n in [updated_name, name]:
                account = discord.utils.get(self.bot.general.guild.members, display_name=n)
                if account is not None:
                    return account
    
    def remove_prefix(self, name):
        for prefix in self.prefixes:
            if prefix in name:
                return name.split(' ')[-1]
        
    def list_members(self, dict):
        updated_members = []

        for member in dict['members']:
            updated_members.append(member['name'])

        return updated_members

    def most_xp(self, biweekly_sorted):
        lst = [biweekly_sorted['Owner']['xp'][0][1],
               biweekly_sorted['Cosmonaut']['xp'][0][1],
               biweekly_sorted['Pilot']['xp'][0][1],
               biweekly_sorted['Rocketeer']['xp'][0][1],
               biweekly_sorted['Cadet']['xp'][0][1]]
        lst.sort(reverse=True)

        return lst[0]
    
    def sort_into_ranks(self, biweekly_data):
        ranks = {'Owner': {'war': {}, 'xp': {}, 'emerald': {}},
                'Cosmonaut': {'war': {}, 'xp': {}, 'emerald': {}},
                'Pilot': {'war': {}, 'xp': {}, 'emerald': {}},
                'Rocketeer': {'war': {}, 'xp': {}, 'emerald': {}},
                'Cadet': {'war': {}, 'xp': {}, 'emerald': {}}}

        for person in biweekly_data:
            discord_acc = self.add_prefix(person)

            if discord_acc is not None:
                #person_temp = person

                #if '_' in person:
                 #   person_temp = person.replace('_', '\\_')

                if self.bot.owner_role in discord_acc.roles:
                    ranks['Owner']['war'][person] = biweekly_data[person]['war']
                    ranks['Owner']['xp'][person] = biweekly_data[person]['xp']
                    ranks['Owner']['emerald'][person] = biweekly_data[person]['emerald']
                elif self.bot.chief_role in discord_acc.roles:
                    ranks['Cosmonaut']['war'][person] = biweekly_data[person]['war']
                    ranks['Cosmonaut']['xp'][person] = biweekly_data[person]['xp']
                    ranks['Cosmonaut']['emerald'][person] = biweekly_data[person]['emerald']
                elif self.bot.captain_role in discord_acc.roles:
                    ranks['Pilot']['war'][person] = biweekly_data[person]['war']
                    ranks['Pilot']['xp'][person] = biweekly_data[person]['xp']
                    ranks['Pilot']['emerald'][person] = biweekly_data[person]['emerald']
                elif self.bot.recruiter_role in discord_acc.roles:
                    ranks['Rocketeer']['war'][person] = biweekly_data[person]['war']
                    ranks['Rocketeer']['xp'][person] = biweekly_data[person]['xp']
                    ranks['Rocketeer']['emerald'][person] = biweekly_data[person]['emerald']
                elif self.bot.recruit_role in discord_acc.roles:
                    ranks['Cadet']['war'][person] = biweekly_data[person]['war']
                    ranks['Cadet']['xp'][person] = biweekly_data[person]['xp']
                    ranks['Cadet']['emerald'][person] = biweekly_data[person]['emerald']
        
        for rank in ranks:
            ranks[rank]['war'] = sorted(ranks[rank]['war'].items(), key=lambda item: item[1], reverse=True)
            ranks[rank]['xp'] = sorted(ranks[rank]['xp'].items(), key=lambda item: item[1], reverse=True)
            ranks[rank]['emerald'] = sorted(ranks[rank]['emerald'].items(), key=lambda item: item[1], reverse=True)
        
        top3 = {'war': [], 'xp': [], 'emerald': []}

        for category in top3:
            for i in range(3):
                top3[category].append(ranks['Pilot'][category][i])
                top3[category].append(ranks['Rocketeer'][category][i])
                top3[category].append(ranks['Cadet'][category][i])
            
            top3[category] = sorted(top3[category], key=lambda x: x[1], reverse=True)[0:3]
            placement = ['[1]', '[2]', '[3]']

            for i in range(3):
                if top3[category][i] in ranks['Pilot'][category]:
                    new_tuple = (f'{placement[i]} {top3[category][i][0]}', top3[category][i][1])
                    index = ranks['Pilot'][category].index(top3[category][i])
                    ranks['Pilot'][category][index] = new_tuple
                elif top3[category][i] in ranks['Rocketeer'][category]:
                    new_tuple = (f'{placement[i]} {top3[category][i][0]}', top3[category][i][1])
                    index = ranks['Rocketeer'][category].index(top3[category][i])
                    ranks['Rocketeer'][category][index] = new_tuple
                elif top3[category][i] in ranks['Cadet'][category]:
                    new_tuple = (f'{placement[i]} {top3[category][i][0]}', top3[category][i][1])
                    index = ranks['Cadet'][category].index(top3[category][i])
                    ranks['Cadet'][category][index] = new_tuple

        return ranks

    def get_activity(self, wars_per_person):
        activity_msgs = []
        biweekly = pickle.load(open("../biweekly.data", "rb"))

        for person in list(biweekly['data']):
            if person in wars_per_person:
                biweekly['data'][person]['war'] = wars_per_person[person]
            else:
                biweekly['data'].pop(person, None)     
        
        biweekly_sorted = self.sort_into_ranks(biweekly['data'])
        
        longest_name = len(sorted(list(biweekly['data']), key=len, reverse=True)[0])
        longest_xp = len(str(self.most_xp(biweekly_sorted)))

        leaderboard_spacing = [('Wars', longest_name + 10), ('Xp', longest_name + 9), ('Emeralds', longest_name + longest_xp + 8)]

        header = ''

        for i in range(len(leaderboard_spacing)):
            if leaderboard_spacing[i][0] == 'Wars':
                header += self.add_spaces(leaderboard_spacing[i][1] - 3)
            else:
                header += self.add_spaces(leaderboard_spacing[i][1])
            
            header += f'{leaderboard_spacing[i][0]}'

        for rank in biweekly_sorted:
            activity = f'**{rank}:**\n'
            activity += '```py\n'

            if rank == 'Owner':
                activity += f'{header}\n\n'

            for i in range(len(biweekly_sorted[rank]['war'])):
                extra_spaces = [4, 4, 4]

                if '[' in biweekly_sorted[rank]['war'][i][0]:
                    extra_spaces[0] -= 4
                if '[' in biweekly_sorted[rank]['xp'][i][0]:
                    extra_spaces[1] -= 4
                if '[' in biweekly_sorted[rank]['emerald'][i][0]:
                    extra_spaces[2] -= 4

                activity += f'{self.add_spaces(extra_spaces[0])}{biweekly_sorted[rank]["war"][i][0]}{self.add_spaces(leaderboard_spacing[0][1] - len(biweekly_sorted[rank]["war"][i][0]) - extra_spaces[0] - 3)}{biweekly_sorted[rank]["war"][i][1]}'

                activity += f'{self.add_spaces(6 + extra_spaces[1] - len(str(biweekly_sorted[rank]["war"][i][1])))}{biweekly_sorted[rank]["xp"][i][0]}{self.add_spaces(longest_name + 7 - extra_spaces[1] - len(biweekly_sorted[rank]["xp"][i][0]))}{biweekly_sorted[rank]["xp"][i][1]}'

                activity += f'{self.add_spaces(longest_xp + extra_spaces[2] + 3 - len(str(biweekly_sorted[rank]["xp"][i][1])))}{biweekly_sorted[rank]["emerald"][i][0]}{self.add_spaces(longest_name + 7 - extra_spaces[2] - len(biweekly_sorted[rank]["emerald"][i][0]))}'

                activity += f'{biweekly_sorted[rank]["emerald"][i][1]}\n'

                if rank == 'Cadet' and len(activity) >= 1850:
                    activity += '```'
                    activity_msgs.append(activity)
                    activity = '```py\n'
            
            activity += '```'
            activity_msgs.append(activity)

        return activity_msgs
    
    # Task Functions
    @tasks.loop(seconds=1, reconnect=True)
    async def count_wars(self):
        await self.bot.wait_until_ready()

        f = open('time.txt', 'r+')
        recorded_time = dt.datetime.strptime(f.read().strip('\n'), '%Y-%m-%d %H:%M:%S.%f')
        current_time = dt.datetime.now()
        delta_time = current_time - recorded_time
        
        if delta_time.days >= 14:
            f.seek(0)
            f.truncate(0)
            f.write(str(current_time))
            f.close()

            time_since_date = current_time.utcnow() - dt.timedelta(days=14)
            wars_per_person = {}
            total_wars = 0

            async for message in self.bot.guild_activity2.history(limit=None, after=time_since_date):
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
                account = self.add_prefix(person)

                if account is None:
                    try:
                        res1 = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{person}?at={int(time.time()) - 2592000}').json()
                        if 'id' not in res1:
                            raise ValueError
                        
                        uuid = res1['id']
                        res2 = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names').json()
                        guild_members = []

                        for member in self.bot.guild_chat.members:
                            guild_members.append(member.display_name)

                        for dict in res2:
                            for prefix in self.prefixes:
                                if (prefix + ' ' + dict['name']) in guild_members:
                                    wars_per_person[dict['name']] += wars_per_person[person]
                                    wars_per_person[person] = 0
                                    break
                            else:
                                continue
                            
                            break

                    except ValueError:
                        pass
            
            guild_roles = [self.bot.recruit_role, self.bot.recruiter_role, self.bot.captain_role, self.bot.chief_role]

            for role in guild_roles:
                for member in role.members:
                    member_name = self.remove_prefix(member.display_name)
                    if member_name not in wars_per_person and member_name is not None:
                        wars_per_person[member_name] = 0

            recorded_time = recorded_time + dt.timedelta(days=1)
            await self.bot.test_channel.send(f'```ml\nBiweekly Activity: {recorded_time.strftime("%Y-%m-%d")} to {current_time.strftime("%Y-%m-%d")}\n```')
            for msg in self.get_activity(wars_per_person):
                await self.bot.test_channel.send(msg)
        else:
            f.close()

    @tasks.loop(seconds=30, reconnect=True)
    async def check_members(self):
        await self.bot.wait_until_ready()
        res = requests.get('https://api.wynncraft.com/public_api.php?action=guildStats&command=HackForums').json()

        # List of updated Hax members
        updated_members = self.list_members(res)

        if list(set(updated_members) - set(self.bot.hax_members)) != []:
            new_members = list(set(updated_members) - set(self.bot.hax_members))
            print('NEW members:', new_members)

            for person in new_members:
                # Searches for display_name in given channel
                discord_name = self.add_prefix(person)

                if discord_name is not None:
                    await self.bot.member_log.send(f'{discord_name.mention} has joined the guild.')
                else:
                    await self.bot.member_log.send(f'{person} has joined the guild.')

                self.bot.hax_members.append(person)

                apply_here = (self.bot.get_channel(669047828949106702)).category

                for chan in apply_here.channels:
                    for mem in chan.members:
                        if mem == discord_name and self.bot.chief_role not in mem.roles:
                            async for message in chan.history(limit=1, oldest_first=True):
                                await message.add_reaction('🔒')
                                await chan.send(f'{discord_name.display_name} has successfully joined the guild.')
 
                                roles = [self.bot.recruit_role, self.bot.warping_role, self.bot.passengers_role,
                                         self.bot.guild_separator, self.bot.event_separator, self.bot.profile_separator]

                                await discord_name.add_roles(*roles)
                                await discord_name.edit(nick=f"Cadet {discord_name.display_name}")
                                
                                guild_info = self.bot.get_channel(794979777312325672)
                                guild_roles = self.bot.get_channel(786507874468757544)

                                await self.bot.guild_chat.send(f'Welcome to HackForums {discord_name.mention}! \
Make sure to check out {guild_info.mention} and assign yourself roles in {guild_roles.mention}.')


                f = open('apps.txt', 'r+')
                apps = f.read()
                apps = eval(apps)

                if person in apps:
                    try:
                        msg = await self.bot.guild_apps.fetch_message(apps[person])
                        await msg.delete()
                        apps.pop(discord_name.display_name, None)
                    except discord.errors.NotFound:
                        print(f'{person} was not found in guild apps.')

                f.seek(0)
                f.truncate(0)
                f.write(str(apps))
                f.close()

        elif list(set(self.bot.hax_members) - set(updated_members)) != []:
            past_members = list(set(self.bot.hax_members) - set(updated_members))
            print('PAST members:', past_members)

            for person in past_members:
                discord_name = self.add_prefix(person)

                if discord_name is not None:
                    await self.bot.member_log.send(f'{discord_name.mention} has left the guild.')

                    if self.bot.kick_status == True:
                        await discord_name.send("""You have been kicked from HackForums for being inactive and/or not completing your war requirements.
        If you think your kick is a mistake, please let us know by contacting a Chief.
        Feel free to apply again in the future if you become more active and interested in warring again.""")

                        await discord_name.remove_roles(*discord_name.roles[1:])
                else:
                    await self.bot.member_log.send(f'{person} has left the guild.')

                self.bot.hax_members.remove(person)
        else:
            pass

def setup(bot):
    bot.add_cog(Tasks(bot))
