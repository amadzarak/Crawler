import requests
import lxml
from bs4 import BeautifulSoup
import pprint
#getting the database content??
import threading
import time
import sqlite3 as sq3
from multiprocessing import Pool

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




if __name__ == '__main__':
    conn = sq3.connect('UnprocessedLinks', check_same_thread=False)
    curOuter = conn.cursor()
    curOuter.execute('SELECT * FROM UnprocessedLinks')
    rows = curOuter.fetchall()                      #the list
    for row in rows:                               #the loop that needs to be multithreaded
        rowClean = str(row)[2:-3]
        parseRow = str(retrievePTags(rowClean))   #the function
        curInner = conn.cursor()
        curInner.execute('SELECT * FROM Crawls') #for rowtoo in
        curInner.execute('''INSERT INTO Crawls (URL, Parsed) VALUES (?,?);''', (rowClean, parseRow))
        curOuter.execute('DELETE FROM UnprocessedLinks WHERE URLs = ?', row)
        conn.commit()