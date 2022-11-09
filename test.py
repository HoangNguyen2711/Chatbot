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

# Python program to convert a list
# to string using join() function
   

def listToString(s):
   
    str1 = " "
   
    return (str1.join(s))

class Category(Action):

        cur = mydb.cursor()
        cur.execute("SELECT name FROM categories WHERE parent_id is not null")
        myresult = cur.fetchall()


        print("We have these coupons: ")
        for x in myresult:

            print(listToString(x))


        