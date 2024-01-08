#
#IMPORTS
#
from staying_alive import keep_alive
keep_alive()


import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from replit import db
import sys
import datetime



#
#AROUND THE WORLD AROUND THE WORLD!
#


#Boolean Ones
global delete_edit_notifier
global slapEnable
global pingEnable
global msgLogEnable
global welcomeEnable

#Value Ones
global delete_edit_channel
global welcome_channel
global audit_log_channel


#Misc
global mutedUsers
global mutedUsersTime
global bannedWords



#
#Config
#

#Value

#To get the channel id please refer to this wikipedia post https://en.wikipedia.org/wiki/Template:Discord_channel#:~:text=To%20get%20the%20channel%2Fserver,to%20get%20the%20guild%20ID.

delete_edit_channel =            #Paste in channel id
welcome_channel =                #Paste in channel id
audit_log_channel =              #Paste in channel id

#Enable/Disable Commands

#Moderation
delete_edit_notifier = False
welcomeEnable = True
msgLogEnable = True
botStatsEnable = True
#Fun
slapEnable = True
pingEnable = True
echoEnable = True




#
#Variables
#

mutedUsers = []
mutedUsersTime = []
bannedWords = []




#
#Define the Bot
#

try:
  TOKEN = db["GOMTOKEN"]
except:
  print("There is no token")
  TOKEN = input("Please enter your token: ")
  db["GOMTOKEN"] = TOKEN
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="/", intents = intents, case_insensitive=True)

#
#Events
#


#
#Sync Commands
#

@bot.event
async def on_ready():
  os.system('clear')
  print(f"Bot is Up! Current User: {bot.user}")
  print()
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

#
#Message Logger/Fun Responses
#

@bot.event
async def on_message(message):
  
  msgContent = message.content
  msgContentLower = msgContent.lower()
  msgAuthor = message.author


  #Log Message
  if msgLogEnable:
    #Check for Attachments
    if message.attachments:
      messageLog = open("messageLog.txt", "a")
      print(f"{msgAuthor} sent the following attachments: ")
      for i in range(len(message.attachments)):
        print(f"{message.attachments[i].url}")
        messageLog.write(f"{msgAuthor} sent attachment: {message.attachments[i].url} @ {datetime.datetime.now()}\n")
        print()
      messageLog.close()
    #Otherwise text
    else:
      print(f"{msgAuthor} said: {msgContent}")
      try:
        messageLog = open("messageLog.txt", "a")
        messageLog.write(f"{msgAuthor} said: {msgContent} @ {datetime.datetime.now()}\n")
        messageLog.close()
      except:
        print("'messageLog.txt' is needed! Please create it!")
    
  #Update the muted users
  for i in range(len(mutedUsers)):
    userSentence = mutedUsersTime[i]
    mutedUser = mutedUsers[i]
    if userSentence < datetime.datetime.now():
      mutedUsers.remove(mutedUser)
      mutedUsersTime.remove(userSentence)


  #Check for author if muted
  if msgAuthor.id in mutedUsers:
    await message.delete()


#
#Checks for Edits

@bot.event
async def on_message_edit(before, after):
  if before.author != bot.user:
    if delete_edit_notifier:
      channel = await bot.fetch_channel(delete_edit_channel)
      print(f"{before.author} edited message to -> {after.content}")
      await channel.send(f"{before.author.mention} edited the message: **{before.content}** to **{after.content}**! ")
      await channel.send(f"Here's where to find it -> {after.channel.mention}!")


#
#Check for Deletes
#

@bot.event
async def on_message_delete(message):
  if message.author != bot.user:
    if delete_edit_notifier:
      channel = await bot.fetch_channel(delete_edit_channel)
      print(f"{message.author} deleted a message! The message was -> {message.content}!")
      await channel.send(f"{message.author.mention} deleted a message! The original message was **{message.content}**!")
      await channel.send(f"Here's where to find it -> {message.channel.mention}!")
  


    

#
#Welcome New Members
#

@bot.event
async def on_member_join(user):
  if welcomeEnable:
    welcomeList = [1, 2, 3]
    pickWelcome = random.choice(welcomeList)
    chanel = await bot.fetch_channel(welcome_channel)
    if pickWelcome == 1:
      await chanel.send(f"Welcome {user.mention}!")
    elif pickWelcome == 2:
      await chanel.send(f"Thanks for joining us {user.mention}!")
    elif pickWelcome == 3:
      await chanel.send(f"Should've brought boba... we hungry here {user.mention}!")
    else:
      print("Error Loading Welcome Message")
  else:
    print("New Member! But Welcome Message is Disabled!")



#
#Fun Commands
#


#
#WILL SMITH
#

@bot.tree.command(name="slap", description="Slap someone random!")
@app_commands.describe(user="Person to slap")
@app_commands.describe(reason="Reason to slap")
async def slap(interaction: discord.Interaction, user:discord.User, *, reason:str):
  if slapEnable:
    await interaction.response.send_message("Loren Ipsum", ephemeral=True, delete_after=0.01)
    await interaction.channel.send(f"{interaction.user.mention} slapped {user.mention} " + reason)
  else:
    await interaction.response.send_message(":x: This command is disabled!", ephemeral=True, delete_after=5)

