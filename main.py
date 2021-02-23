import discord
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check


client = discord.Client()

client = commands.Bot(command_prefix = '!') 

token = open("token.txt", "r")

@client.event
async def on_ready():
    print(f"{client.user} connected to Discord..") 
    await client.change_presence(activity=discord.Game("Yeff's Games"))

@client.command()
async def ping(ctx):
    await ctx.send("pong!") 

@client.command()
async def kick(ctx, member : discord.Member, *, reason):
        await member.kick(reason=None)
        
        kick_embed = discord.Embed(title=f"Kicked {member}", description=reason, color=discord.Color.red())

        await ctx.send(embed=kick_embed)

@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

@client.command()
async def create_channel(ctx, channel_name='custom-channel'):
    embed = discord.Embed(
           title=f"Channel Created by {ctx.author}",
           description=f"Channel Name: {channel_name}",
           color=discord.Color.green()
   )

    embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)

    guild = ctx.guild
    existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await ctx.send(embed=embed)
        await guild.create_text_channel(channel_name)
    else:
        await ctx.send("This channel already exists.")

@client.command()
async def delete_channel(ctx, channel_name):
   embed = discord.Embed(
           title=f"Channel Deleted by {ctx.author}",
           description=f"Channel Deleted: {channel_name}",
           color=discord.Color.green()
   )

   embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)

   # check if the channel exists
   existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)
   
   # if the channel exists
   if existing_channel is not None:
      await existing_channel.delete()
      await ctx.send(embed=embed)
   # if the channel does not exist, inform the user
   else:
      await ctx.send(f'No channel named "{channel_name}", was found')

def spam_check(ctx):
        return ctx.author.id == 765103623695892521

@commands.check(spam_check)
@client.command()
async def spam(ctx, user: discord.User):
        try:
         with open('rickroll.txt', 'r') as f:
                 for line in f:
                         await user.send(line)
                         time.sleep(1)

        except:
            await ctx.send("Spam failed, very sad.")

@client.command()
async def force_shutdown(ctx, reason = "None"):
        embed = discord.Embed(
           title=f"Commencing shutdown...",
           color=discord.Color.greyple()
   )
        
        embed.add_field(name="Reason:", value=reason, inline=True)

        await ctx.send(embed=embed)

        await client.logout()

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason):
        await member.send(f"Hey there! You were banned from {ctx.guild.name} for violating the rules!")
        await member.ban(reason=reason)
        embed = discord.Embed(
                title = "User Banned"
        )
        embed.add_field(name = "Banned User", value = member.mention, inline = True)
        embed.add_field(name = "Reason", value = reason, inline = True)

        await ctx.send(embed=embed);

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"Unbanned: {user.mention}")
            
            
client.run(token.read())
