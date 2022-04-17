import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
import datastructure
import datatransaction
import sqlite3
import datetime
import asyncio

bot = commands.Bot(command_prefix="*", case_insensitive=True)
bot.author_id = 533777500699099156  # Change to your discord id!!!


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command(name='DM',
             description="Send DMs")
async def DM(ctx,member:discord.Member,*,content):
  await member.send(content)
# async def DM(ctx):
#     players = []
#     message = await ctx.send("Message")
#     await message.add_reaction('✅')
#     await asyncio.sleep(10)
#     client = discord.Client()
#     message = await ctx.fetch_message(message.id)

#     for reaction in message.reactions:
#         if reaction.emoji == '✅':
#             async for user in reaction.users():
#                 # if user != client.user:
#                     players.append(user.mention)

#     if len(players) < 1:
#         await ctx.send('Time is up, and not enough players')
#     else:
#         await ctx.send(players)

#     user = await client.fetch_user("533777500699099156")
#     await user.send("Hello there!")

#     # user=await client.get_user_info("533777500699099156")
#     # await client.send_message(user, "Your message goes here")

#Show Trial Info for Channel
@bot.command(name='show_event',
             description="Show event info for the selected channel")
@commands.guild_only()
async def showtrial(ctx):
    channel_id = str(ctx.channel.id)
    myEmbed = datatransaction.read_event(channel_id)
    #await ctx.send(f"A new channel called {channel_name} was made")
    await ctx.channel.send(embed=myEmbed)

#Create Trial Channel
@bot.command(name='add_event', description="Create a new channel for a trial")
@commands.guild_only()
async def add_event(ctx, channel_name):
    channel = await ctx.guild.create_text_channel(channel_name)
    owner = str(ctx.author).split('#')[0]
    channel_id = channel.id
    print(channel_id)
    datatransaction.add_event(channel_name, channel_id, owner)
    await ctx.send(f"A new channel called {channel_name} was made")

    #Start Data Input Wizard
    await ctx.author.send(f"Enter event information.")

    #channel_id=str(ctx.channel.id)

    def check(msg):
        return msg.author == ctx.author  #and msg.channel == ctx.channel #and \
        #msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    msg_send = msg.content
    #if msg.content.lower() == "y":
    datatransaction.event_info(channel_id, msg_send)

    await ctx.author.send(f"Enter event time.")

    #channel_id=str(ctx.channel.id)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author  # and msg.channel == ctx.channel #and \
        #msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    msg_send = msg.content
    #if msg.content.lower() == "y":
    datatransaction.event_time(channel_id, msg_send)


@bot.command(name="event_info")
@commands.guild_only()
async def event_info(ctx):
    await ctx.send(f"Enter event information.")
    channel_id = str(ctx.channel.id)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel  #and \
        #msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    msg_send = msg.content
    #if msg.content.lower() == "y":
    datatransaction.event_info(channel_id, msg_send)
    #     await ctx.send("You said yes!")
    # else:
    #     await ctx.send("You said no!")


@bot.command(name="event_time")
@commands.guild_only()
async def event_time(ctx):
    await ctx.send(f"Enter event time.")
    channel_id = str(ctx.channel.id)

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel  #and \
        #msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    msg_send = msg.content
    #if msg.content.lower() == "y":
    datatransaction.event_time(channel_id, msg_send)
    #     await ctx.send("You said yes!")
    # else:
    #     await ctx.send("You said no!")


#Create Trial Channel
@bot.command(name='edit_counts',
             description="Create a new channel for a trial")
@commands.guild_only()
async def edit_counts(ctx, tank, healer, dps):
    channel_id = str(ctx.channel.id)
    username = str(ctx.author).split('#')[0]
    print(username)
    channel = str(ctx.channel.name)
    channel_id = str(ctx.channel.id)
    print(channel_id)
    datatransaction.edit_counts(channel_id, username, tank, healer, dps)
    await ctx.send(f"Trial for {channel} was edited")


#Mockup for Status Information
@bot.command(name='status',
             description="Status Reading (Input from Trial Channel)")
@commands.guild_only()
async def status(ctx):
    channel_id = str(ctx.channel.id)
    myEmbed1 = datatransaction.read_event(channel_id)
    myEmbed2 = datatransaction.read_roster(channel_id)
    #await ctx.author.send(embed=myEmbed)
    await ctx.channel.send(embed=myEmbed1)
    await ctx.channel.send(embed=myEmbed2)


#Mockup for Role Information
@bot.command(name='show_roles', description="Roles Reading")
@commands.guild_only()
#@commands.has_role("Core Team") #example of role restricted command
async def showroles(ctx):
    myEmbed = datatransaction.read_roles()
    #await ctx.author.send(embed=myEmbed)
    await ctx.channel.send(embed=myEmbed)