#
#LATENCY
#


@bot.tree.command(name="ping", description="Returns latency of the bot")
async def ping(interaction: discord.Interaction):
  if pingEnable:
    await interaction.response.send_message(f":ping_pong: PONG! Latency: {round (bot.latency * 1000)} ms!")
    await interaction.response.send_message(":x: This command is disabled!", ephemeral=True, delete_after=5)


#
#ECHOooooo
#

@bot.tree.command(name="echo", description="Gom will imitate what you said")
@app_commands.describe(message="Message to Replicate")
async def echo(interaction: discord.Interaction, *, message:str):
  if echoEnable:
    await interaction.response.send_message("Loren Ipsum", ephemeral=True, delete_after=0)
    await interaction.channel.send(f"{message}")
  else:
    await interaction.response.send_message(":x: This command is disabled!", ephemeral=True, delete_after=5)
  

#
#Bot Stats
#

@bot.tree.command(name="bot_stats", description = "Returns this bot's stats")
async def bot_stats(interaction: discord.Interaction):
  if botStatsEnable:
    developer = await bot.fetch_user(668626305188757536)
    
    bot_stats = discord.Embed(title="Bot Stats")
    bot_stats.add_field(name = "Developer", value= f"{developer}")
    bot_stats.add_field(name = "Version", value = "1.0.0")
    bot_stats.add_field(name = "Python Version", value = sys.version)
    bot_stats.add_field(name = "Discord.PY Version", value = discord.__version__)
  
    await interaction.response.send_message(embed=bot_stats)
  else:
    await interaction.response.send_message(":x: This command is disabled!", ephemeral=True, delete_after=5)


#
#Modding
#


#
#Check for muted users
#

@bot.tree.command(name="check_muted", description="Check for muted users")
async def check_muted(interaction: discord.Interaction):
  if len(mutedUsers) > 0:
    await interaction.response.send_message("Sending list...", ephemeral=True, delete_after=0.1)
    await interaction.channel.send("These are the muted users!")
    for i in range(len(mutedUsers)):
      user = interaction.guild.get_member(mutedUsers[i])
      sentenceLeft = mutedUsersTime[i] - datetime.datetime.now()
      await interaction.channel.send(f"```User: {user}  Sentence: {sentenceLeft}```")
      

  
  else:
    await interaction.response.send_message("No muted users!", ephemeral=True)

    

#
#Kick
#

@bot.tree.command(name="kick", description = "Kicks a User with a Reason!")
@app_commands.describe(user = "User to Kick!")
@app_commands.describe(reason = "Reason for the Kick")
async def kick(interaction: discord.Interaction, user:discord.User, *, reason:str):
  author = interaction.user
  auditchannel = await bot.fetch_channel(audit_log_channel)

  successfulKick = discord.Embed(title=":white_check_mark: User Successfully Kicked!")

  unsuccessfulKickLevelHigh = discord.Embed(title=":x: Bot Level lower than User!")

  unsuccessfulKickSelf = discord.Embed(title=":x: You cannot kick yourself!")

  unsuccessfulKickPermissions = discord.Embed(title=":x: Missing Permissions!")

  unsuccessfulKickBot = discord.Embed(title=":x: I cannot kick myself!")
  
  
  if author.guild_permissions.kick_members:
    if user != author:
      if user != bot.user:
        try:
          await interaction.guild.kick(user)
          await interaction.response.send_message(embed=successfulKick)
          print(f"{author} kicked user ->  {user}")
          await auditchannel.send(f"{author.mention} kicked user ->  {user.mention}. Reason: {reason}")
        except Exception as e:
          print(e)
          await interaction.response.send_message(embed=unsuccessfulKickLevelHigh)
      else:
        await interaction.channel.send_message(embed=unsuccessfulKickBot)
    else:
      await interaction.channel.send_message(embed=unsuccessfulKickSelf)
  else:
    await interaction.response.send_message(embed=unsuccessfulKickPermissions)




#
#Banz
#

