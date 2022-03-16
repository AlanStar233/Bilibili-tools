import requests
import json
import time
from lxml import html
from json import JSONDecodeError

# 预定义aid，bv2av_api，headers
aid = ''
bvid = ''
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

# 定义查询变量
# 根信息
response_code = video_data['code']  # 响应码
response_message = video_data['message']  # 错误信息

# 视频基本信息
bvid = video_data['data']['bvid']
video_Part = video_data['data']['videos']  # 稿件分P数
video_Area_tid = video_data['data']['tid']  # 稿件分区tID
video_Area_tname = video_data['data']['tname']  # 稿件子分区名
video_copyright = video_data['data']['copyright']  # 视频类型(1:原创 2:转载)
video_cover = video_data['data']['pic']  # 视频封面URL
video_title = video_data['data']['title']  # 视频标题
video_pubdate = video_data['data']['pubdate']  # 稿件发布时间
video_ctime = video_data['data']['ctime']  # 用户投稿时间
video_desc = video_data['data']['desc']  # 视频简介
video_duration = video_data['data']['duration']  # 稿件总时长
video_dynamic = video_data['data']['dynamic']  # 随视频发布的动态文字内容
video_cid = video_data['data']['cid']  # 视频CID(默认第1P)
video_dimension_width = video_data['data']['dimension']['width']  # 视频分辨率(默认第1P),宽
video_dimension_height = video_data['data']['dimension']['height']  # 视频分辨率(默认第1P),高
video_dimension_rotate = video_data['data']['dimension']['rotate']  # 视频分辨率(默认第1P),是否宽高对换

# 视频高级状态信息
# 视频状态
video_state = video_data['data']['state']
# 视频属性标志
video_rights_elec = video_data['data']['rights']['elec']  # 是否支持充电
video_rights_download = video_data['data']['rights']['download']  # 是否支持下载
video_rights_movie = video_data['data']['rights']['movie']  # 是否为电影
video_rights_PGC_pay = video_data['data']['rights']['pay']  # 是否为PGC付费
video_rights_HD5 = video_data['data']['rights']['hd5']  # 是否有高码率
video_rights_no_reprint = video_data['data']['rights']['no_reprint']  # 是否有禁止转载标志
video_rights_UGC_pay = video_data['data']['rights']['ugc_pay']  # 是否UGC付费
video_rights_stein_gate = video_data['data']['rights']['is_stein_gate']  # 是否为互动视频
video_rights_cooperation = video_data['data']['rights']['is_cooperation']  # 是否为联合投稿
video_subtitle = video_data['data']['subtitle']['allow_submit']  # 是否允许提交字幕
# 视频基本互动数据
video_stat_view = video_data['data']['stat']['view']  # 播放数
video_stat_danmaku = video_data['data']['stat']['danmaku']  # 弹幕数
video_stat_like = video_data['data']['stat']['like']  # 点赞数
video_stat_coin = video_data['data']['stat']['coin']  # 硬币数
video_stat_favorite = video_data['data']['stat']['favorite']  # 收藏数
video_stat_share = video_data['data']['stat']['share']  # 分享数
video_stat_reply = video_data['data']['stat']['reply']  # 评论数
video_stat_nowrank = video_data['data']['stat']['now_rank']  # 当前排名
video_stat_hisrank = video_data['data']['stat']['his_rank']  # 历史最高排行
video_stat_evaluation = video_data['data']['stat']['evaluation']  # 视频评分

# 视频所属UP主信息
video_owner_UID = video_data['data']['owner']['mid']  # up主UID
video_owner_name = video_data['data']['owner']['name']  # up主昵称

# 状态转换
# 状态码解读
response_status = ''
response_code = str(response_code)
if response_code == '0':
    response_status = '请求成功'
elif response_code == '-400':
    response_status = '请求错误'
elif response_code == '-403':
    response_status = '权限不足'
elif response_code == '-404':
    response_status = '无此视频'
elif response_code == '62002':
    response_status = '稿件不可见'
# 错误信息
response_message = str(response_message)
if response_message == '0':
    response_message = '暂无'
# 视频状态
video_state = str(video_state)
if video_state == '1':
    video_state = '橙色通过'
elif video_state == '0':
    video_state = '开放浏览'
elif video_state == '-1':
    video_state = '待审'
elif video_state == '-2':
    video_state = '被打回'
elif video_state == '-3':
    video_state = '网警锁定'
elif video_state == '-4':
    video_state = '视频撞车锁定'
elif video_state == '-5':
    video_state = '管理员锁定'
elif video_state == '-6':
    video_state = '修复待审'
elif video_state == '-7':
    video_state = '暂缓审核'
elif video_state == '-8':
    video_state = '补档待审'
elif video_state == '-9':
    video_state = '等待转码'
elif video_state == '-10':
    video_state = '延迟审核'
elif video_state == '-11':
    video_state = '视频源待修'
elif video_state == '-12':
    video_state = '转储失败'
elif video_state == '-13':
    video_state = '允许评论待审'
elif video_state == '-14':
    video_state = '临时回收站'
elif video_state == '-15':
    video_state = '分发中'
elif video_state == '-16':
    video_state = '转码失败'
elif video_state == '-20':
    video_state = '创建未提交'
