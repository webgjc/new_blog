import json

data = []
data_all = []

source = json.load(open("000001s.json", "r"))
for i in source["data"]["klines"]:
    data_all.append({
        "x": i.split(",")[0],
        "y": float(i.split(",")[2])
    })
    if i.split(",")[0] > '2010-01-01':
        data.append({
            "x": i.split(",")[0],
            "y": float(i.split(",")[2])
        })

json.dump(data_all, open("000001all.json", "w"))
json.dump(data, open("000001.json", "w"))

print(1)