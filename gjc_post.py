import json
data = json.load(open("gjc_posts.json", "r"))
count = {
    "2017": 1,
    "2018": 1,
    "2019": 2
}

for post in data["RECORDS"]:
    if post["post_status"] != "publish":
        continue
    year = post["post_date"].split("-")[0]
    header = '''
---
title: {}
catalog: true
date: {}
---

'''.format(post["post_title"], post["post_date"])
    content = header + post["post_content"]
    print(content, file=open("source/_posts/{}/article_{}_{}.md".format(year, count[year], post["post_title"].strip()), "w"))
    count[year] += 1