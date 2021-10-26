import requests
import json
from lxml import html
from urllib.parse import urlparse

# 通过输入的动态URL提取path，即未处理的dynamic_id
url = input('请输入动态URL:')
parsed_result = urlparse(url)
url_path = parsed_result.path

# 获取dynamic_id (去除'/')
dynamic_id = url_path.replace('/', '')

# 请求一次API，返回页数
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

dynamic_api = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(
    dynamic_id)
dynamic_resp = requests.get(dynamic_api, headers=headers)
dynamic_data = json.loads(dynamic_resp.text)
# dynamic_type
# dynamic_type = 1  转发消息
# dynamic_type = 2  图文
# dynamic_type = 4  纯文字
# dynamic_type = 8  视频投稿
# dynamic_type = 16 小视频
# dynamic_type = 64 专栏
dynamic_type = int(dynamic_data['data']['card']['desc']['type'])
print('dynamic_type:', dynamic_type)
# reply_type
# reply_type = 11 图文
# reply_type = 17 纯文字
# reply_type = 1  视频投稿
# reply_type = 5  小视频
# reply_type = 12 专栏
if dynamic_type == 2:  # 图文
    reply_type = 11
    rid = dynamic_data['data']['card']['desc']['rid']
    reply_getpage_api = 'https://api.bilibili.com/x/v2/reply?sort=0&type={}&oid={}'.format(reply_type, rid)
    reply_getpage_resp = requests.get(reply_getpage_api, headers=headers)
    reply_getpage_data = json.loads(reply_getpage_resp.text)
    # 评论总数(主楼)
    main_floor = int(reply_getpage_data['data']['page']['count'])
elif dynamic_type == 4:  # 纯文字
    reply_type = 17
    reply_getpage_api = 'https://api.bilibili.com/x/v2/reply?sort=0&type={}&oid={}'.format(reply_type, dynamic_id)
    reply_getpage_resp = requests.get(reply_getpage_api, headers=headers)
    reply_getpage_data = json.loads(reply_getpage_resp.text)
    # 评论总数(主楼)
    main_floor = int(reply_getpage_data['data']['page']['count'])
elif dynamic_type == 1:  # 转发消息
    reply_type = 17
    reply_getpage_api = 'https://api.bilibili.com/x/v2/reply?sort=0&type={}&oid={}'.format(reply_type, dynamic_id)
    reply_getpage_resp = requests.get(reply_getpage_api, headers=headers)
    reply_getpage_data = json.loads(reply_getpage_resp.text)
    # 评论总数(主楼)
    main_floor = int(reply_getpage_data['data']['page']['count'])
# 每页只有20条主楼评论
if main_floor % 20 != 0:
    page = int((main_floor - main_floor % 20) / 20 + 1)
else:
    page = int(main_floor / 20)

# 楼ID(rpid),需要嵌套获取，用pn翻页，pn默认值为1
r = 0
page_num = 1
times = 0
print('----------------------------------------')
# 如果reply_type == 11
# 应该获取的是rid
if reply_type == 11:
    for page in range(1, page + 1):
        reply_api = 'https://api.bilibili.com/x/v2/reply?sort=0&type={}&oid={}&pn={}'.format(reply_type, rid, page_num)
        reply_resp = requests.get(reply_api, headers=headers)
        reply_data = json.loads(reply_resp.text)
        r_max = len(reply_data['data']['replies'])
        print('=====当前是第', page_num, '页=====')
        for r in range(0, r_max):
            reply_content = reply_data['data']['replies'][r]['content']['message']
            reply_id = reply_data['data']['replies'][r]['rpid']
            reply_sender = reply_data['data']['replies'][r]['member']['uname']
            reply_sender_uid = reply_data['data']['replies'][r]['member']['mid']
            print('*****这是第', times + 1, '条评论*****')
            print('评论内容:', reply_content)
            print('评论ID:', reply_id)
            print('发送者:', reply_sender, '用户UID:', reply_sender_uid)
            times = times + 1
        page_num = page_num + 1
# 如果reply_type == 17
# 应该获取的是dynamic_id
elif reply_type == 17:
    for page in range(1, page + 1):
        reply_api = 'https://api.bilibili.com/x/v2/reply?sort=0&type={}&oid={}&pn={}'.format(reply_type, dynamic_id, page_num)
        reply_resp = requests.get(reply_api, headers=headers)
        reply_data = json.loads(reply_resp.text)
        # 考虑到只有两层主楼的情况，此时r_max会取1，而for取值为双开区间，则需要r_max值+1，即为2
        r_max = len(reply_data['data']['replies'])
        print('=====当前是第', page_num, '页=====')
        for r in range(0, r_max):
            reply_content = reply_data['data']['replies'][r]['content']['message']
            reply_id = reply_data['data']['replies'][r]['rpid']
            reply_sender = reply_data['data']['replies'][r]['member']['uname']
            reply_sender_uid = reply_data['data']['replies'][r]['member']['mid']
            print('*****这是第', times + 1, '条评论*****')
            print('评论内容:', reply_content)
            print('评论ID:', reply_id)
            print('发送者:', reply_sender, '用户UID:', reply_sender_uid)
            times = times + 1
        page_num = page_num + 1
# 打印信息
print('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
print('全局消息:')
print('该动态有', main_floor, '层主楼')
print('共计', times, '条可见主楼回复')
print('该动态共有', page, '页')
print('共有', main_floor - times, '条信息被折叠')
print('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')

# 测试
# dynamic_type = 2  图文  ok
# dynamic_type = 4  纯文字 ok
