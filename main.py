# Strarted from this article: https://builtin.com/software-engineering-perspectives/discord-bot-python

import discord
import os
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

x_root_path = "https://x.com/"
twitter_root_path = "https://twitter.com/"
fxtwitter_root_path = "https://fxtwitter.com/"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MY_GUILD_ID_LIST = os.getenv("MY_GUILD_ID_LIST")
DEV_ACTIVE = int(os.getenv("DEV_ACTIVE"))

guild_ids = [int(guild_id.strip()) for guild_id in MY_GUILD_ID_LIST.split(",") if guild_id.strip()]

# Took class from: https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        if DEV_ACTIVE == 1:
            self.tree.copy_global_to(guild=discord.Object(id=guild_ids[0]))
            await self.tree.sync(guild=discord.Object(id=guild_ids[0]))
        else:
            for guild_id in guild_ids:
                self.tree.copy_global_to(guild=discord.Object(id=guild_id))
                await self.tree.sync(guild=discord.Object(id=guild_id))

intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents)

@bot.tree.command()
@app_commands.describe(link='Your x.com or twitter.com link(s) you want to convert')
async def convert(interaction: discord.Interaction, link: str):
    """Converts up to five x.com or twitter.com links into a fxtwitter.com links (5 links at once is my max)"""
    x_or_twitter_link_present = False
    if ((x_root_path in link and link != x_root_path)
        or (twitter_root_path in link and link != twitter_root_path)):
        x_or_twitter_link_present = True
	
    if x_or_twitter_link_present == True:
        converted_links = "\n".join(convert_links_to_fxtwitter_root(link))
        await interaction.response.send_message(f'{converted_links}')
    else:
        await interaction.response.send_message(f'Give a link to convert, dummy')

@bot.event
async def on_ready():
    server_count = 0
    for server in bot.guilds:
        print(f"- {server.id} (name: {server.name})")
        server_count += 1
    
    if server_count == 0:
        print("fxtwitter converter is not in any servers.")
    elif server_count == 1:
        print("fxtwitter converter is in 1 server.")
    else:
        print(f"fxtwitter converter is in {server_count} servers.")

@bot.event
async def on_message(message):
    referenced_message = None
    x_or_twitter_link_present = False

    if(not bot.user.mentioned_in(message)):
        return

    if ((message.reference is not None) and bot.user.mentioned_in(message)):
        referenced_message = await message.channel.fetch_message(message.reference.message_id)

    if ((referenced_message is not None) 
        and ((x_root_path in referenced_message.content and referenced_message.content != x_root_path)
                or (twitter_root_path in referenced_message.content and referenced_message.content != twitter_root_path))):
        x_or_twitter_link_present = True
	
    if x_or_twitter_link_present == True:
        fx_converted_links = convert_links_to_fxtwitter_root(referenced_message.content)
        await send_converted_links(referenced_message, fx_converted_links)

		
def get_xtwitter_links_from_msg(message):
    links = []
    split_msg = message.split()
    for item in split_msg:
        if ((x_root_path in item) or (twitter_root_path in item)):
            links.append(item)
    return links

def convert_links_to_fxtwitter_root(message):
    converted_links = []
    links = get_xtwitter_links_from_msg(message)
    for link in links:
        path = ""
        if x_root_path in link:
            path =  x_root_path
        elif twitter_root_path in link:
            path =  twitter_root_path
        
        if path != "":
            converted_links.append(link.replace(path, fxtwitter_root_path))
    return converted_links

async def send_converted_links(message, fx_converted_links):
        newline = "\n"
        link_count = len(fx_converted_links)
        converted_link_queue = []
        
        if link_count == 1:
            await message.channel.send(f"{newline.join(fx_converted_links)}", 
                                       reference=message.to_reference(), 
                                       mention_author=False)
        elif link_count <= 5:
            await message.channel.send(f"{newline.join(fx_converted_links)}", 
                                       reference=message.to_reference(), 
                                       mention_author=False)
        else:
            links_in_queue = 0
            first_msg_sent = False
            for link in fx_converted_links:
                converted_link_queue.append(link)
                links_in_queue += 1
                if links_in_queue == 5:
                    links_in_queue = 0
                    if first_msg_sent == False:
                        await message.channel.send(f"{newline.join(converted_link_queue)}", 
                                                   reference=message.to_reference(), 
                                                   mention_author=False)
                        first_msg_sent = True
                        converted_link_queue.clear()
                    else:
                        await message.channel.send(f"\n{newline.join(converted_link_queue)}")
                        converted_link_queue.clear()
            if len(converted_link_queue) != 0:
                await message.channel.send(f"\n{newline.join(converted_link_queue)}")
                converted_link_queue.clear()
                

bot.run(DISCORD_TOKEN)