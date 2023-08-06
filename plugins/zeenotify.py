import requests as ree
from bs4 import BeautifulSoup
# import re
'''
Sample output(bunch link)
<a class="noSelect content" data-minutelytitle="Dance Karnataka Dance Season 7 - August 06, 2023" href="/tv-shows/details/dance-karnataka-dance-season-7/0-6-4z5349291/dance-karnataka-dance-season-7-august-06-2023/0-1-6z5403327"><img alt="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5403327/list/0000015567f16274865e439785f652b73fc99ff5.jpg" title="Dance Karnataka Dance Season 7 - August 06, 2023 Episode 30" width="100%"/></a>
<a class="noSelect content" data-minutelytitle="Trinayani - August 07, 2023" href="/tv-shows/details/trinayani/0-6-3199/trinayani-august-07-2023/0-1-6z5407627"><img alt="Trinayani - August 07, 2023 Episode 795" crossorigin="anonymous" src="https://akamaividz2.zee5.com/image/upload/w_522,h_294,c_scale,f_webp,q_auto:eco/resources/0-1-6z5407627/list/000001923292163834464dcba493c303e3d85a8e.jpg" title="Trinayani - August 07, 2023 Episode 795" width="100%"/></a>

'''

link1=''
def fun():
    while 1:
        #kannada serials link
        url = ('https://www.zee5.com/tv-shows/collections/before-tv-episodes-zee-kannada/0-8-670')

        response = ree.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the HTML element that contains information about the latest episode
        episode_element = soup.find_all("a", class_="noSelect content", href=True)
        
        #here we check the episode is new or not 
        if link1 != episode_element[0]:
            link = episode_element[0]
            globals()['link1']=link

            #here we extract the perticuler episode link 
            b=str(link['href'])
            "https://www.zee5.com"+b
fun()
