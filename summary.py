from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
import urllib.parse
import os
import requests
import re
import sys
import pytz

def get_headlines(timeframe):
	#Set up db connection
	client_url = 'mongodb://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + '@' + os.environ['DB_HOST'] + '/apnews?authSource=admin'
	db_client = MongoClient(client_url,27017)
	db = db_client.webScraper

	#Cron runs at midnight, so get dates for yesterday since no data will exist yet today
	central = pytz.timezone('America/Chicago')
	yesterday = datetime.now(central) - timedelta(days = 1)
	year = yesterday.strftime("%Y")
	month = yesterday.strftime("%Y-%m")
	day = yesterday.strftime("%Y-%m-%d")

	sites_json = {}
	lookup_col = ''
	lookup_val = ''

	#No match statment in python 3.6
	if timeframe == 'daily':
		lookup_col = "Day"
		lookup_val = day
	elif timeframe == 'monthly':
		lookup_col = "Month"
		lookup_val = month
	elif timeframe == 'yearly':
		lookup_col = "Year"
		lookup_val = day
	else:
		print("Invalid timeframe ", timeframe)
		return

	#Pull values from mongodb, setup sites_json dict
	headlines = db.headlines.find({lookup_col:lookup_val})
	sites = db.headlines.distinct("Site")
	sites_json["All"] = {}
	for site in sites:
		sites_json[site] = {}

	#Loop through headlines that were found. Tally up word count for each news source
	for headline in headlines:
		site = headline["Site"]
		stripped_words = re.sub('["\'!?.]','',headline["Headline"])
		words = stripped_words.split(' ')
		for word in get_unique_values(words):
			word_count = words.count(word)
			if word in sites_json["All"]:
				sites_json["All"][word] = sites_json["All"][word] + word_count
			else:
				sites_json["All"][word] = word_count
			if word in sites_json[site]:
				sites_json[site][word] = sites_json[site][word] + word_count
			else:
				sites_json[site][word] = word_count

	#Insert word count into appropriate collection
	for site_json in sites_json:
		collection = db[timeframe]
		status = collection.insert_one({"Site":site_json,lookup_col:lookup_val,"Words":sites_json[site_json]})

def get_unique_values(values):
	value_set = set(values)
	return list(value_set)

if len(sys.argv) != 2:
	sys.exit("Invalid arg count. Expected format: python3 summary.py [daily/monthly/yearly]")

get_headlines(sys.argv[1])