import discord
import asyncio
import random
import time
import os
from discord.ext import commands

# Replace 'YOUR_TOKEN' with your Discord bot token
TOKEN = 'YOUR_TOKEN'

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

def clr():
    os.system("cls")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    print("1. Create channels and send messages")
    print("2. Delete all channels")
    print("3. Exit")

    while True:
        option = input("Select an option (1-3): ")

        if option == "1":
            try:
                server_id = input("Enter the server ID where you want to create the channels: ")
                num_channels = int(input("Enter the number of channels to create: "))
                channel_names = input("Enter the channel names (comma-separated): ").split(",")
                num_messages = int(input("Enter the number of messages to send in each channel: "))
                message_contents = input("Enter the message contents (comma-separated): ").split(",")

                guild = bot.get_guild(int(server_id))
                if guild is not None:
                    created_channels = []
                    for _ in range(num_channels):
                        new_channel_name = random.choice(channel_names).strip()
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
                        task = asyncio.create_task(send_messages(channel, num_messages, message_contents))
                        tasks.append(task)

                    await asyncio.gather(*tasks)

                    print("1. Delete all channels")
                    print("2. Exit")

                    while True:
                        option = input("Select an option (1-2): ")

                        if option == "1":
                            try:
                                server_id = input("Enter the server ID where you want to delete all channels: ")
                                guild = bot.get_guild(int(server_id))
                                if guild is not None:
                                    confirm = input("y/n: ")
                                    if confirm.lower() == "y":
                                        for channel in guild.channels:
                                            await channel.delete()
                                        print("All channels have been deleted.")
                                        time.sleep(2)
                                        clr()
                                        
                                    else:
                                        print("Deletion canceled.")
                                else:
                                    print(f'Could not find the server with ID "{server_id}"')
                                break
                            except ValueError:
                                print("Invalid input. Please try again.")
                        elif option == "2":
                            print("Exiting...")
                            break
                        else:
                            print("Invalid option. Please select again.")

                    break
                else:
                    print(f'Could not find the server with ID "{server_id}"')
            except ValueError:
                print("Invalid input. Please try again.")
        elif option == "2":
            try:
                server_id = input("Enter the server ID where you want to delete all channels: ")
                guild = bot.get_guild(int(server_id))
                if guild is not None:
                    confirm = input("y/n: ")
                    if confirm.lower() == "y":
                        for channel in guild.channels:
                            await channel.delete()
                        print("All channels have been deleted.")
                        time.sleep(2)
                        clr()
                    else:
                        print("Deletion canceled.")
                else:
                    print(f'Could not find the server with ID "{server_id}"')
            except ValueError:
                print("Invalid input. Please try again.")
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select again.")


async def send_messages(channel, num_messages, message_contents):
    for _ in range(num_messages):
        message_content = random.choice(message_contents).strip()
        await channel.send(message_content)


bot.run(TOKEN)
