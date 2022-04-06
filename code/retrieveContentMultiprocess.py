
import grequests
import requests  # always import after grequests
import sqlite3 as sq3
from bs4 import BeautifulSoup

import time


def retrieveFirstParse(url, count):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    f = grequests.get(url, headers=headers)
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
    usedLinks = []
    for resp in rsm_iterator:
        count += 1
        qs = (retrieveWebContent(resp))
        bh = resp.url
        #usedLinks.append(bh)
        curInner = conn.cursor()
        curInner.execute('SELECT * FROM Crawls')
        curInner.execute('''INSERT INTO Crawls (URL, Parsed) VALUES (?,?);''', (bh, str(qs)))
        #April 5, 2022: I am having the an issue. How do I differential from the links I have already visited
        #I need to stop having a bunch of duplicates in my table.
        conn.commit()
        print(usedLinks)
        #curOuter.execute('DELETE FROM UnprocessedLinks WHERE URLs = ?', bh)
        # your will have an error. You need to pass in a sequence, but you forgot the comma to make your parameters a tuple:
        # (bh,) not bh



