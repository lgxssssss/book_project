import sqlite3
conn = sqlite3.connect('test.db')
  #建立database.db数据库连接
conn.execute('create table if not exists order(oid INTEGER PRIMARY KEY AUTOINCREMENT,uid varchar(100) not null,id varchar(200) not null,`price` double);') #执行单条sql语句
conn.close() 