#Have Users Assign Default Role
@bot.command(name='role', description="Default Role Assignment")
@commands.guild_only()
async def role(ctx, role):
    username = str(ctx.author).split('#')[0]
    #role=ctx.content.split(' ')[1]
    #role='DPS'
    sanitized_role = str(role).upper()
    if sanitized_role not in ('TANK', 'HEALER', 'DPS', 'ALT'):
        await ctx.author.send("Unauthorized Role")
    else:
        datatransaction.role_assign(username, sanitized_role)


#Have Users Assign Default Role
@bot.command(name="msg")
@commands.guild_only()
async def msg(ctx):
    await ctx.send(f"Enter a roster message.")
    channel_id = str(ctx.channel.id)
    username = str(ctx.author).split('#')[0]

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel  #and \
        #msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    msg_send = msg.content
    #if msg.content.lower() == "y":
    datatransaction.roster_msg(msg_send, channel_id, username)
    #     await ctx.send("You said yes!")
    # else:
    #     await ctx.send("You said no!")


#Trial Sign for Channel Roster
@bot.command(name='su', description="Trial Signup (Input from Trial Channel)")
@commands.guild_only()
async def su(ctx, *role):
    username = str(ctx.author).split('#')[0]
    user_id = ctx.author.id
    guild = str(ctx.guild).split('#')[0]
    #user_message=str(ctx.content)
    channel = str(ctx.channel.name)
    channel_id = str(ctx.channel.id)
    default = 0

    if not role:
        role = datatransaction.user_role(username)
        default = 1
        print(default)
        print(role)

    date_object = datetime.datetime.now()

    if default == 0:
        sanitized_role = str(role[0]).upper()
        if sanitized_role not in ('TANK', 'HEALER', 'DPS', 'ALT'):
            await ctx.author.send("Unauthorized Role")
        else:
            role = sanitized_role
    if role != 'ALT':
        enrolled_count = datatransaction.query_role_count(channel_id, role)
        limit_count = datatransaction.query_limit_count(channel_id, role)
        print(enrolled_count)
        print(default)
        print(role)
        if enrolled_count < limit_count:
            #await ctx.author.send("There was an open spot")
            response = datatransaction.signup_data(channel_id, username,user_id, guild,
                                                   channel, date_object, role)
        else:
            #await ctx.author.send("Role Full")
            response = 3

    if role == 'ALT':
        response = datatransaction.signup_data(channel_id, username,user_id, guild,
                                               channel, date_object, role)

    if response == 0:
        myEmbed = discord.Embed(title="Trial", description=channel)
        myEmbed.add_field(name="Username: ", value=username, inline=True)
        myEmbed.add_field(name="Status: ",
                          value=role + " Successful Signup",
                          inline=True)
        await ctx.author.send(embed=myEmbed)
    if response == 1:
        myEmbed = discord.Embed(title="Trial", description="Already Enrolled")
        myEmbed.add_field(name="Username: ", value=username, inline=True)
        myEmbed.add_field(name="Status: ",
                          value="Already Enrolled",
                          inline=True)
        await ctx.author.send(embed=myEmbed)
    if response == 2:
        myEmbed = discord.Embed(title="Trial", description="Error")
        myEmbed.add_field(name="Username: ", value=username, inline=True)
        myEmbed.add_field(name="Status: ", value="Signup Failed", inline=True)
        await ctx.author.send(embed=myEmbed)
    if response == 3:
        myEmbed = discord.Embed(title="Trial", description="Error")
        myEmbed.add_field(name="Username: ", value=username, inline=True)
        myEmbed.add_field(name="Status: ",
                          value=role + " Role Full",
                          inline=True)
        await ctx.author.send(embed=myEmbed)


#User withdraws from a given event channels roster
@bot.command(name='wd',
             description="Trial Withdraw (Input from Trial Channel)")
@commands.guild_only()
async def wd(ctx):
    username = str(ctx.author).split('#')[0]
    guild = str(ctx.guild).split('#')[0]
    #user_message=str(ctx.content)
    channel = str(ctx.channel.name)
    channel_id = str(ctx.channel.id)
    datatransaction.delete_signup(channel_id, username, guild, channel)
    myEmbed = discord.Embed(title="Trial", description=channel)
    myEmbed.add_field(name="Username: ", value=username, inline=True)
    myEmbed.add_field(name="Status: ",
                      value="Successfully Withdrawn",
                      inline=True)
    await ctx.author.send(embed=myEmbed)


#Remove all signups
@bot.command(name='nuke_signup', description="Delete all signup information")
@commands.guild_only()
@commands.has_role("Trial lead")
async def nuke_event(ctx):
    datatransaction.nuke_signup()
    myEmbed = discord.Embed(title="Signups", description="Deleted")
    await ctx.author.send(embed=myEmbed)


#Remove all signups
@bot.command(name='nuke_event', description="Delete all event information")
@commands.guild_only()
@commands.has_role("Trial lead")
async def nuke_event(ctx):
    datatransaction.nuke_event()
    myEmbed = discord.Embed(title="Events", description="Deleted")
    await ctx.author.send(embed=myEmbed)


extensions = [
    'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
