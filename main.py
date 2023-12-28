# Strarted from this article: https://builtin.com/software-engineering-perspectives/discord-bot-python

import discord
import os
from dotenv import load_dotenv

load_dotenv()

x_root_path = "https://x.com/"
twitter_root_path = "https://twitter.com/"
fxtwitter_root_path = "https://fxtwitter.com/"

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
    x_or_twitter_link_present = False
    if ((message.author.name == "fxtwitter converter" 
         or message.author.name == "fxtwitter converter dev") 
         and message.author.bot == True):
        return

    if ((x_root_path in message.content and message.content != x_root_path)
        or (twitter_root_path in message.content and message.content != twitter_root_path)):
        x_or_twitter_link_present = True
	
    if x_or_twitter_link_present == True:
        fx_converted_links = convert_links_to_fxtwitter_root(message.content)
        await message.channel.send(f"Here, have an embed for that:\n{fx_converted_links}", reference=message.to_reference(), mention_author=False)
		
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
    return "\n".join(converted_links)

bot.run(DISCORD_TOKEN)