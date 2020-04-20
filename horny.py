import xml.etree.ElementTree as ET
import requests
import os
from dotenv import load_dotenv
load_dotenv()


headers = {
    "user-agent": "SmegAlt/1.0 (by Snekky on e621)",
}


def gelbooru(text):
    text = text.replace(" ", "+")
    GELBOORU_API = os.getenv('GELBOORU_API')
    text = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100" + GELBOORU_API + "&tags=" + text
    r = requests.get(text)
    xml = ET.fromstring(r.content)
    return xml.findall('post')

def e621(text):
    # text = text.replace(" ", "+")
    text = "https://e621.net/post/index.json"      # nothing works lol unepic
    r = requests.get(text, headers=headers)
    return "this should be working but it is not, " + str(r.status_code)
