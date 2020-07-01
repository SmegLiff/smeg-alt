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
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_SERVER_1 = os.getenv("TARGET_SERVER_1")
OUTPUT_CHANNEL_1 = os.getenv("OUTPUT_CHANNEL_1")

reading_reply = False
player_1 = None
player_2 = None
playing = None

rps = ("rock", "paper", "scissors")

ball_content = (
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
)

client = discord.Client()


def random_list_item(list_name, amount=1):
    list_ = list_name[:]  # copies the input list to pop
    output = []

    for i in range(amount):
        output.append(list_.pop(random.randint(0, len(list_) - 1)))

    return output


def strip_prefix(text, prefix):  # it looks better ok
    return text.split(prefix, 1)[1]


class StupidInput(Exception):
    pass


lurk_channel = None


@client.event
async def on_ready():
    global lurk_channel

    print(f"We have logged in as {client.user}")
    game = discord.Game("smeg help")

    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    global reading_reply
    global player_1, player_2
    global playing

    if message.author == client.user:
        return

    if message.guild is None:  # DM
        if playing == 1 and player_2 is not None:
            if len(message.content) > 1 and "0" in message.content:
                await client.get_user(message.author.id).send("play the game properly you moron, you picked `0` then")

                card_input = "0"
            else:
                try:
                    int(message.content)
                    card_input = message.content
                except ValueError:
                    await client.get_user(message.author.id).send(
                        "play the game properly you moron, you picked `0` then")

                    card_input = "0"
            if message.author == player_1:
                ready = poker.discard("p1", card_input)
            elif message.author == player_2:
                ready = poker.discard("p2", card_input)

            if ready != "no":  # lol
                channel, player_1_hand, player_2_hand, winner, winner_value = ready

                player_1_hand = ", ".join(player_1_hand)
                player_2_hand = ", ".join(player_2_hand)

                player_1 = str(player_1)[:-5]
                player_2 = str(player_2)[:-5]

                if winner == 1:
                    win_text = player_1 + "** wins with **" + winner_value[2]
                elif winner == 2:
                    win_text = player_2 + "** wins with **" + winner_value[2]
                else:
                    win_text = "it's a tie"

                text = f"{player_1}'s hand: {player_1_hand}\n{player_2}'s hand: {player_2_hand}\n**{win_text}!**"

                await channel.send(text)

                reading_reply = False
                player_1 = None
                player_2 = None
                playing = None
    else:  # Server
        if message.author in (player_1, player_2) and reading_reply:
            if message.content == "smeg cancel":
                reading_reply = False
                player_1 = None
                player_2 = None
                playing = None

            if playing == 0:  # RPS
                if message.content in rps:
                    pick = random_list_item(rps)[0]

                    pick_index = rps.index(pick)
                    user_pick = rps.index(message.content)

                    if pick_index - user_pick == 1 or user_pick - pick_index == 2:
                        await message.channel.send(f"haha i picked {pick} i won you noob")
                    elif user_pick - pick_index == 1 or pick_index - user_pick == 2:
                        await message.channel.send(f"ok i picked {pick} you won chronbratgulasions")
                    else:
                        await message.channel.send(f"i picked {pick} so we tied and that's stupid")

                    reading_reply = False
                    player_1 = None
                    player_2 = None
                    playing = None
                else:
                    await message.channel.send("play the game properly you moron")

                    reading_reply = False
                    player_1 = None
                    player_2 = None
                    playing = None

        # spies on a certain server, and copies messages into another server
        if message.guild.id == int(TARGET_SERVER_1):
            # it's a test feature, i don't actually do anything with the chat log yet
            header = f"#{message.channel} - [{message.author}] {str(message.created_at.utcnow())[0:-7]} UTC\n"
            channel = client.get_channel(int(OUTPUT_CHANNEL_1))  # output channel

            await channel.send(header + message.content)

        if message.content.startswith("smeg "):
            text = strip_prefix(message.content, "smeg ")

            if text.startswith("play "):  # gamer mode
                text = strip_prefix(text, "play ")
                if playing is not None:
                    await message.channel.send("no")
                elif text.startswith("rps"):
                    reading_reply = True
                    player_1 = message.author
                    playing = 0

                    await message.channel.send("ok say `rock` `paper` or `scissors`")
                elif text.startswith("poker"):
                    reading_reply = True
                    player_1 = message.author
                    playing = 1

                    await message.channel.send("waiting for player 2...\nplayer 2 type `smeg join` to join")
                elif text.startswith("strip poker"):
                    await message.channel.send("https://spnati.net/")
            elif text == "join":
                if reading_reply:
                    if message.author != player_1:
                        player_2 = message.author
                        reading_reply = False

                        await message.channel.send("alright, sending your hands to DMs")

                        hand = poker.play(message.channel)
                        hand_1 = ", ".join(hand[0])
                        hand_2 = ", ".join(hand[1])

                        await client.get_user(player_1.id).send(
                            f"your hand is: {hand_1}\n type the cards that you want to change (1-5) for example `134` type `0` to keep all cards"
                        )
                        await client.get_user(player_2.id).send(
                            f"your hand is: {hand_2}\n type the cards that you want to change (1-5) for example `134` type `0` to keep all cards"
                        )
                    else:
                        await message.channel.send("what")
                else:
                    await message.channel.send("wtf are you trying to join")
            else:
                try:
                    text = infocommand(text, message.author)
                    if text != "":
                        await message.channel.send(text)
                except AttributeError:
                    return

        if "sex" in message.content.lower():
            await message.channel.send("sex")

        if message.content.lower().startswith("8ball"):
            text = random_list_item(ball_content)[0]

            await message.channel.send(text)

        if "big" in message.content.lower():
            text = strip_prefix(message.content, "big")

            if text[0] == " ":
                text = strip_prefix(text, " ")

            big_text = pyfiglet.figlet_format(text)

            await message.channel.send("```\n" + big_text + "\n```")

        if message.author.id == 365975655608745985:  # Pokecord
            if message.content == "This is the wrong pokémon!":
                await message.channel.send("haha what a fucking retard")
            elif message.content.startswith("Congratulations"):
                await message.channel.send("wow ok nice reverse image search loser")
                await message.channel.send("ok now check the iv or ban")

        if message.content.lowe().startswith("gelbooru"):
            if message.channel.is_nsfw():
                text = strip_prefix(message.content, "gelbooru")
                api_result = horny.gelbooru(text)

                try:
                    image_url = []

                    for post in api_result.get("posts"):
                        image_url.append(post.attrib['file_url'])

                    text = random_list_item(image_url, api_result.get("amount"))
                    text = "\n".join(text)

                    if len(text) > 2000:
                        await message.channel.send("that's too much, coomer")
                    else:
                        await message.channel.send(text)
                except (ValueError, IndexError):
                    await message.channel.send(
                        "ok either you don't know how to search properly or your little kink is too stupid to be found")
            else:
                await message.channel.send("horny")

        if message.content.lower().startswith("e621 "):
            if message.channel.is_nsfw():
                text = strip_prefix(message.content, "e621 ")
                posts = horny.e621(text)

                await message.channel.send(posts)
            else:
                await message.channel.send("horny")

        if message.content.lower().startswith("roll "):
            text = strip_prefix(message.content, "roll ")

            if "d" in text:  # standard dice notation with basic arithmetic
                split_text = re.split("([-+*/])", text)
                result = split_text[:]  # copies value
                for dice_roll in split_text[::2]:  # even indices
                    if "d" not in dice_roll:  # the notation is wrong somehow
                        await message.channel.send("good job dumbass you messed up the notation")
                        return 0

                    dice_calc = dice_roll.split("d")
                    sub_result = 0

                    if dice_calc[0] == "":
                        dice_calc[0] = 1

                    for i in range(0, int(dice_calc[0])):
                        sub_result += random.randint(1, int(dice_calc[1]))

                    for index, value in enumerate(result):
                        if value == dice_roll:
                            result[index] = str(sub_result)
                final_result = eval("".join(result))

                await message.channel.send(f":game_die: **{final_result}**")

            if "%" in text:
                split_text = re.split("([-+*/])", text)
                result = split_text[:]  # copies value

                for percentage in split_text[::2]:  # even indices
                    if "%" not in percentage:  # the notation is wrong somehow
                        await message.channel.send("good job dumbass you messed up the notation")
                        return 0

                    fraction = str(round(float(percentage.replace("%", ""))) / 100)

                    for index, value in enumerate(result):
                        if value == percentage:
                            result[index] = str(fraction)
                final_result = int(eval("".join(result)) * 100)

                if random.randint(1, 100) <= final_result:
                    rng_bool = ":white_check_mark:"
                else:
                    rng_bool = ":negative_squared_cross_mark:"
                await message.channel.send(f":game_die: **{final_result}%**: {rng_bool}")

        if message.content.lower() == "poger":
            reading_reply = True
            player_1 = message.author
            playing = 1

            await message.channel.send("waiting for player 2...\nplayer 2 type `smeg join` to join")


client.run(TOKEN)
