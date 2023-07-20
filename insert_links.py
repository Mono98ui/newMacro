import psycopg2
from psycopg2 import sql

conn = psycopg2.connect("dbname=MacroDB user=Test_user password=test")
cur = conn.cursor()
f = open("links.txt", "r")
lines = f.readlines()
for line in lines:
    tabLink = line.split(";")#tableau
    cur.execute(
    sql.SQL("insert into {}(links, show_more, inter) values (%s, %s, %s)")
        .format(sql.Identifier("t_links_inv")),
    [tabLink[0], tabLink[1], tabLink[2]])

#cur.execute("select * from testtable")
#print(cur.fetchone())
conn.commit()
conn.close()