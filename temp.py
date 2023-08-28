from database import database

db = database("MacroDB","Test_user","test")

db.insert_links()
db.insert_indicator()