import xml.etree.ElementTree as ET
import requests
import os
import re
from dotenv import load_dotenv
load_dotenv()


headers = {
    "user-agent": "SmegAlt/1.0 (by Snekky on e621)",
}


def gelbooru(text):
    if text.startswith("["):
        amount = re.search("(?<=\[).+?(?=\])", text) # i still don't know regex and just rely on stackoverflow
        amount = amount.group(0)
        try:
            amount = int(amount)
            if amount > 100: amount = 100
        except ValueError: # someone is trying to break the bot again
            amount = 1
        text = re.sub("\[.*?\]", "", text)
    else:
        amount = 1
    text = text.replace(" ", "+")
    GELBOORU_API = os.getenv('GELBOORU_API')
    text = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100" + GELBOORU_API + "&tags=" + text
    r = requests.get(text)
    xml = ET.fromstring(r.content)
    returnvalue = {"posts": xml.findall("post"), "amount": amount}
    return returnvalue
