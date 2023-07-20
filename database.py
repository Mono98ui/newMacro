import psycopg2
from psycopg2 import sql

class database:

    def __init__(self, dbname, username, password):
        self.dbname = dbname
        self.username = username
        self.password = password

    def insert_links():
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

    def fetch_links():
        conn = psycopg2.connect("dbname=MacroDB user=Test_user password=test")
        cur = conn.cursor()
        cur.execute("select * from testtable")
        #print(cur.fetchone())
        conn.close()

