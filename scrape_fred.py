import pandas_datareader as pdr
from datetime import datetime
from database import database
import os
from private import Private
from decimal import Decimal
import numpy as np
from round_decimal import round_decimal

def check_forNoneNanData(datas, i):
    val = datas.iloc[i, 0]
    if isinstance(val, np.int64):
        val = round_decimal(int(val))  # Apply round_decimal
    else:
        val = round_decimal(val)  # Apply round_decimal

    # Handle NaN case and rounding to two decimal places
    if i == 0 and val.is_nan():
        return round_decimal(0)
    elif val.is_nan():
        return check_forNoneNanData(datas, i-1)

    # Return the rounded value
    return val

pr = Private()

start = datetime(2002, 1, 1)
end = datetime(2040, 6, 1)
db = database(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))
db.update_status("process_fred", 1)
indicators = db.fetch_indicators()

# Scrape the data from FRED and store it in the database
for indicator in indicators:
    list_datas = []
    try:
        datas = pdr.DataReader(indicator[0], "fred", start, end)
        for i in range(datas.shape[0]):
            templistDatas = str(datas.iloc[i]).split(" ")
            templistDatas = list(filter(lambda a: a != "", templistDatas))

            list_datas.append({
                "timestamp": datetime.strptime(templistDatas[2] + " " + templistDatas[3][0:len(templistDatas[3])-1], '%Y-%m-%d %H:%M:%S'),
                "value": check_forNoneNanData(datas, i),  # Rounded value
            })

        db.insert_value_component(indicator[3].strip().lower(), list_datas)
    except Exception as e:
        print(f"Error: {e}")
        db.update_status("process_fred", -1)

# Update status after processing
db.update_status("process_fred", 2)

pr.clean()
