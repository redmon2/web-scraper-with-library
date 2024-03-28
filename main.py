from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.parse
import os
import requests

client_url = 'mongodb://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/apnews?authSource=admin'
db_client = MongoClient(client_url,27017)

page_url = "https://apnews.com/us-news"
element_tag = "h3"
element_class = "PagePromo-title"
num_headlines = 3

page_to_scrape = requests.get(page_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

def save_headline(headline):
	print(headline)
	data = db_client.headlines
	storage = data.storage
	status = storage.insert_one({"Site":"apnews","Headline":headline})
	print(status)

if True:
	headers = soup.findAll(element_tag, class_=element_class)

count = 0
for header in headers:
	if count >= num_headlines:
		break
	headline = header.a.span.text
	save_headline(headline)
	count = count + 1

