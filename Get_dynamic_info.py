import requests
import json
import os
from lxml import html
from urllib.parse import urlparse

# 通过输入的动态URL提取path，即未处理的dynamic_id
url = input('请输入动态URL:')
parsed_result = urlparse(url)
url_path = parsed_result.path

# 获取dynamic_id (去除'/')
dynamic_id = url_path.replace('/', '')

# 预定义dynamic_id，api，headers
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

# 定义uid，api，headers
userinfo_api = 'http://api.bilibili.com/x/space/acc/info?mid={}'.format(UID)

# 配置response和data
userinfo_resp = requests.get(userinfo_api, headers=headers)
user_data = userinfo_resp.text
user_selector = html.fromstring(user_data)

# user_data转换为Python格式
user_data = json.loads(user_data)

# 认证码及认证身份类型初始化
official_role_num = user_data['data']['official']['role']
official_role = ''

# 认证身份判定
if official_role_num == 0:
    official_role = '未认证'
elif 1 <= official_role_num <= 2:
    official_role = '个人认证'
elif 3 <= official_role_num <= 6:
    official_role = '企业认证'
elif official_role_num == 7:
    official_role = '个人认证'

# 认证类型转换为具体描述
if official_verify_type == -1:
    official_verify_type = '未认证'
elif 1 >= official_verify_type >= 0:
    official_verify_type = '已认证'
# 认证描述为空时判定
if official_verify_desc == '':
    official_verify_desc = '未认证或暂无描述'

# 打印
print('------------------------------')
print('动态数据')
print('动态id:', dynamic_id)
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
print('认证状态:', official_verify_type)
print('认证类型:', official_role, '认证码:', official_role_num)
print('认证描述:', official_verify_desc)
print('------------------------------')

# 调用系统函数pause
os.system('pause')
