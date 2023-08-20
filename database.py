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
            sql.SQL("insert into {}(links, show_more, inter, t_name) values (%s, %s, %s, %s)")
                .format(sql.Identifier("t_links_inv")),
            [tabLink[0].strip(), tabLink[1].strip(), tabLink[2], tabLink[3].strip()])

        conn.commit()
        conn.close()

    def insert_indicator(self):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        f = open("indicators.txt", "r")
        lines = f.readlines()
        for line in lines:
            tabLink = line.split(":")#tableau
            cur.execute(
            sql.SQL("insert into {}(id, descr, inter, t_name) values (%s, %s, %s, %s)")
                .format(sql.Identifier("t_indicators_fred")),
            [tabLink[0].strip(), tabLink[1].strip(), tabLink[2].strip(), tabLink[3].strip()])

        conn.commit()
        conn.close()

    def insert_value_component(self, t_name, list_data):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        for data in list_data:
            #Ajouter  "ON CONFLICT (date) DO NOTHING" a la requete pour debugger
            cur.execute(
            sql.SQL("insert into {}(date, value) values (%s, %s) ON CONFLICT (date) DO NOTHING")
                .format(sql.Identifier(t_name)),
            [data["timestamp"], data["value"]])

        conn.commit()
        conn.close()

    def insert_value_component_gr(self, t_name, list_data):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        for data in list_data:
            #Ajouter  "ON CONFLICT (date) DO NOTHING" a la requete pour debugger
            cur.execute(
            sql.SQL("insert into {}(date, value, intervalMonth) values (%s, %s, %s) ON CONFLICT (date, intervalMonth) DO "+
                    "update set value = %s where {}.date = %s and {}.intervalMonth = %s")
                .format(sql.Identifier(t_name), sql.Identifier(t_name), sql.Identifier(t_name)),
            [data["timestamp"], data["value"], data["intervalMonth"], data["value"], data["timestamp"], data["intervalMonth"]])

        conn.commit()
        conn.close()

    def fetch_links(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_links_inv", columnName, operator, columnVal)
    
    def fetch_indicators(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_indicators_fred", columnName, operator, columnVal)
    
    def fetch_status(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_status_process", columnName, operator, columnVal)
    
    #faire une sql builder pour pouvoir mettre beaucoup de condition
    def fetch_table(self, t_name, columnName, operator, columnVal):
        where = sql.SQL("where {}{}{}").format(sql.SQL(columnName), sql.SQL(operator), sql.Literal(columnVal)) if columnName and columnVal else sql.SQL("")
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute(
            sql.SQL("select * from {} {}")
                .format(sql.Identifier(t_name), where))
        datas = cur.fetchall()
        conn.close()
        return datas
    
    def update_status(self, id, status):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute(
        sql.SQL("update t_status_process set status=%s where process_name=%s"),
        [status, id])

        conn.commit()
        conn.close()