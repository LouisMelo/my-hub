import pymysql

db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='louisnow117',
    db='hub',
    charset='utf8mb4'
)

cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO zhangzishi(id, \
       title, url, scraped_at, published_at) \
       VALUES ('%s', '%s',  '%s',  '%s',  '%s')" % \
       ('Mac', 'Mohan', '12344', '2019-10-10', '2019-10-10')

# 执行sql语句
cursor.execute(sql)
# 执行sql语句
db.commit()
 
# 关闭数据库连接
db.close()