#for sending msg to telegram 
from bot import Bot
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from config import ADMINS

#for extract the new episode link
import requests as ree
from bs4 import BeautifulSoup


import requests as ree
from bs4 import BeautifulSoup
import time

'''
Sample output(bunch link)
<a class="noSelect content" data-minutelytitle="Dance Karnataka Dance Season 7 - August 06, 2023" href="/tv-shows/details/dance-karnataka-dance-season-7/0-6-4z5349291/dance-karnataka-dance-season-7-august-06-2023/0-1-6z5403327"><img alt="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5403327/list/0000015567f16274865e439785f652b73fc99ff5.jpg" title="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" width="100%"/></a>
<a class="noSelect content" data-minutelytitle="Trinayani - August 07, 2023" href="/tv-shows/details/trinayani/0-6-3199/trinayani-august-07-2023/0-1-6z5407627"><img alt="Trinayani - August 07, 2023 Episode 795" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5407627/list/000001923292163834464dcba493c303e3d85a8e.jpg" title="Trinayani - August 07, 2023 Episode 795" width="100%"/></a>

'''
link1=[1]
listlink=[1]
def fun():
    while 1:
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
            global b
            b=str(i)
            print(f"https://www.zee5.com{b}\n\n")
            time.sleep(2)
            
        #here we delete the old episode link(premium free)
        duplicatelinks = set(link1).difference(set(listlink))
        duplicatelist=list(duplicatelinks)
        for j in duplicatelist:
            link1.remove(j)
