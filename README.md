# Smart Web Scraping
I am currently working on a Sentiment Analysis program, however, as I was writing the code I wanted to have more control over the inputs I put into the model. My Sentiment Analysis project was related to the coverage the U.S politicians received in the news. There are many great APIs, and recently I learned about [Newscatcher](https://newscatcherapi.com/free-news-api). There are others such as: [newsdata.io](https://newsdata.io/), [newsapi.org](https://newsapi.org/), [webz.io](https://webz.io/), [gnews.io](https://gnews.io/), and [infomedia.org](https://infomedia.org/). 

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
  
urlEntry = ['https://www.theguardian.com/us','https://www.nytimes.com/', 'https://www.wsj.com/', 'https://apnews.com/', 'https://www.reuters.com/', 'https://nypost.com/', 'https://thehill.com/', 'https://www.realclearpolitics.com/', 'https://fivethirtyeight.com/', 'https://www.politico.com/']

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

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220403221137.png?raw=true)

With all these links, I needed an efficient way to store the data and use it. I save my final output as a  ```.csv``` file, which I then saved to a database using SQLite. 

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404161215.png?raw=true)

We can use the URLs that are contained within our set, and insert them into our first table called `UnprocessedLinks`. This table will be where any incoming links will be stored as they get ready for processing.

```python
import sqlite3 as sq3  
conn = sq3.connect('UnprocessedLinks')  
curOuter = conn.cursor()  
curOuter.execute('SELECT * FROM UnprocessedLinks')  
for k in webMap:  
    curOuter.execute('''INSERT INTO UnprocessedLinks (URLs) VALUES (?);''', (k,))  
    conn.commit()
```

## Error Handling
For quite sometime, I was facing issues with erroneous links. Some links were simply deadlinks, some were internal links that were not prepended with http, and some were links to social media which I did not want. 
At first I was using a for loop to filter thru these links, however there are so many different ways that a link could be wrong. 
While the internal links and links to social media were managed relatively simply, it was the dead links that were giving me grief. I created a temporary solution while  I was doing my testing of connecting to a website called [Blank.org](http://www.blank.org) which for the time was the easiest method I had of resolving the error. In fact, I think it was an absolutely hilarious way of temporarily solving a major issue. Because Blank.org has literally no content on it, so I basically was able to pretend the link has no content in it, but still was valid in the eyes of the `requests` module.

```python
try:  
    r = requests.get(url, headers=headers, timeout=3)  
    r.raise_for_status()  
except requests.exceptions.RequestException as e:  
 r = requests.get('http://www.blank.org', headers=headers, timeout=3)
```

However, if I were to enter this program into production this would need to change. 
This is where the function `contentUsefulness()` comes into play.
I basically updated the way that `politicsCrawl()` and `straightCrawl()` were allowed to function. Basically before any link is even allowed to be entered into our set `webMap` the content of the website is rated.

```python
try:  
    f = usefulnessQuestioning(start_url)  
    f.raise_for_status()  
except requests.exceptions.RequestException as e:  
 f = contentError(start_url)
```

I have two main pain points that I experienced retrieving links. First of all, many times I end up with large amounts of links from social media like Facebook, Twitter and Instagram which I am not looking for. Second, sometimes website use internal links to link to other pages.

However, in order for `usefulnessQuestioning` to work I actually will need to train a model that can identify if the data we have scraped is worth saving. Unfortunately, at this point in the development process we do not have enough data collected to create a good model. I will need to continue the process by using my temporary fix, and collecting all the data even if it is not the exact data I want.


## Extract Content

```python
import sqlite3 as sq3  
conn = sq3.connect('UnprocessedLinks')  
curOuter = conn.cursor()  
curOuter.execute('SELECT * FROM UnprocessedLinks')  
rows = curOuter.fetchall()  
for row in rows:  
    rowClean = str(row)[2:-3]  
    parseRow = str(retrievePTags(rowClean))  
    curInner = conn.cursor()  
    curInner.execute('SELECT * FROM Crawls') #for rowtoo in  
 curInner.execute('''INSERT INTO Crawls (URL, Parsed) VALUES (?,?);''', (rowClean, parseRow))  
    curOuter.execute('DELETE FROM UnprocessedLinks WHERE URLs = ?', row)  
    conn.commit()
```


```python
def retrievePTags(url):  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'  
 }  
    f = requests.get(url, headers=headers)  
    print(f)  
  
    soup = BeautifulSoup(f.content, 'lxml')  
    body = soup.find_all('p')  
    bodyContent = []  
    for x in body:  
        bodyContent.append(x.get_text().replace('\n', ''))  
    return bodyContent
```

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404144224.png?raw=true)

