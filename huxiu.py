import requests
from bs4 import BeautifulSoup
import pymysql
import uuid
import time
import sys

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password=sys.argv[1],
    db='hub',
    charset='utf8mb4'
)

cursor = connection.cursor()

header = {
  'User-Agent': 'PostmanRuntime/7.13.0',
  'Accept': '*/*',
  'Cache-Control': 'no-chche',
  'Postman-Token': 'f3c6b814-1da7-4572-8bfd-7b1670466d6d',
  'Host': 'www.huxiu.com',
  'cookie': '__secdyid=646d94518ceb227ba0f179f03f92553665e7722c2d63cca7021570874304; SERVERID=4ae5405a223af78c2466769f0b2cf838|1570874371|1570874304',
  'accept-encoding': 'gzip, deflate',
  'Connection': 'keep-alive'
}

response = requests.get('https://www.huxiu.com/article', headers=header)

if (response.status_code == 200):
    print('load success!')
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('div', class_='article-item article-item--big')

    for article in articles:
        url = 'www.huxiu.com' + article.a.get('href')
        title = article.a.div.img.get('alt')
        scraped_at = time.strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO `huxiu` (`id`, `title`, `url`, `scraped_at`) VALUES ('%s', '%s', '%s', '%s')" % (uuid.uuid1(), title, url, scraped_at)

        try:
            cursor.execute(sql)
            connection.commit()
            print('import data success!')
        except Exception:
            print(Exception)
            connection.rollback()

connection.close()