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
        await send_converted_links(message, fx_converted_links)

		
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
            await message.channel.send(f"Here, have an embed for that:\n{newline.join(fx_converted_links)}", 
                                       reference=message.to_reference(), 
                                       mention_author=False)
        elif link_count <= 5:
            await message.channel.send(f"Here, have some embeds for those:\n{newline.join(fx_converted_links)}", 
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
                        await message.channel.send(f"Here, have some embeds for those:\n{newline.join(converted_link_queue)}", 
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