@bot.tree.command(name="ban", description = "Ban a User with a Reason!")
@app_commands.describe(user = "User to Ban")
@app_commands.describe(reason = "Reason for the Ban")
async def ban(interaction: discord.Interaction, user:discord.User, *, reason:str):
  author = interaction.user
  auditchannel = await bot.fetch_channel(audit_log_channel)

  successfulBan = discord.Embed(title=":white_check_mark: User Successfully Banned!")

  unsuccessfulBanHigherLevel = discord.Embed(title=":x: Bot Level lower than User!")

  unsuccessfulBanSelf = discord.Embed(title=":x: You cannot ban yourself!")

  unsuccessfulBanPermissions = discord.Embed(title=":x: Missing Permissions!")

  unsuccessfulBanBot = discord.Embed(title=":x: I cannot ban myself!")

  if author.guild_permissions.ban_members:
    if user != author:
      if user != bot.user:
        try:
          await interaction.guild.ban(user)
          await interaction.response.send_message(embed=successfulBan)
          print(f"{author} kicked user ->  {user}")
          await auditchannel.send(f"{author.mention} banned user ->  {user.mention}. Reason: {reason}")
        except Exception as e:
          print(e)
          await interaction.response.send_message(embed=unsuccessfulBanHigherLevel)
      else:
        await interaction.response.send_message(embed=unsuccessfulBanBot)
    else:
      await interaction.response.send_message(embed=unsuccessfulBanSelf)
  else:
    await interaction.response.send_message(embed=unsuccessfulBanPermissions)

#
#Text Mute
#

@bot.tree.command(name="tmute", description="Text Mutes a User")
@app_commands.describe(user="User to mute")
@app_commands.describe(reason="Reason for mute")
@app_commands.describe(time="Time (in minutes) for mute")
async def tmute(interaction:discord.Interaction, user:discord.User, *, reason:str, time:int):
  author = interaction.user
  auditchannel = await bot.fetch_channel(audit_log_channel)

  successfulMute = discord.Embed(title=f":white_check_mark: User Successfully Muted for {time} minute(s)!")

  unsuccessfulMuteError = discord.Embed(title=":x: Unexpected Error Occurred!")

  unsuccessfulMuteSelf = discord.Embed(title=":x: You cannot mute yourself!")

  unsuccessfulMutePermissions = discord.Embed(title=":x: Missing Permissions!")

  unsuccessfulMuteBot = discord.Embed(title=":x: I cannot mute myself!")

  unsuccessfulMuteTime = discord.Embed(title=":x: Time must be > 0!")

  if author.guild_permissions.moderate_members:
    if user != author:
      if user != bot.user:
        if time > 0:
          try:
            mutedUsers.append(user.id)
            mutedUsersTime.append(datetime.datetime.now() + datetime.timedelta(minutes=time))
            await interaction.response.send_message(embed=successfulMute)
            print(f"{author} muted user ->  {user} for {time} minutes")
            await auditchannel.send(f"{author.mention} text muted user ->  {user.mention} for {time} minutes. Reason: {reason}")
          except Exception as e:
            print(e)
            await interaction.response.send_message(embed=unsuccessfulMuteError)
        else:
          await interaction.response.send_message(embed=unsuccessfulMuteTime)
      else:
        await interaction.response.send_message(embed=unsuccessfulMuteBot)
    else:
      await interaction.response.send_message(embed=unsuccessfulMuteSelf)
  else:
    await interaction.response.send_message(embed=unsuccessfulMutePermissions)


#
#Text Unmute
#

@bot.tree.command(name="tunmute", description="Text Unmutes a User")
@app_commands.describe(user="User to unmute")
async def tunmute(interaction: discord.Interaction, user:discord.User):
  author = interaction.user
  auditchannel = await bot.fetch_channel(audit_log_channel)

  successfulUnmute = discord.Embed(title=f":white_check_mark: User Successfully Unmuted!")

  unsuccessfulUnmuteError = discord.Embed(title=":x: Unexpected Error Occurred!")

  unsuccessfulUnmuteSelf = discord.Embed(title=":x: You cannot unmute yourself!")

  unsuccessfulUnmutePermissions = discord.Embed(title=":x: Missing Permissions!")

  unsuccessfulUnmuteBot = discord.Embed(title=":x: I cannot unmute myself!")

  unsuccessfulUnmuteNotMuted = discord.Embed(title=":x: User is not muted!")

  
  if author.guild_permissions.moderate_members:
    if user != author:
      if user != bot.user:
        if user.id in mutedUsers:
          try:
            pos = mutedUsers.index(user.id)
            temp = mutedUsersTime[pos]
            mutedUsers.remove(user.id)
            mutedUsersTime.remove(temp)
            await interaction.response.send_message(embed=successfulUnmute)
            print(f"{author} unmuted user ->  {user}")
            await auditchannel.send(f"{author.mention} text unmuted user ->  {user.mention}")
          except Exception as e:
            print(e)
            await interaction.response.send_message(embed=unsuccessfulUnmuteError)
        else:
          await interaction.response.send_message(embed=unsuccessfulUnmuteNotMuted)
      else:
        await interaction.response.send_message(embed=unsuccessfulUnmuteBot)
    else:
      await interaction.response.send_message(embed=unsuccessfulUnmuteSelf)
  else:
    await interaction.response.send_message(embed=unsuccessfulUnmutePermissions)





#Log the launch
try:
  launchLog = open("launchLog.txt", "a")
  launchLog.write(f"Launched on {datetime.datetime.now()}\n")
  launchLog.close()
except Exception as e:
  print("LaunchLog file most likely doesn't exist. Please create a file called 'launchLog.txt'!")

  print(e)



bot.run(TOKEN)

