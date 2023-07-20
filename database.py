import psycopg2
from psycopg2 import sql

class database:

    def __init__(self, dbname, username, password):
        self.dbname = dbname
        self.username = username
        self.password = password

    def insert_links(self):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        f = open("links.txt", "r")
        lines = f.readlines()
        for line in lines:
            tabLink = line.split(";")#tableau
            cur.execute(
            sql.SQL("insert into {}(links, show_more, inter) values (%s, %s, %s)")
                .format(sql.Identifier("t_links_inv")),
            [tabLink[0], tabLink[1], tabLink[2]])

        conn.commit()
        conn.close()

    def fetch_links(self):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute("select * from t_links_inv")
        #print(cur.fetchall())
        links = cur.fetchall()
        conn.close()
        return links

