#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from plugins.link_generator import get_short
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
import re
import requests as ree
from bs4 import BeautifulSoup

'''
Sample output(bunch link)
<a class="noSelect content" data-minutelytitle="Dance Karnataka Dance Season 7 - August 06, 2023" href="/tv-shows/details/dance-karnataka-dance-season-7/0-6-4z5349291/dance-karnataka-dance-season-7-august-06-2023/0-1-6z5403327"><img alt="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5403327/list/0000015567f16274865e439785f652b73fc99ff5.jpg" title="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" width="100%"/></a>
<a class="noSelect content" data-minutelytitle="Trinayani - August 07, 2023" href="/tv-shows/details/trinayani/0-6-3199/trinayani-august-07-2023/0-1-6z5407627"><img alt="Trinayani - August 07, 2023 Episode 795" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5407627/list/000001923292163834464dcba493c303e3d85a8e.jpg" title="Trinayani - August 07, 2023 Episode 795" width="100%"/></a>

'''
link1=[1]
listlink=[1]
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('notify'))
async def notify(client: Client, message: Message):
    while True:
        #kannada serials link
        url = ('https://www.zee5.com/tv-shows/collections/before-tv-episodes-zee-kannada/0-8-670')

        response = ree.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the HTML element that contains information about the latest episode
        episode_element = soup.find_all("a", class_="noSelect content", href=True)
        
        for l in episode_element:
            if l['href'] not in listlink:
                listlink.append(l['href'])
                
        #here we check the episode is new or not
        new_link = set(listlink).difference(set(link1))
        newlist=list(new_link)
        for i in newlist:
            link1.append(i)
            b=str(i)
            await client.send_message(message.chat.id, f"https://www.zee5.com{b}")
            # print(f"https://www.zee5.com{b}\n\n")
            await asyncio.sleep(5)
            
        #here we delete the old episode link(premium free)
        duplicatelinks = set(link1).difference(set(listlink))
        duplicatelist=list(duplicatelinks)
        for j in duplicatelist:
            link1.remove(j)
        notify(client,message)
        break
        
    
        # return notify(Client,Message)
            
@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.text & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
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

    await reply_text.edit(f"<b>Here is your link \n{tlink}\n\nPri᥎ᥲᴛᥱ ᥣiᥒκ 🔗\n<code>{tlink}</code> \n\n<b>𐍃ɦ᧐rᴛ ᥣiᥒκ😎</b>\n<code>{link}</code></b>")

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
