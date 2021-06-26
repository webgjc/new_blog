import json

data = []

source = json.load(open("000001s.json", "r"))
for i in source["data"]["klines"]:
    data.append({
        "x": i.split(",")[0],
        "y": float(i.split(",")[2])
    })

print(data)

json.dump(data, open("000001.json", "w"))
