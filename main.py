# Strarted from this article: https://builtin.com/software-engineering-perspectives/discord-bot-python

import discord
import os
from dotenv import load_dotenv

load_dotenv()

x_root_path = "https://x.com/"
twitter_root_path = "https://twitter.com/"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

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
    root_path = ""
    if message.author.name == "fxtwitter converter" and message.author.bot == True:
        return

    if x_root_path in message.content and message.content != x_root_path:
        root_path = x_root_path
    elif twitter_root_path in message.content and message.content != twitter_root_path:
        root_path = twitter_root_path
	
    if root_path != "":
        fx_converted_links = "\n".join(get_xtwitter_links_from_msg(message.content, root_path)).replace(root_path, "https://fxtwitter.com/")
        await message.channel.send(f"Here, have an embed for that:\n{fx_converted_links}", reference=message.to_reference(), mention_author=False)
		
def get_xtwitter_links_from_msg(message, root_path):
    links = []
    split_msg = message.split()
    for item in split_msg:
        if root_path in item:
            links.append(item)
    return links

bot.run(DISCORD_TOKEN)