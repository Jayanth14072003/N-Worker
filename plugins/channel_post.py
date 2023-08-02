#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from plugins.link_generator import get_short
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
import requests as ree
from bs4 import BeautifulSoup
import re

def fun(a):
    url = ('https://www.zee5.com/tv-shows/details/gattimela/0-6-1392/episodes')

    response = ree.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the HTML element that contains information about the latest episode
    episode_element1 = soup.find_all("div", class_="showDuration")
    episode_element2 = soup.find_all("a", class_="noSelect content")
    en1 = "Episode "+a
    for i in episode_element2:
        s=str(i)
        if re.search(en1,s):
            p = str(re.findall('https://+.*."\st',s))
            global photo
            photo = re.sub("w_+.*eco/","", p[2:-5])
            break
    en2 = "E"+a
    for i in episode_element1:
        ss=str(i)
        if re.search(en2,ss):
            global d
            d = str(re.findall("\d+\s\w+",ss))
            global date
            date = d[-5:-2]
            break
            
    return photo,d,date

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    # prefname = re.sub(r'(_)', ' ', str(message.video.file_name))
    # fname = prefname.split('S')[0]
    ena=str(re.findall(r"E\d+",str(message.video.file_name)))
    en=str(re.findall(r"\d+",ena))
    reply_text = await message.reply_photo(photo=fun(en)[0],caption="Please wait...")
    en = None
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    tlink = f"https://telegram.me/{client.username}?start={base64_string}"
    link = get_short(tlink)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=link)]]) 
    
    await reply_text.edit(f"<b>Here is your link \n{tlink}\n{fun("1130")[1][2:-6]+"-"+dm[date]+"- 2023"}\nPri᥎ᥲᴛᥱ ᥣiᥒκ 🔗\n<code>{tlink}</code> \n\n<b>𐍃ɦ᧐rᴛ ᥣiᥒκ😎</b>\n<code>{link}</code></b>")

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = get_short(f"https://telegram.me/{client.username}?start={base64_string}")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=link)]])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
