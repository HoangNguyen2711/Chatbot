
# - intent: buy_product
#   examples: |
#     - i want to order 
#     - want to order 
#     - want to order 
#     - get me a 
#     - need to buy  please
#     - want to purchase me buy pls
#     - buy 
from bs4 import BeautifulSoup
from rasa_sdk.events import SlotSet

import urllib.request 

url =  'https://guitar.com/news/'

page = urllib.request.urlopen(url)

soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find('h3',class_='entry-title td-module-title').find_all('a')

for feed in new_feeds:
	title = feed.get('title')
	link = feed.get('href')
	print('Latest new from guitar.com: {} - Link: {}'.format(title, link))


