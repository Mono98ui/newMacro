import psycopg2
from psycopg2 import sql
#
#This class allowed the user to connect to database
#
class database:

    #
    #Param:
    #dbname: databasename
    #username: Username of the user of the database
    #password: The password of the user
    #This is the constructor initilizing the variable that allow us to connect to the database
    #
    def __init__(self, dbname, username, password):
        self.dbname = dbname
        self.username = username
        self.password = password
    #
    #Param: None
    #This method insert informations related mainly to indicator found in investing.com 
    #
    def insert_links(self):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        f = open("links.txt", "r")
        lines = f.readlines()
        for line in lines:
            tabLink = line.split(";")#tableau
            print(tabLink[5])
            cur.execute(
            sql.SQL("insert into {}(links, show_more, inter, t_name, descr, is_oscillator) values (%s, %s, %s, %s, %s, %s)")
                .format(sql.Identifier("t_links_inv")),
            [tabLink[0].strip(), tabLink[1].strip(), tabLink[2], tabLink[3].strip(), tabLink[4].strip(), tabLink[5]])

        conn.commit()
        conn.close()
    #
    #Param: None
    #This method insert informations related mainly to indicator found in Fred
    #
    def insert_indicator(self):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        f = open("indicators.txt", "r")
        lines = f.readlines()
        for line in lines:
            tabLink = line.split(":")#tableau
            cur.execute(
            sql.SQL("insert into {}(id, descr, inter, t_name, is_oscillator) values (%s, %s, %s, %s, %s)")
                .format(sql.Identifier("t_indicators_fred")),
            [tabLink[0].strip(), tabLink[1].strip(), tabLink[2].strip(), tabLink[3].strip(), tabLink[4]])

        conn.commit()
        conn.close()
    
    #
    #Param:
    #t_name: table name
    #list_data: data fecth from the source: either fred or indicator
    #This method insert data from indicators
    #
    def insert_value_component(self, t_name, list_data):
        
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        
        for data in list_data:
            #Ajouter  "ON CONFLICT (date) DO NOTHING" a la requete pour debugger
            # ON CONFLICT (date) DO  update set value = %s where {}.date = %s
            cur.execute(
            sql.SQL("insert into {}(date, value) values (%s, %s) ON CONFLICT (date) DO NOTHING")
                .format(sql.Identifier(t_name), sql.Identifier(t_name)),
            [data["timestamp"], data["value"]])

            #cur.execute(
            #sql.SQL("insert into {}(date, value) values (%s, %s) ON CONFLICT (date) DO NOTHING")
            #    .format(sql.Identifier(t_name), sql.Identifier(t_name)),
            #[data["timestamp"], data["value"]])

        conn.commit()
        conn.close()
    #
    #Param:
    #t_name: table name
    #list_data: the list of growth rate
    #This method insert the growrate from indicators
    #
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
    #
    #Param:
    #columnName: column name
    #operator: the operator for where statement
    #columnVal: the value of the column
    #This method show the content of the table t_links_inv
    #
    def fetch_links(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_links_inv", columnName, operator, columnVal)
    #
    #Param:
    #columnName: column name
    #operator: the operator for where statement
    #columnVal: the value of the column
    #This method show the content of the table t_indicators_fred
    #
    def fetch_indicators(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_indicators_fred", columnName, operator, columnVal)
    #
    #Param:
    #columnName: column name
    #operator: the operator for where statement
    #columnVal: the value of the column
    #This method show the content of the table t_status_process
    #
    def fetch_status(self, columnName="", operator="", columnVal=""):
        return self.fetch_table("t_status_process", columnName, operator, columnVal)
    #
    #Param:
    #t_name: Table name
    #after: part of the sql statement after from t_name
    #This method show the content of the table containing the growrate
    #
    def fetch_table_show_gr(self, t_name, after=""):
        afterSQL = sql.SQL(after)
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute(
            sql.SQL("select CASE WHEN tb.is_oscillator THEN Null ELSE round(t1.value::numeric, 2) END, round(t2.value::numeric, 2), t1.value > t2.value,"
                    +" CASE WHEN t1.value > t2.value THEN 'Hawkish' ELSE 'Dovish' END"
                    +",t1.date from {} {}")
                .format(sql.Identifier(t_name), afterSQL))
        datas = cur.fetchall()
        conn.close()
        return datas
    #
    #Param:
    #t_name: Table name
    #after: part of the sql statement after from t_name
    #This method show the content of the table specify.
    #This a template for other method
    #
    #Comment: faire une sql builder pour pouvoir mettre beaucoup de condition
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

    def fetch_table_Main(self, t_name, columnName, operator, columnVal):
        where = sql.SQL("where {}{}{}").format(sql.SQL(columnName), sql.SQL(operator), sql.Literal(columnVal)) if columnName and columnVal else sql.SQL("")
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute(
            sql.SQL("select * from {} {} order by {}.date")
                .format(sql.Identifier(t_name), where, sql.Identifier(t_name)))
        datas = cur.fetchall()
        conn.close()
        return datas
    #
    #Param:
    #id: The id of the process
    #status: Status of the process
    #This method update the status of the process
    #
    def update_status(self, id, status):
        conn = psycopg2.connect("dbname={} user={} password={}".format(self.dbname,self.username, self.password ))
        cur = conn.cursor()
        cur.execute(
        sql.SQL("update t_status_process set status=%s where process_name=%s"),
        [status, id])

        conn.commit()
        conn.close()