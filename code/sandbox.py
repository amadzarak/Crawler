from bs4 import BeautifulSoup
import requests
import json
import pickle

def applyContentFilterModel(url):
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
        return '<Response [200]>'
    else:
        skip = '<Response [404]>'
        return skip

    #return conntectionStatus, modelResult[0]

print(applyContentFilterModel('https://www.bbc.com/news/world-us-canada-61005388'))