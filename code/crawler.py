import requests
import lxml
from bs4 import BeautifulSoup
import pprint
from functions import straightCrawl, politicsCrawl

urlEntry = ['https://www.bbc.com/news/world-us-canada-61005388']
count = 0
for poli in urlEntry:
    count += 1
    x = politicsCrawl(poli, count)
    #print(x)
    print(count)
