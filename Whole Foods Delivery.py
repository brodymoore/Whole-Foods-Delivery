import bs4
from selenium import webdriver
import sys
import time
import os
from datetime import datetime

from twilio.rest import Client

# Insert information for Twilio API below
# account_sid = ""
# auth_token = ""
# from_number = ""
# to_number = ""
client = Client(account_sid, auth_token)

# Insert information for amazon path
# amazon_path = ""

def getWFSlot(url):

   driver = webdriver.Chrome(executable_path="Insert chromedriver path")
   driver.get(url)           
   no_open_slots = True

   while no_open_slots:
      time.sleep(30)
      driver.refresh()
      current_time = datetime.now().strftime("%H:%M:%S")
      print("Refreshed at",current_time)
      html = driver.page_source
      soup = bs4.BeautifulSoup(html,'lxml')
      try:
            day = soup.find_all("div",class_ = "ufss-date-select-toggle-text-month-day")
            availability = soup.find_all("div",class_ = "ufss-date-select-toggle-text-availability")
            for i in range(3):
               if availability[i].text.strip() != "Not available":
                  
                  day = soup.find_all("div",class_ = "ufss-date-select-toggle-text-month-day")
                  day = day[i].text.strip()
                  
                  deliv_time = soup.find_all("span",class_ = "ufss-aok-offscreen")
                  available = deliv_time[0].text.strip()

                  message = "There is a delivery available on " + day + " at this time range: " + available
                  client.messages.create(from_=from_number, 
                                 to=to_number, 
                                 body=message)
                  print(message)
                  f = open("test2.html",'w')
                  f.write(str(soup))
                  f.close
                  no_open_slots = False
      except AttributeError:
         continue
getWFSlot(amazon_path)