elif video_state == '-30':
    video_state = '创建已提交'
elif video_state == '-40':
    video_state = '定时发布'
elif video_state == '-100':
    video_state = '用户删除'
# 视频类型
video_copyright = str(video_copyright)
if video_copyright == '1':
    video_copyright = '转载'
elif video_copyright == '2':
    video_copyright = '自制'
# 是否支持充电
video_rights_elec = str(video_rights_elec)
if video_rights_elec == '1':
    video_rights_elec = '是'
elif video_rights_elec == '0':
    video_rights_elec = '否'
# 是否支持下载
video_rights_download = str(video_rights_download)
if video_rights_download == '1':
    video_rights_download = '是'
elif video_rights_download == '0':
    video_rights_download = '否'
# 是否为电影
video_rights_movie = str(video_rights_movie)
if video_rights_movie == '1':
    video_rights_movie = '是'
elif video_rights_movie == '0':
    video_rights_movie = '否'
# 是否为UGC付费
video_rights_UGC_pay = str(video_rights_UGC_pay)
if video_rights_UGC_pay == '1':
    video_rights_UGC_pay = '是'
elif video_rights_UGC_pay == '0':
    video_rights_UGC_pay = '否'
# 是否为PGC付费
video_rights_PGC_pay = str(video_rights_PGC_pay)
if video_rights_PGC_pay == '1':
    video_rights_PGC_pay = '是'
elif video_rights_PGC_pay == '0':
    video_rights_PGC_pay = '否'
# 是否有高码率
video_rights_HD5 = str(video_rights_HD5)
if video_rights_HD5 == '1':
    video_rights_HD5 = '是'
elif video_rights_HD5 == '0':
    video_rights_HD5 = '否'
# 是否有禁止转载标识
video_rights_no_reprint = str(video_rights_no_reprint)
if video_rights_no_reprint == '1':
    video_rights_no_reprint = '是'
elif video_rights_no_reprint == '0':
    video_rights_no_reprint = '否'
# 是否为互动视频
video_rights_stein_gate = str(video_rights_stein_gate)
if video_rights_stein_gate == '1':
    video_rights_stein_gate = '是'
elif video_rights_stein_gate == '0':
    video_rights_stein_gate = '否'
# 是否为联合投稿
video_rights_cooperation = str(video_rights_cooperation)
if video_rights_cooperation == '1':
    video_rights_cooperation = '是'
elif video_rights_cooperation == '0':
    video_rights_cooperation = '否'
# 是否允许提交字幕
video_subtitle = str(video_subtitle)
if video_subtitle == 'True':
    video_subtitle = '是'
elif video_subtitle == 'False':
    video_subtitle = '否'
# 视频评分
video_stat_evaluation = str(video_stat_evaluation)
if video_stat_evaluation == '':
    video_stat_evaluation = '暂无评分'
# 时间戳转换
video_ctime = int(video_ctime)
video_pubdate = int(video_pubdate)

video_ctime = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(video_ctime))
video_pubdate = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime(video_pubdate))

# 打印结果
print('------------------------------')
print('API返回信息:')
print('响应码:', response_code)
print('响应解释:', response_status)
print('错误信息:', response_message)
print('------------------------------')
print('视频基本信息:')
print('视频标题:', video_title)
print('AV号:', aid, 'BV号:', bvid)
print('视频分区号:', video_Area_tid, '子分区名:', video_Area_tname)
print('******************************')
print('视频动态信息:', video_dynamic)
print('******************************')
print('视频简介:', video_desc)
print('******************************')
print('视频投稿时间:', video_ctime, '视频发布时间:', video_pubdate)
print('视频CID:', video_cid)
print('视频分辨率:', video_dimension_width, '*', video_dimension_height)
print('视频分P数:', video_Part, '个')
print('视频总时长:', video_duration, '秒')
print('视频类型:', video_copyright)
print('视频封面URL:', video_cover)
print('------------------------------')
print('视频高级状态信息:')
print('视频状态:', video_state)
print('是否支持充电:', video_rights_elec)
print('是否支持下载:', video_rights_download)
print('是否为电影:', video_rights_movie)
print('是否为UGC付费:', video_rights_UGC_pay)
print('是否为PGC付费:', video_rights_PGC_pay)
print('是否有高码率:', video_rights_HD5)
print('是否有禁止转载标志:', video_rights_no_reprint)
print('是否为互动视频:', video_rights_stein_gate)
print('是否为联合投稿:', video_rights_cooperation)
print('是否允许提交字幕:', video_subtitle)
print('------------------------------')
print('视频基本互动数据:')
print('播放数:', video_stat_view, '次')
print('弹幕数:', video_stat_danmaku, '条')
print('点赞数:', video_stat_like, '次')
print('硬币数:', video_stat_coin, '个')
print('收藏数:', video_stat_favorite, '次')
print('分享数:', video_stat_share, '次')
print('回复数:', video_stat_reply, '个')
print('当前站内排名:', video_stat_nowrank, '名')
print('历史最高排名:', video_stat_hisrank, '名')
print('视频评分:', video_stat_evaluation)
print('------------------------------')
print('视频所属up主信息:')
print('UP主UID:', video_owner_UID)
print('UP主昵称:', video_owner_name)
print('------------------------------')
