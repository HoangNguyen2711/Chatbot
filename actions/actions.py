# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup
from rasa_sdk.events import SlotSet

import requests
import mariadb
import urllib.request 

    
mydb =  mariadb.connect(
  host="localhost",
  user="root",
  password="",
  database="guitarstoree"
)

class Hello(Action):

    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello There!")

        return []

class ask_weather(Action):
    def name(self) -> Text:
        return "action_weather"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en'}
        city= 'cantho'
        city = city+'+weather'
        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        dispatcher.utter_message(location)
        dispatcher.utter_message(info + ' at: '+ time.lower())
        dispatcher.utter_message('Average temperature: '+weather+"°C")

class news(Action):

    def name(self) -> Text:
        return "action_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url =  'https://www.guitarworld.com/news'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        new_feeds = soup.find('div', class_='content').find_all('h3', class_='article-name')
        dispatcher.utter_message('Latest news from Guitarworld:')
        for feed in list(new_feeds):
            feed_result= feed.find('a')
            title = feed_result.contents[0]
            link = feed_result.get('href')
            dispatcher.utter_message('{} \nMore: {}'.format(title, url+link))


class Coupon(Action):

    def name(self) -> Text:
        return "action_coupon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cur = mydb.cursor()
        cur.execute("SELECT name, vale, expery_date FROM coupons")
        myresult = cur.fetchall()

        if len(myresult) >= 1:
            dispatcher.utter_message("We have: ")
            for x in myresult:
                dispatcher.utter_message(x[0]+' ' + str(int(x[1])) +'%')
        else:
            dispatcher.utter_message("There are no promotions at the moment!")

