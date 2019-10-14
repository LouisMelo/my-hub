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
  "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"
}

response = requests.get('https://www.zhangzishi.cc/', headers=header)

print(response.status_code)

soup = BeautifulSoup(response.content, "html5lib")

articles = soup.find_all('article', class_='excerpt')

for article in articles:
  title = article.h2.a.string
  url = article.h2.a.get('href')
  scraped_at = time.strftime('%Y-%m-%d %H:%M:%S')
  published_at = article.footer.time.string

  sql = "INSERT INTO `zhangzishi` (`id`, `title`, `url`, `scraped_at`, `published_at`) VALUES ('%s', '%s', '%s', '%s', '%s')" % (uuid.uuid1(), title, url, scraped_at, published_at)

  try:
    cursor.execute(sql)
    connection.commit()
  except Exception:
    print (Exception)  
    connection.rollback()

connection.close()  
