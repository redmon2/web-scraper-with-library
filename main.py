from pymongo import MongoClient
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
import os
import requests
import pytz

client_url = 'mongodb://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/apnews?authSource=admin'
db_client = MongoClient(client_url,27017)

central = pytz.timezone('America/Chicago')
now = datetime.now(central)
year = now.strftime("%Y")
month = now.strftime("%Y-%m")
day = now.strftime("%Y-%m-%d")
hour = now.strftime("%H")

page_url = "https://apnews.com/us-news"
element_tag = "h3"
element_class = "PagePromo-title"
num_headlines = 3

page_to_scrape = requests.get(page_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

def save_headline(headline):
	db = db_client.webScraper
	headlines = db.headlines
	status = headlines.insert_one({"Site":"apnews","Headline":headline,"Year":year,"Month":month,"Day":day,"Hour":hour})

if True:
	headers = soup.findAll(element_tag, class_=element_class)

count = 0
for header in headers:
	if count >= num_headlines:
		break
	headline = header.a.span.text
	save_headline(headline)
	count = count + 1

