import json 
import asyncio
import discord
from discord.ext import commands 
from discord import Status, Activity, ActivityType
from webserver import keep_alive
import os
import random
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

  
WHITELISTER_ROLE = "Whitelister" #Replace with role that can whitelist people 
bot_status = "Whitelisting people" #Replace with the bot status you want to be showed up on bot , current status that will be showed up is Playing Whitelisting People 
VIP_ROLE_NAME = "Vip" #Replace with the role that will be assigned once whitelisted
STAFFROLE = "Staff"
 # Replace with your staff roles
LOG_CHANNEL_ID = 1115276037526397078  # Replace with your log channel ID
JSONFILE = "file name" #Replace with your file name example ips.json
# Load existing data from the JSON file
with open(JSONFILE, "r") as json_file:
    existing_data = json.load(json_file)
@bot.event
async def on_ready():
    await bot.change_presence(status=Status.online,
                              activity=Activity(type=ActivityType.playing, name=bot_status))
    print(f"Bot is ready. Logged in as {bot.user.name}")


#  Whitelist command

@bot.command()
@commands.has_role(WHITELISTER_ROLE)  # Check if the user has the Whitelister role
async def add(ctx, username, user_mention):
    user_id = user_mention.strip("<@!>")
    member = ctx.guild.get_member(int(user_id))
    vip_role = discord.utils.get(ctx.guild.roles, name=VIP_ROLE_NAME)

    if vip_role and member:
        if username not in existing_data:  # Check if username already exists
            existing_data.append(username)
            await member.add_roles(vip_role)
            embed = discord.Embed(
                title=f'__{ctx.author.mention}__',
                description=f'✅ Successfully whitelisted {username} and gave the VIP role to {member.mention}',
                color=discord.Color.random()
            )
            await ctx.send(ctx.author.mention, embed=embed)
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed9 = discord.Embed(
                    title=f'__{ctx.author.mention}__',
                    description=f'✅ {ctx.author.mention} whitelisted {username} and assigned the VIP role to {member.mention}',
                    color=discord.Color.random()
                )
                await log_channel.send(embed=embed9)
        else:
            embed2 = discord.Embed(
                title=f'__{ctx.author.mention}__',
                description=f'❌ {username} is already whitelisted!',
                color=discord.Color.random()
            )
            await ctx.send(ctx.author.mention, embed=embed2)
    else:
        embed3 = discord.Embed(
            title=f'__{ctx.author.mention}__',
            description=f'❌ Unable to find the user/VIP role',
            color=discord.Color.random()
        )
        await ctx.send(ctx.author.mention, embed=embed3)

    # Write the updated data back to the JSON file
    with open(JSONFILE, "w") as json_file:
        json.dump(existing_data, json_file)

@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(
            title=f'__{ctx.author.mention}__',
            description='❌ You don\'t have permissions to do that',
            color=discord.Color.random()
        )
        await ctx.channel.send(ctx.author.mention, embed=embed)

# Chat Log Command
@bot.event
async def on_message_delete(message):
    # Check if the author is the server owner, a staff role, or the bot itself
    if message.author == message.guild.owner or message.author == bot.user:
        return
    
    # Create and send the embed when a message is deleted
    embed = discord.Embed(
        title="Message Deleted",
        description=f"Author: {message.author.mention}",
        color=discord.Color.red()
    )
    embed.add_field(name="Original", value=message.content)
    
    # Check if the message has any attachments (images)
    if len(message.attachments) > 0:
        embed.set_image(url=message.attachments[0].url)
        
    channel = bot.get_channel(LOG_CHANNEL_ID)
    await channel.send(embed=embed)
# Send log on message modified command
@bot.event
async def on_message_edit(before, after):
    # Check if the author is the server owner, a staff role, or the bot itself
    if after.author == after.guild.owner or after.author == bot.user:
        return
    
    # Create and send the embed when a message is edited
    embed = discord.Embed(
        title="Message Edited",
        description=f"Author: {after.author.mention}",
        color=discord.Color.orange()
    )
    embed.add_field(name="Original Content", value=before.content)
    embed.add_field(name="Updated Content", value=after.content)
    
    # Check if the edited message has any attachments (images)
    if len(after.attachments) > 0:
        embed.set_image(url=after.attachments[0].url)
        
    channel = bot.get_channel(LOG_CHANNEL_ID)  # Replace with your channel ID
    await channel.send(embed=embed)
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="List of available commands:",
        color=discord.Color.random()
    )
    embed.add_field(name="!add <Whitelist Type> <@user_mention>", value="Whitelist a user and assign the VIP role")
    
    # Add more fields for other commands if needed if you are too dumb to do that ask chat gpt to fix your code 

    await ctx.send(embed=embed)

# run keep_alive function 
keep_alive()
# Here is an important part , to make your bot more secure , create a replit secret : WATCH TUT if too dumb
token = os.environ.get('TOKEN')
bot.run(token)








