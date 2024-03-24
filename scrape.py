from bs4 import BeautifulSoup
import requests

page_url = "https://apnews.com/us-news"

page_to_scrape = requests.get(page_url)

soup = BeautifulSoup(page_to_scrape.text, "html.parser")

if True:
    headers = soup.findAll("h3", class_="PagePromo-title")
    #headlines = headers.find("span", attrs={"class":"PagePromoContentIcons-text"}).text

count = 0
for header in headers:
    if count > 3:
        break
    print(str(count) + ":" + headline.find("span", class_="PagePromoContentIcons-text").text)
    count = count + 1
    
#print(soup.prettify)