We now have a large enough dataset that we can use in order for us to train out `contentUsefulness()` model. With the model trained, we can finally step aside and let the crawler script run completely on its own without any supervision.

## Multiprocessing vs. Multithreading
Initially, running this script took an extremely long time, and I knew for a fact that if I continued running the program at its current pace it could potentially take days in order to scrape all the content I need. 
Unfortunately, the global interpreter lock prevents multiple threads of Python code from running. Therefore, while multithreading on Python is not perfect, I can still take speed up the program by using multiprocessing to bypass the GIL.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404194122.png?raw=true)

Looking at the task manager we can clearly see that there is only only thread of the program currently running. I updated the code to use ```grequests``` which is a combination of ```gevent``` and the ```requests``` library.

With multithreading, I also had to bear in mind that SQLite, does not allow multi operations to occur on a database at the same time.

```python
import grequests  
import requests  # always import after grequests  
import sqlite3 as sq3  
from bs4 import BeautifulSoup  
  
import time  
  
  
def retrieveFirstParse(url, count):  
    print(f'Iteration #{count}: {url} pending')  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'  
 }  
    f = grequests.get(url, headers=headers)  
    print(f'Iteration #{count}: finished processing {url}')  
    return f  
  
  
def retrieveWebContent(f):  
    soup = BeautifulSoup(f.content, 'lxml')  
    body = soup.find_all('p')  
    bodyContent = []  
    for x in body:  
        bodyContent.append(x.get_text().replace('\n', ''))  
    return bodyContent  
  
  
def exception_handler(request, exception):  
    print("Request failed")  
  
  
if __name__ == "__main__":  
    batches = 2  
 conn = sq3.connect('UnprocessedLinks', check_same_thread=False)  
    curOuter = conn.cursor()  
    curOuter.execute('SELECT * FROM UnprocessedLinks')  
    urls = curOuter.fetchall()  
  
    count = 0  
 rs = (retrieveFirstParse(str(url)[2:-3], count) for url in urls)  
    rsm_iterator = grequests.imap(rs, size=batches, exception_handler=exception_handler)  
    for resp in rsm_iterator:  
        print(f'Iteration #{count}: Adding {resp.url} to job')  
        count += 1  
 qs = (retrieveWebContent(resp))  
        bh = resp.url  
        curInner = conn.cursor()  
        curInner.execute('SELECT * FROM Crawls')  
        curInner.execute('''INSERT INTO Crawls (URL, Parsed) VALUES (?,?);''', (bh, str(qs)))  
        curOuter.execute('DELETE FROM UnprocessedLinks WHERE URLs = ?', (bh,))  
        # You need to pass in a sequence, but you forgot the comma to make your parameters a tuple:  
 conn.commit()
```


After updating the code, we can see that the program was running asychronously, and I could clearly notice an increase in speed as  I was scraping content.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404194031.png?raw=true)

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404212252.png?raw=true)

Using Viz Tracer, one can visualize the asynchronous nature of the program. While remaining in the same thread, the program is still able to run different processes at the same time.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220404221520.png?raw=true)


## Labeling the Data
After speeding up the scraping considerably, I was finally able to scrape nearly 30,000 different webpages. I noticed that I had acquired thousands of pages of Terms and Conditions content, Login pages, About pages, advertising and web shopping sites (due to affiliate links). If I were to create a sentiment analysis model of all the pages, it would have some severe problems. So by creating this model, I can mitigate the amount of un-useful data I was scraping, by preventing the program from scraping these kind of websites.

The first step was to label the content I has acquired in order to then create a model that I will use to prevent useless data
There are three parameters that I will indicate.

| Parameter | Reason |
| -------- | --- |
| 0 | Not useful at all, do not save content like this | 
| 1 | This content is quite abbreviated. | 
| 2 | This is very useful. |

While there were 30,000 items I had to go through, it was actually a relatively simple process. Especially because the scraper has already saved almost 8,000 blank entries. This would include login pages, dead links etc.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220405033835.png?raw=true)

After I had all the data labelled I could finally create the model.

# Model
The first step was to export the data set as a CSV. I took a selection of 10,000 out of the original 30,000 rows, just to make things simpler. After creating the framework, I could always create a more robust model.

I converted the CSV as a pandas dataframe.
```python
import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt  
from sklearn.model_selection import train_test_split  
from sklearn.feature_extraction.text import CountVectorizer  
from sklearn import svm  
from joblib import dump, load  
import pickle  
  
dataset = pd.read_csv('CrawlsLabelled.csv')
print(dataset[['Parsed', 'Param']]) #Return 10 rows of data  
```

Next I separated out the columns, and split them into training data and test data.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220405193454.png?raw=true)

