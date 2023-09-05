from database import database
import pandas_datareader as pdr
from datetime import datetime

#db = database("MacroDB","Test_user","test")

#db.insert_links()
#db.insert_indicator()
start = datetime (2002, 1, 1)
end = datetime (2040, 6, 1)

datas = pdr.DataReader("TCU", "fred", start, end)