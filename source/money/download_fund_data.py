import re
import time
import json
import requests


code_list = set()
fund_data = json.load(open("./fund.json"))
for i in fund_data:
    code_list.add(i["fund_code"])
start_time = fund_data[-1]["date"]
start_timestamp = time.mktime(time.strptime(start_time, "%Y-%m-%d")) * 1000
req = requests.Session()

for code in code_list:
    print(code)
    try:
        time.sleep(0.5)
        resp = req.get("http://fund.eastmoney.com/pingzhongdata/{}.js".format(code))
        source_data = re.search("Data_ACWorthTrend = (.*?);", resp.text).group(1)
        data = [i for i in json.loads(source_data) if i[0] >= start_timestamp]
        res = []
        for i in data:
            res.append({
                "x": time.strftime("%Y-%m-%d", time.localtime(i[0]/1000)),
                "y": i[1]
            })
        json.dump(res, open("./funddata/{}.json".format(code), "w"))
    except Exception as e:
        print(e)

