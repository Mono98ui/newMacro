import requests
parameters = {
    "start-date": "2021-06-18",
    "end-date": "2023-07-19",
    "time-frame": "Daily",
    "add-missing-rows": "false"
}
headers = {
    "Host":"api.investing.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept":"application/json, text/plain, */*",
    "Accept-Language":"en-US,en;q=0.5",
    "Accept-Encoding":"gzip, deflate, br",
    "Referer":"https://ca.investing.com/",
    "Origin":"https://ca.investing.com/",
    "Connection":"keep-alive",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"no-cors",
    "Sec-Fetch-Site":"same-site",
    "Sec-GPC":"1",
    "TE":"trailers",
    "domain-id":"ca",
    "Pragma":"no-cache",
    "Cache-Control":"no-cache"
}
session = requests.Session()
response = session.get("https://api.investing.com/api/financialdata/historical/8831"
                        ,params=parameters, headers=headers)

print(response.status_code)
print(response.text)
