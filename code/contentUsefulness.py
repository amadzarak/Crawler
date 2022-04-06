# here i want to write a script that actually determines if the content I just scraped is even useful.
# if the content is not considered useful, or I cannot extract information from it then the url will be added to a table
#called URL blacklists
# one method may be identifying topics and seeing if the topics are in other scraped sits???
from bs4 import BeautifulSoup
import requests
import json
import pickle

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

def contentError(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    y = requests.get('http://www.blank.org', headers=headers, timeout=3)
    return y