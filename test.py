from database import database
import pandas_datareader as pdr
from datetime import datetime

db = database("MacroDB","Test_user","test")
#db.insert_indicator()
indicators = db.fetch_indicators()
start = datetime (2002, 1, 1)
end = datetime (2040, 6, 1)
for indicator in indicators:
    list_datas = []
    datas = pdr.DataReader(indicator[0], "fred", start, end)
    print(datas)

