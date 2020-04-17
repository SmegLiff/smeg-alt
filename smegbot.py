import os

import discord
from dotenv import load_dotenv
import random
import pyfiglet
import requests
import xml.etree.ElementTree as ET

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
    ":8ball: yes",
    ":8ball: no fuck you",
    ":8ball: no fuck off"
]

client = discord.Client()

# @client.event
# async def on_ready():
#     # print(f'{client.user} has connected to Discord!')
#     print("haha cum")
def randomlistitem(listname):
    return listname[random.randint(0, len(listname) - 1 )]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "sex" in message.content:
        await message.channel.send("sex")

    if message.content.startswith("8ball"):
        text = randomlistitem(ballcontent)
        await message.channel.send(text)

    if "big" in message.content:
        text = message.content.split("big", 1)[1]
        bigtext = pyfiglet.figlet_format(text)
        await message.channel.send("```\n" + bigtext + "\n```")

    if message.author.id == 365975655608745985: # Pokecord
        if message.content == "This is the wrong pokémon!":
            await message.channel.send("haha what a fucking retard")
        elif message.content.startswith("Congratulations"):
            await message.channel.send("wow ok nice reverse image search loser")
            await message.channel.send("ok now check the iv or ban")

    if message.content.startswith("gelbooru "):
        text = message.content.split("gelbooru ", 1)[1]
        text = text.replace(" ", "+")
        GELBOORU_API = os.getenv('GELBOORU_API')
        text = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100" + GELBOORU_API + "&tags=" + text
        r = requests.get(text)
        xml = ET.fromstring(r.content)
        posts = xml.findall('post')
        imgurl = []
        for post in posts:
            imgurl.append(post.attrib['file_url'])
        text = randomlistitem(imgurl)
        await message.channel.send(text)


client.run(TOKEN)
