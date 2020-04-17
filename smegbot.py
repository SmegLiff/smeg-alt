import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

ballcontent = [
    ":8ball: nope",
    ":8ball: lol no",
    ":8ball: nah"
    ":8ball: not happening ever",
    ":8ball: go ask ur mom",
    ":8ball: ok yeah i guess",
    ":8ball: maybe so",
    ":8ball: i don't think so, but i am not sure",
    ":8ball: 8ball machine :b:roke",
    ":8ball: yea definitely lol",
    ":8ball: isn't it obvious?",
    ":8ball: lmao yeah",
    ":8ball: yes"
]

client = discord.Client()

# @client.event
# async def on_ready():
#     # print(f'{client.user} has connected to Discord!')
#     print("haha cum")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "sex":
        await message.channel.send("sex")

    if message.content.startswith("8ball"):
        text = ballcontent[random.randint(0, len(ballcontent) - 1 )]
        await message.channel.send(text)


client.run(TOKEN)
