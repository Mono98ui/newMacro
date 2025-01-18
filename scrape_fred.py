import pandas_datareader as pdr
from datetime import datetime
from database import database
import os
import math
from private import Private

def check_forNoneNanData(datas, i):
    if i == 0 and math.isnan(float(datas.iloc[i,0])):
        return float(0)
    elif math.isnan(float(datas.iloc[i,0])):
        return check_forNoneNanData(datas, i-1)
    return float(datas.iloc[i,0])

pr = Private()


start = datetime (2002, 1, 1)
end = datetime (2040, 6, 1)
db = database(os.getenv('DB_NAME'),os.getenv('DB_USER'),os.getenv('DB_PASSWORD'))
db.update_status("process_fred", 1)
indicators = db.fetch_indicators()

#Scrape the data from fred and stor it in the database
for indicator in indicators:
    list_datas = []
    try:
        datas = pdr.DataReader(indicator[0], "fred", start, end)
        for i in range(datas.shape[0]):

            templistDatas = str(datas.iloc[i]).split(" ")
            templistDatas = list(filter(lambda a: a != "", templistDatas))

            list_datas.append({
            "timestamp": datetime.strptime(templistDatas[2]+" "+templistDatas[3][0:len(templistDatas[3])-1], '%Y-%m-%d %H:%M:%S'),
            "value":float(check_forNoneNanData(datas, i)),
            })
        db.insert_value_component(indicator[3].strip().lower(), list_datas)
    except:
        db.update_status("process_fred", -1)
db.update_status("process_fred", 2)

pr.clean()