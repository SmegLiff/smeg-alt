import random

def command(text):
    if text.startswith("help"):
        if random.randint(0,1): # 50% chance to say no
            return """
            ```
these commands do not require a prefix because why not
  8ball [text] - haha funny ball
  roll 4d6 + 2d3 - dice roll
  roll 1% * 1000% - teaches you how gacha is bullshit
  gelbooru [tag] [tag] - yes.
  e621 [tag] [tag] - somehow isn't working, why does e621 require complicated setups anyway?
  sex - sex.
  big [text] - makes things big

"serious" commands below require the prefix
  help - this
  captoggle - makes auto capitalization no longer cause your commands to fail to trigger
```"""   # well that is ugly
        else:
            return "no"
    if text.startswith("captoggle"):
        return """
https://www.google.com/search?q=android+disabling+auto+capitalization\n
https://www.google.com/search?q=ios+disabling+auto+capitalization
        """  # gottem