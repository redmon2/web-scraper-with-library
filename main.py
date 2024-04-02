from pymongo import MongoClient
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
import os
import requests
import pytz
import sys

client_url = 'mongodb://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/apnews?authSource=admin'
db_client = MongoClient(client_url,27017)

#Scraper variables
if len(sys.argv) != 2:
	sys.exit("Invalid arg count. Expected format: python3 main.py [Site]")

site = sys.argv[1]
num_headlines = 3

valid_sites = ["ap", "cnn", "fox"]
if site not in valid_sites:
	sys.exit("Invalid site: " + site)

if site == "ap":
	page_url = "https://apnews.com/us-news"
	element_tag = "h3"
	element_class = "PagePromo-title"
elif site == "cnn":
	page_url = "https://www.cnn.com/us"
	element_tag = "span"
	element_class = "container__headline-text"
elif site == "fox":
	page_url = "https://www.foxnews.com/us"
	element_tag = "h2"
	element_class = "title"

page_to_scrape = requests.get(page_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

#Time variables
central = pytz.timezone('America/Chicago')
now = datetime.now(central)
year = now.strftime("%Y")
month = now.strftime("%Y-%m")
day = now.strftime("%Y-%m-%d")
hour = now.strftime("%H")

def save_headline(headline):
	db = db_client.webScraper
	headlines = db.headlines
	status = headlines.insert_one({"Site":site,"Headline":headline,"Year":year,"Month":month,"Day":day,"Hour":hour})

headers = soup.findAll(element_tag, class_=element_class)

count = 0
for header in headers:
	if count >= num_headlines:
		break
	if site == "ap":
		headline = header.a.span.text
	elif site == "cnn":
		headline = header.text
	elif site == "fox":
		headline = header.a.text
	save_headline(headline)
	count = count + 1

