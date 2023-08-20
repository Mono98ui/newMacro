import pandas_datareader as pdr
from datetime import datetime
from database import database

start = datetime (2002, 1, 1)
end = datetime (2040, 6, 1)
db = database("MacroDB","Test_user","test")
db.update_status("process_investing", 1)
indicators = db.fetch_indicators()

for indicator in indicators:
    list_datas = []
    try:
        datas = pdr.DataReader(indicator[0], "fred", start, end)
        for i in range(datas.shape[0]):

            templistDatas = str(datas.iloc[i]).split(" ")
            templistDatas = list(filter(lambda a: a != "", templistDatas))

            list_datas.append({
            "timestamp": datetime.strptime(templistDatas[2]+" "+templistDatas[3][0:len(templistDatas[3])-1], '%Y-%m-%d %H:%M:%S'),
            "value":float(datas.iloc[i,0]),
            })
        print(list_datas)
        db.insert_value_component(indicator[3].strip().lower(), list_datas)
    except:
        db.update_status("process_investing", -1)
db.update_status("process_investing", 2)