import requests
import json
import time
from lxml import html

# 定义变量
r = 0
# headers及各项API初始化
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}
# 每周必看抓取周数列表
week_pop_week_API = 'https://api.bilibili.com/x/web-interface/popular/series/list'
# 每周必看
# weekly_pop_API = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'.format(week_id)

# 每周必看数据抓取
# response
week_pop_resp = requests.get(week_pop_week_API, headers=headers)
week_pop_week_data = week_pop_resp.text
# 返回Python数据类型
week_pop_week_data = json.loads(week_pop_week_data)
# 最新一期的期号
week_id_now = week_pop_week_data['data']['list'][0]['number']
print("最新一期为:", week_id_now, "期")
week_id = input("请输入查看的期数:")
week_id = int(week_id)
if week_id > week_id_now or week_id < 1:
    print("期数数值不合法!")
else:
    # response
    weekly_pop_API = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'.format(week_id)
    week_pop_resp = requests.get(weekly_pop_API, headers=headers)
    week_pop_data = week_pop_resp.text
    # 返回Python数据类型
    week_pop_data = json.loads(week_pop_data)
    # 每周必看主属性
    week_pop_data_title = week_pop_data['data']['config']['subject']
    week_pop_data_name = week_pop_data['data']['config']['name']
    week_pop_data_label = week_pop_data['data']['config']['label']
    # 仅用于分享时的卡片生成文案
    week_pop_data_share_title = week_pop_data['data']['config']['share_title']
    week_pop_data_share_subtitle = week_pop_data['data']['config']['share_subtitle']

    # 稿件个数检测
    week_pop_data_content_counts = len(week_pop_data['data']['list'])
    # 生成
    print("********************************************************************************")
    print("期数信息:", week_pop_data_name, "||", "标签:", week_pop_data_label)
    print("合集标题:", week_pop_data_title)
    print("********************************************************************************")
    print("本期稿件个数为:", week_pop_data_content_counts)
    print("********************************************************************************")
    for r in range(0, week_pop_data_content_counts + 1):
        # 视频信息
        week_pop_data_content_aid = week_pop_data['data']['list'][r]['aid']
        week_pop_data_content_parts = week_pop_data['data']['list'][r]['videos']
        week_pop_data_content_title = week_pop_data['data']['list'][r]['title']
        week_pop_data_content_pubdate = week_pop_data['data']['list'][r]['pubdate']
        week_pop_data_content_desc = week_pop_data['data']['list'][r]['desc']
        # up主数据
        week_pop_data_content_uploader_mid = week_pop_data['data']['list'][r]['owner']['mid']
        week_pop_data_content_uploader_name = week_pop_data['data']['list'][r]['owner']['name']
        # 视频互动数据
        week_pop_data_content_stat_view = week_pop_data['data']['list'][r]['stat']['view']
        week_pop_data_content_stat_danmaku = week_pop_data['data']['list'][r]['stat']['danmaku']
        week_pop_data_content_stat_reply = week_pop_data['data']['list'][r]['stat']['reply']
        week_pop_data_content_stat_favorite = week_pop_data['data']['list'][r]['stat']['favorite']
        week_pop_data_content_stat_coin = week_pop_data['data']['list'][r]['stat']['coin']
        week_pop_data_content_stat_share = week_pop_data['data']['list'][r]['stat']['share']
        week_pop_data_content_stat_nowrank = week_pop_data['data']['list'][r]['stat']['now_rank']
        week_pop_data_content_stat_hisrank = week_pop_data['data']['list'][r]['stat']['his_rank']
        week_pop_data_content_stat_like = week_pop_data['data']['list'][r]['stat']['like']
        week_pop_data_content_stat_dynamic = week_pop_data['data']['list'][r]['dynamic']
        # 推荐语
        week_pop_data_content_rcmd_reason = week_pop_data['data']['list'][r]['rcmd_reason']
        # 其他数据
        week_pop_data_content_short_link = week_pop_data['data']['list'][r]['short_link']

        # 数据处理
        week_pop_data_content_pubdate_format = time.strftime('%Y{Y}%m{m}%d{d} %H:%M:%S', time.localtime(week_pop_data_content_pubdate)).format(Y='年', m='月', d='日')

        # 打印
        print("[", r+1, "]", "AV号:", week_pop_data_content_aid)
        print("标题:", week_pop_data_content_title)
        print("发布时间:", week_pop_data_content_pubdate_format, "分P:", week_pop_data_content_parts)
        print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
        print("简介:", week_pop_data_content_desc)
        print("********************************************************************************")