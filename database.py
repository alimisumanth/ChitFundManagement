import sqlite3

con=sqlite3.connect("chitdb.sqlite")
cur=con.cursor()
con.row_factory = sqlite3.Row
cur.execute("DROP Table IF EXISTS GROUP1")
cur.execute("DROP Table IF EXISTS GROUP2")
cur.execute("CREATE TABLE GROUP1(id integer PRIMARY KEY AUTOINCREMENT,name text,Totalmonths integer DEFAULT 20,RemainingMonths integer DEFAULT 20,PaidAmount integer,BalanceAmount integer,groups text)")
cur.execute("CREATE TABLE GROUP2(id integer PRIMARY KEY AUTOINCREMENT,name text,Totalmonths integer DEFAULT 20,RemainingMonths integer DEFAULT 20,PaidAmount integer,BalanceAmount integer,groups text)")
con.commit()

