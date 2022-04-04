I am currently working on a Sentiment Analysis program, however, as I was writing the code I wanted to have more control over the inputs I put into the model. My Sentiment Analysis project was related to the coverage the U.S politicians received in the news. There are many great APIs, and recently I learned about [https://newscatcherapi.com/free-news-api|newscatcher]. There are others such as: [newsdata.io], [newsapi.org], [webz.io], [gnews.io], and [infomedia.org]. 

I decided that in order to have the most control, I would need to collect the data myself. Also, I felt that because many of the APIs limit the amount of calls you can make in a free plan, if did choose to use one of the APIs I would need to pay for a more premium plan. Unfortunately, I felt that this was out of my budget, and I needed a workaround. Creating the WebCrawler was a great undertaking, and I truly do have an appreciation for those of us that are willing to offer their APIs as a service. 

For a more complex project, I might be forced to either update my current code or bite the bullet and pay for an API, but for my current use case, the Crawler I have written works perfectly fine.

## The Initial Approach
The amount of information contained on the internet is enormous, and I specifically was looking for news and analysis written about politicians. The underlying hypothesis with this project, was that by compiling a list of links, and then compiling a list of links contained within the first list of links, the data would increase exponentially.

I began by curating a list of my favorite news sources.
1. The Guardian
2. The New York Times
3. Wall Street Journal
4. AP News
5. Reuters
6. The New York Post
7. The Hill
8. Real Clear Politics
9. FiveThirtyEight
10. Politico

```python
from functions import straightCrawl, politicsCrawl  
  
urlEntry = ['https://www.theguardian.com/us','https://www.nytimes.com/', 'https://www.wsj.com/, 'https://apnews.com/', 'https://www.reuters.com/', 'https://nypost.com/', 'https://thehill.com/', 'https://www.realclearpolitics.com/', 'https://fivethirtyeight.com/', 'https://www.politico.com/']

count = 0  
for poli in urlEntry:  
    count += 1  
 x = politicsCrawl(poli, count)  
    print(x)  
    print(count)
```


The first manual scraping program consisted of two functions: ```politicsCrawl()``` and ```straightCrawl()```.

```python
def politicsCrawl(start_url, count):  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'  
 }  
    f = requests.get(start_url, headers=headers)  
    soup = BeautifulSoup(f.content, 'lxml')  
    linksOnStart = soup.find_all('a')  
    newLinks = []  
    for x in linksOnStart:  
        words = x.get_text()  
        x = x.get('href')  
        newLinks.append(x)  
  
    linkFilter = []
 for x in newLinks:  
        if x != None and x.startswith('http'):  
            linkFilter.append(x)
```

The function ```politicsCrawl()```  iterated through my initial list of ten manually entered news websites, and compiled all the linked contained on the homepage.
Within the function it filtered through any ```<a href=''>``` tags that are not proper http or https links. Such as links to share an item on Twitter, or Facebook. All the valid URL links on the homepage of these website were entered into a set. 

It may be prudent to mention that as I was writing the code, I actually had the functions write to a text document the first time. It simplified the development process, as I was able to monitor all the outputs.

After running the ```politicsCrawl()``` the first time, I had compiled thousands of links. In fact, I saw links from some sources that I had not even entered into my first manual list such as The Chicago Tribune, MarketWatch, WashingtonExaminer, Vogue, Newsweek, The Federalist, Washington Examiner and more.

```python
webMap = set()  
for i in linkFilter:  
    webMap.update(straightCrawl(i))  
    print(len(webMap))  
    print(webMap)
```

I had all the links that both crawling functions acquired entered into a set for a specific reason. That was because for me, the order of the lists did not really matter. What mattered was that I limited the amount of duplicate lists. If I grabbed a lot of duplicate information, it might affect the language model. 

With the first set of links acquired, it was now time to iterate through all the link and call the function ```straightCrawl()```. 

```python
def straightCrawl(url):  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'  
 }  
    f = requests.get(url, headers=headers)  
    print(f)  
    soup = BeautifulSoup(f.content, 'lxml')  
    linksOnStart = soup.find_all('a')  
    newLinks = []  
    for x in linksOnStart:  
        words = x.get_text()  
        x = x.get('href')  
        newLinks.append(x)  
  
    linkFilter = []  # filter down new links  
 for x in newLinks:  
        if x != None and x.startswith('http'):              # and term in x  
 linkFilter.append(x)  
    return linkFilter
```

I had run the program just one time, and acquired a huge list of over 26,700 unique URLs.
!()[https://github.com/amadzarak/CrawlerForNLP/blob/main/Pasted%20image%2020220403221137.png?raw=true]

With all these links, I needed an efficient way to store the data and use it. I save my final output as a  ```.csv``` file, which I then saved to a database using SQLite. 

!()[https://github.com/amadzarak/CrawlerForNLP/blob/main/Pasted%20image%2020220403204309.png?raw=true]

