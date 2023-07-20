import pandas_datareader as pdr
import datetime
#il manque 
start = datetime.datetime (2002, 1, 1)
end = datetime.datetime (2040, 6, 1)
f = open("indicators.txt", "r")
lines = f.readlines()
for line in lines:
    indicator = line.split(":")
    data = pdr.DataReader(indicator[0], "fred", start, end)
    print(data)