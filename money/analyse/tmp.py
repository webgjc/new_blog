import re
import json 
import requests

date_list = []
tmp = requests.get("http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112407444039735425554_1612348798572&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg=19900101&end=20220101&_=1612348798573")
zhishu_data = json.loads(re.search("798572(.*?);", tmp.text).group(1)[1:-1])
json.dump(zhishu_data, open("000001.json", "w"))