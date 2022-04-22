import json
import time
import config

all = None
with open("downloads/list.json",encoding="utf-8") as f:
    all = json.load(f)

print(all['pageModel']['itemList'][0]['createDate'])
print(all['pageModel']['itemList'][0]['id'])

print(config.today_time)