from bs4 import BeautifulSoup
import requests

page_url = "https://apnews.com/us-news"
element_tag = "h3"
element_class = "PagePromo-title"
num_headlines = 3

page_to_scrape = requests.get(page_url)
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

def save_headline(headline):
    print(headline)

if True:
    headers = soup.findAll(element_tag, class_=element_class)

count = 0
for header in headers:
    if count >= num_headlines:
        break
    headline = header.a.span.text
    save_headline(headline)
    count = count + 1

