import re
import json
import time
import requests
import pandas as pd


req = requests.Session()

fund_name_code_map = {
    "汇添富创新医药主题混合": "0006113",
    "鹏华中证传媒指数分级": "160629",
    "华安中证全指证券公司": "160419",
    "天弘创业板ETF联接C": "001593",
    "信诚中证800有色指数": "165520",
    "方正富邦中证保险主题": "167301",
    "博时中证银行指数分级": "160517",
    "国泰国证食品饮料行业": "160222",
    "鹏华中证信息技术指数": "160626",
    "鹏华丰融定期开放债券": "000345",
    "天弘中证电子ETF联接A": "001617",
    "诺安成长混合": "320007",
    "易方达消费行业股票": "110022",
    "汇添富上证综合指数": "470007",
    "招商中证白酒指数分级": "161725",
    "永赢智能领先混合C": "006269",
    "天弘沪深300ETF联接A": "000961",
    "天弘上证50指数A": "001548",
    "前海开源金银珠宝混合A": "001302",
    "嘉实农业产业股票": "003634",
    "嘉实物流产业股票A": "003298",
    "银河创新成长混合": "519674",
    "富国周期优势混合": "005760",
    "景顺长城新兴成长混合": "260108",
    "鹏华丰禄债券": "003547",
    "富国稳健增强债券C": "000109",
    "浙商聚潮新思维混合": "166801",
    "南方宝元债券C": "006585",
    "南方创业板ETF联接C": "004343",
    "天弘中证电子指数A": "001617",
    "兴业多策略灵活配置混合": "000963",
    "工银瑞信全球股票(QDII)": "486001",
    "富国上证综指ETF联接": "100053",
    "招商国证生物医药指数": "161726",
    "汇添富中证环境治理指数(LOF)A": "501030",
    "前海开源金银珠宝主题精选灵活配置混合A": "001302",
    "天弘沪深300指数A": "000961",
    "富国国家安全主题混合": "001268",
    "招商产业债券A": "217022",
    "万家日日薪货币A": "519511",
    "英大现金宝货币": "000912",
    "景顺长城沪深300增强": "000311",
    "天弘创业板指数A": "001592",
    "广发稳健增长混合": "270002",
    "南方中债10年期国债指数C": "160124",
    "兴全轻资产投资混合(LOF)": "163412",
    "招商MSCI中国A股国际通指数A": "005761",
    "天弘创业板指数C": "001593",
}

fundcode = {}
source_data = req.get("http://fund.eastmoney.com/js/fundcode_search.js")
data = json.loads(re.search("r = (.*?);", source_data.text).group(1))
for i in data:
    fundcode[i[2]] = i[0]
# print(fundcode)

date_list = []
tmp = req.get("http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112407444039735425554_1612348798572&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg=19900101&end=20220101&_=1612348798573")
# print(re.search("798572(.*?)", tmp.text).group(1)[1:-1][10:])
zhishu_data = json.loads(re.search("798572(.*?);", tmp.text).group(1)[1:-1])
# zhishu_data = req.get("http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112407444039735425554_1612348798572&secid=1.000001&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg=19900101&end=20220101&_=1612348798573").json()
for i in zhishu_data["data"]["klines"]:
    date_list.append(i.split(",")[0])

result = []
fund_data = pd.read_csv("./alipay_record_20210203_1253_1.csv")
columns = fund_data.columns
unfund_names = set()
for index, row in fund_data.iterrows():
    # print(index, row)
    # print(row[columns[9]])
    # break
    if row[columns[0]].startswith("20"):
        fund_tmp = row[columns[8]].split("-")
        if len(fund_tmp) == 3:
            money_tmp = 0
            if "卖出" in fund_tmp[2]:
                money_tmp = str(-float(row[columns[9]]))
            if "买入" in fund_tmp[2]:
                money_tmp = row[columns[9]]
            if "分红" in fund_tmp[2]:
                money_tmp = str(-float(row[columns[9]]))
            if money_tmp == 0:
                continue
            fund_tmp[1] = fund_tmp[1].strip()
            tmp_code = None
            if fund_name_code_map.get(fund_tmp[1]) is not None:
                tmp_code = fund_name_code_map.get(fund_tmp[1])
            if fundcode.get(fund_tmp[1]) is not None:
                tmp_code = fundcode.get(fund_tmp[1])
                if fund_name_code_map.get(fund_tmp[1]) is None:
                    fund_name_code_map[fund_tmp[1]] = fundcode.get(fund_tmp[1]),
                    print("\"{}\": \"{}\",".format(fund_tmp[1], fundcode.get(fund_tmp[1])))
            if tmp_code is None:
                unfund_names.add(fund_tmp[1])
            else:
                date = time.mktime(time.strptime(row[columns[2]].split(" ")[0], "%Y/%m/%d"))
                date = time.strftime("%Y-%m-%d", time.localtime(date))
                result.append({
                    "date": date,
                    "datetime": row[columns[2]],
                    "fund_name": fund_tmp[1],
                    "fund_code": tmp_code,
                    "money": money_tmp
                })
# print(result)
# print("未确认基金代码:", unfund_names)
# print(fund_name_code_map)
# print(result)

# 矫正时间数据
use_date_list = []
for i in date_list:
    if i > result[-1]["date"]:
        use_date_list.append(i)
for item in result:
    if item["date"] not in use_date_list:
        for j in use_date_list:
            if item["date"] < j:
                item["date"] = j
                break

json.dump(result, open("./fund.json", "w"))
print("finish")



