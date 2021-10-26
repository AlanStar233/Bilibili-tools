import time

import requests
import json
from lxml import html

# 定义uid，api，headers
uid = 1
NickName = ''
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

for uid in range(1, 100000):
    api = 'http://api.bilibili.com/x/space/acc/info?mid={}'.format(uid)
    # 配置response和user_data
    resp = requests.get(api, headers=headers)
    user_data = resp.text
    # 返回Python数据类型
    user_data = json.loads(user_data)
    # 封号判定
    StatusCode = user_data['code']
    if StatusCode == -404:
        print('UID:', uid, '  |  ', '[账号不存在]')
        time.sleep(2)
    else:
        NickName = user_data['data']['name']
        print('UID:', uid, '  |  ', NickName)
        time.sleep(2)


