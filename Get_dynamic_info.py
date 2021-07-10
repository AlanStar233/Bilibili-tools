import requests
import json
import os
from lxml import html

# 预定义dynamic_id，api，headers
dynamic_id = input('请输入动态ID:')
api = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(dynamic_id)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# 配置response和data
resp = requests.get(api, headers=headers)
dynamic_data = resp.text
selector = html.fromstring(dynamic_data)

# 返回Python数据类型
dynamic_data = json.loads(dynamic_data)

# 定义查询变量
# 动态数据
rid = dynamic_data['data']['card']['desc']['rid']
view = dynamic_data['data']['card']['desc']['view']
like = dynamic_data['data']['card']['desc']['like']
comment = dynamic_data['data']['card']['desc']['comment']
repost = dynamic_data['data']['card']['desc']['repost']
# 发送者数据
UID = dynamic_data['data']['card']['desc']['uid']
Uname = dynamic_data['data']['card']['desc']['user_profile']['info']['uname']
# 发送者认证数据
official_verify_type = dynamic_data['data']['card']['desc']['user_profile']['card']['official_verify']['type']
official_verify_desc = dynamic_data['data']['card']['desc']['user_profile']['card']['official_verify']['desc']

# 打印
print('------------------------------')
print('动态数据')
print('rid:', rid)
print('浏览量:', view)
print('赞:', like)
print('评论:', comment)
print('转发:', repost)
print('------------------------------')
print('发送者数据')
print('UID:', UID)
print('用户名:', Uname)
print('------------------------------')
print('动态发送者认证数据')
print('认证代号:', official_verify_type)
print('认证描述:', official_verify_desc)
print('------------------------------')

# 调用系统函数pause
os.system('pause')