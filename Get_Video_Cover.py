import requests
import json
from lxml import html

# 预定义aid，bv2av_api，headers
aid = ''
bv2av_api = 'https://api.bilibili.com/x/web-interface/view'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# BV转AV
def bv_to_av(bv):
    r = requests.get(bv2av_api, {'bvid': bv}, headers=headers)
    response = decode_json(r)
    try:
        return str(response['data']['aid'])
    except (KeyError, TypeError):
        return '获取av号失败'

# 定义一个decode_json(r)方法
def decode_json(r):
    try:
        response = r.json()
    except JSONDecodeError:
        # 虽然用的是requests的json方法，但要捕获的这个异常来自json模块
        return -1
    else:
        return response

# 交互页面
mode = input('AV号模式(1) / BV号模式(2) :')
if mode == '1':
    aid = input('请输入视频av号(纯数字):')
elif mode == '2':
    bvid = input('请输入视频bv号:')
    aid = bv_to_av(bvid)

# 定义aid请求的api
aid_api = 'http://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)

# 获取视频信息
resp = requests.get(aid_api, headers=headers)
video_data = resp.text
selector = html.fromstring(video_data)

# 返回Python的数据类型
video_data = json.loads(video_data)

# json解析，定位pic所在的位置;定位title
pic_source = video_data['data']['pic']
title = video_data['data']['title']
uploader = video_data['data']['owner']['name']

# 打印结果
print('------------------------------')
print("视频标题为:", title)
print('------------------------------')
print("UP主为:", uploader)
print('------------------------------')
print("图片地址为:", pic_source)
print('------------------------------')