```python  
  
z = dataset['URL']  
y = dataset["Parsed"]  
x = dataset['Param']  
z_train, z_test, y_train, y_test, x_train, x_test = train_test_split(z, y, x, test_size = 0.2)  
```

I vectorized the webpage contents. 
```
cv = CountVectorizer()  
contentFeatures = cv.fit_transform(y_train)  
print(contentFeatures)  

```

The algorithm I used was Linear Support Vector Classification
```  
model = svm.SVC()  
model.fit(contentFeatures,x_train)  
  
features_test = cv.transform(y_test)  
print("Accuracy: {}".format(model.score(features_test,x_test)))  

```

My initial run of the model show it has a 90% accuracy. I obviously know exactly where the program was faulty, as at one point during the labelling process I did get slightly lazy. I went back into the dataset, and made sure to correct any instances I was being lazy during the labelling process.

In order to use the model for future use without having to retrain the model, I needed to save the vectorizer and the trained model.
```

# Save the vectorizer  
vec_file = 'contentVector.pickle'  
pickle.dump(cv, open(vec_file, 'wb'))  
  
# Save the model  
mod_file = 'conteUsefulness.model'  
pickle.dump(model, open(mod_file, 'wb'))

```



# Testing the Content Filter
In order to test the filter, I copied the contents of a news article that was not contained in our training data.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220406171057.png?raw=true)

```python
from joblib import dump, load  
from sklearn.feature_extraction.text import CountVectorizer  
import pickle  
  
# https://www.bbc.com/news/world-us-canada-61005388  
X_test = ["I pasted the text here"]  
  
# load the vectorizer  
loaded_vectorizer = pickle.load(open('contentVector.pickle', 'rb'))  
  
    # load the model  
loaded_model = pickle.load(open('conteUsefulness.model', 'rb'))  
  
    # make a prediction  
print(loaded_model.predict(loaded_vectorizer.transform(X_test)))
```

I was pleasantly surprised with the output, because it was correct. Indeed, the content of this webpage would be useful.
![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220406170428.png?raw=true)

Conversely, I wanted to test if it could detect whether content was useless.
```python
X_test = ["You are a poop"]  
  
# load the vectorizer  
loaded_vectorizer = pickle.load(open('contentVector.pickle', 'rb'))  
  
    # load the model  
loaded_model = pickle.load(open('conteUsefulness.model', 'rb'))  
  
    # make a prediction  
print(loaded_model.predict(loaded_vectorizer.transform(X_test)))
```

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220406171236.png?raw=true)

So we can now be assured that the model is running the way that it should be.
One issue that I noticed was the model prefers its input in a certain way, I believe this has to do with the fact that the CSV file that the model was trained on had the data saved within square brackets and double quotes ( ```[" data "]``` ). So in order for the model to be useful within our overall program, we will need to make sure the data being passed into the function is in a format it likes. I will certainly take note of this issue the next time I train a model.

## Updating usefulnessQuestion()
Now I wanted to update the function in order for it to reflect the functionality of the filter model we created.
```python
def usefulnessQuestioning(url):  
    headers = {  
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'  
 }  
    conntectionStatus = requests.get(url, headers=headers, timeout=3)  
    soup = BeautifulSoup(conntectionStatus.content, 'lxml')  
    body = soup.find_all('p')  
    bodyContent = []  
    for x in body:  
        runOne = x.get_text().replace('\n', '')  
        bodyContent.append(str(runOne))  
    bodyContent = [i.replace('"', '') for i in bodyContent]  
    bodyContent = [i.replace('\'', '') for i in bodyContent]  
    bodyContent = [''.join(bodyContent)]  
    bodyContent = json.dumps(bodyContent)  
    loaded_vectorizer = pickle.load(open('contentVector.pickle', 'rb'))  
    loaded_model = pickle.load(open('conteUsefulness.model', 'rb'))  
    modelResult = loaded_model.predict(loaded_vectorizer.transform([bodyContent]))  
    if (modelResult[0] > 0):  
        return conntectionStatus  
    else:  
        return contentError(url)
```

Before any link is written into our database, the content of the link is questioned. Using the model we created earlier, we are able to confirm whether or the the content on the link will be useful, before we even record it. Specifically, I did not want the scraper to go thru Terms and Conditions pages, or About pages, which did not contain the content that I was looking for. All those pages had boilerplate text that was not at all useful to me. After running the crawler with this functionality, I can confidently ascertain the content I am now retrieving is very much useful.

![](https://github.com/amadzarak/CrawlerForNLP/blob/main/images/Pasted%20image%2020220406182541.png?raw=true)


# Concluding Thoughts
The program is running nearly perfect. It is fast and scraping useful information, especially with the addition of the content filter. I now had data that was more relevant to the language modeling tasks that I intend on doing in the future.
