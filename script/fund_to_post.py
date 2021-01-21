import json

post_file = "../_posts/money_2_基金实际操作.md"
fund_file = "../money/fund.json"

post_header = '''---
article: false
title: 基金实际操作篇
catalog: true
date: 1020-08-23 19:31:43
subtitle: 买入卖出才显自如
header-img:
---

'''

post = post_header

data = json.load(open(fund_file, "r"))

item_date_format = '''
---
### {date}
- {name} ({code})
- {money}
'''

item_format = '''

- {name} ({code})
- {money}
'''

the_date = None
for item in data:
    money = "买入" + item["money"] + "元" if float(item["money"]) > 0 else "卖出" + str(-float(item["money"])) + "元"
    template = None
    if item["date"] != the_date:
        template = item_date_format
        the_date = item["date"]
    else:
        template = item_format
    post += template.format(date=item["date"],
                            name=item["fund_name"],
                            code=item["fund_code"],
                            money=money)

with open(post_file, "w") as f:
    f.write(post)
