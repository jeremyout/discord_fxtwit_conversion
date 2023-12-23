# Strarted from this article: https://builtin.com/software-engineering-perspectives/discord-bot-python

import discord
import os
from dotenv import load_dotenv

load_dotenv()

x_root_path = "https://x.com/"

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
    if message.author.name == "fxtwitter converter" and message.author.bot == True:
        return 
	
    if x_root_path in message.content and message.content != x_root_path:
        fx_converted_link = get_x_link_from_msg(message.content).replace(x_root_path, "https://fxtwitter.com/")
        await message.channel.send(f"Here, have an embed for that:\n{fx_converted_link}", reference=message.to_reference(),mention_author=False)
		
def get_x_link_from_msg(message):
    split_msg = message.split()
    print(split_msg)
    for item in split_msg:
        if x_root_path in item:
            return item

bot.run(DISCORD_TOKEN)