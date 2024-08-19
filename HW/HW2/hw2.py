#!/home/nath/Documents/python_environments/nath/bin/python3

from bs4 import BeautifulSoup
import urllib
import urllib.request
import csv
import time
import re
import pandas as pd
from datetime import datetime
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options

web_prefix = 'https://www.presidency.ucsb.edu'
url = 'https://www.presidency.ucsb.edu/documents/app-categories/presidential/spoken-addresses-and-remarks?items_per_page=60&page='
speeches = []

for i in range(0,1000):
    print("Getting page " + str(i) + " ...")
    time.sleep(1)
    web_page = urllib.request.urlopen(url + str(i))
    soup = BeautifulSoup(web_page.read(), 'html.parser')
    divs_with_about = soup.find_all('div', about=True)
    speech_links = [div['about'] for div in divs_with_about]
    for speech_link in speech_links:
        speeches.append(speech_link)
    top_date = soup.find('span', class_="date-display-single").get_text()
    if("2020" in top_date):
        break

dates, titles, texts, citations = [], [], [], []
for speech in speeches:
    print("Getting: " + speech)
    web_page = urllib.request.urlopen(web_prefix + speech)
    time.sleep(3)
    soup = BeautifulSoup(web_page.read(), 'html.parser')
    title = soup.find('div', class_="field-ds-doc-title").get_text()
    text = soup.find('div', class_="field-docs-content").get_text()
    date = soup.find('span', class_="date-display-single").get_text()
    date = datetime.strptime(date, "%B %d, %Y")
    formatted_date = date.strftime("%Y-%m-%d")
    president = soup.find('h3', class_="diet-title").get_text()
    citation = ""    
    try:
        citation = soup.find('p', class_="ucsbapp_citation").get_text()
    except:
       pass 
    
    dates.append(date)
    titles.append(title)
    texts.append(text)
    citations.append(citation)

df = pd.DataFrame({'title': titles, 
                   'date': dates,
                   'text': texts,
                   'citation': citations,
                  })

# filter by date and president
df = df[df['president'] == "Joe Biden"]
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'].between("2021-01-20","2024-12-12")]

df.to_csv('jrb_pres_speeches.csv')

