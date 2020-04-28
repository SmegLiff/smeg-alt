import random

def infocommand(text, author = None):
    if author != None:
        author = str(author)
    if text == "help":

        if random.randint(0,1): # 50% chance to say no
            return """
            ```
these commands do not require a prefix because why not
  8ball text - haha funny ball
  roll 4d6 + 2d3 - dice roll
  roll 1% * 1000% - teaches you how gacha is bullshit
  gelbooru[amount of posts] tag tag - yes.
  e621 tag tag - somehow isn't working, why does e621 require complicated setups anyway?
  sex - sex.
  big text - makes things big
  poger - alias of smeg play poker

"serious" commands below require the prefix
  help - this
  captoggle - makes auto capitalization no longer cause your commands to fail to trigger
  play - epic gaming moment, do smeg help play for more info
  cancel - cancel some prompts, like games (probably broken somehow)
```"""   # well that is ugly
        else:
            if random.randint(0,1):
                return "no"
            else:
                output = "shut up " + author[:-5]
                return output

    elif text.startswith("help "):
        text = text.replace("help ", "")
        if text == "play":
            return """```
  rps - plays rock paper scissors
  poker - draw poker, 2 players
  strippoker - owo
            ```"""



    if text.startswith("captoggle"):
        return """
https://www.google.com/search?q=android+disabling+auto+capitalization\n
https://www.google.com/search?q=ios+disabling+auto+capitalization
        """  # gottem
