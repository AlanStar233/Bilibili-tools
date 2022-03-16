import requests
import json

# # 创建 session 方法
# session = requests.session()
# # 请求登录
# print("**********登录模块**********")
# login_API = 'http://passport.bilibili.com/qrcode/getLoginUrl'
# login_headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
# }
# login_info_resp = requests.get(login_API, headers=login_headers)
# login_info_data = login_info_resp.text
# # 返回Python类型
# login_info_data = json.loads(login_info_data)
# # 取出登录链接
# login_check_link = login_info_data['data']['url']
# login_check_oauthKey = login_info_data['data']['oauthKey']
# # 生成二维码以供登录
# qrcode_img = qrcode.make(login_check_link)
# qrcode_img.save('./img/login.png')
# # 展示二维码
# print("请按任意键完成登录...")
# login_qrcode = cv.imread("./img/login.png")
# cv.imshow("bilibili-qrcode_login", login_qrcode)
# cv.waitKey(0)
# cv.destroyAllWindows()
#
# # 获得cookie
# tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
# 等待输入case_id
# 读取 cookie.txt
with open("./cookie.txt", "r") as doc:
    bili_cookie = doc.read()
    if bili_cookie == '':
        print("状态:")
        print("cookie.txt 文件为空!")
        print("请根据引导操作:")
        print("请打开处于B站登录态的浏览器，按F12，找到控制台(console)，在其中输入 document.cookie ")
        print("将控制台输出的结果完整复制到文件夹内的cookie.txt文件中，并保存")
        print("请执行操作!程序即将退出!")
        exit()
    else:
        print("状态:cookie获取完成!")
# 请求输入案件id
case_id = input("请输入需要查询的案件id:")

# headers 及各项API初始化
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "cookie": bili_cookie
}
# 案件详情
judge_API = 'https://api.bilibili.com/x/credit/v2/jury/case/info?case_id={}'.format(case_id)
# 众议观点(因后台控制，不可抓取前端不可见内容)
judge_content_API = 'https://api.bilibili.com/x/credit/v2/jury/case/opinion?case_id={}'.format(case_id)
# response
judge_info_resp = requests.get(judge_API, headers=headers)
judge_info_data = judge_info_resp.text
# 返回Python类型
judge_info_data = json.loads(judge_info_data)
# API状态解析
judge_info_code = judge_info_data['code']   # 服务器在json中返回的状态码
judge_info_status = judge_info_data['message']  # 服务器在json中返回的状态message
print("请求状态:", judge_info_code, judge_info_status)
# 开始 json 解析
# 注:存在一个case_id
# type = 1 AC14x411c74g
# type = 2 AC18x411c7Px
# type = 3 AC1bx411c7fi
# type = 4 AC14x411c7Kz
case_type = judge_info_data['data']['case_type']  # 1:单条评论    2:评论氛围    3:单条弹幕    4:弹幕氛围
case_avid = judge_info_data['data']['avid']  # AV号
case_cid = judge_info_data['data']['cid']  # cid
case_vote_cd = judge_info_data['data']['vote_cd']   # 投票冷却时间
case_result_text = judge_info_data['data']['result_text']   # 系统综合结果
case_content_title = judge_info_data['data']['title']   # 稿件标题

# case_info 对应的参数
# 在case_type = 1 时的情形
if case_type == 1:
    case_type_desc = '单条评论' # 对case类型的描述
    case_uname = judge_info_data['data']['case_info']['comment']['uname']  # type=1
    case_content = judge_info_data['data']['case_info']['comment']['content']  # type=1
    case_child_comments = judge_info_data['data']['case_info']['child_comments']  # type=1
    case_danmaku_img = '不支持'  # type=4
# 在case_type = 2 时的情形
# elif case_type == 2:

# 在case_type = 3 时的情形
elif case_type == 3:
    case_type_desc = '单条弹幕'
    case_uname = '不支持'
    case_content = judge_info_data['data']['case_info']['single_danmu']['content']
    case_chiled_comments = '不支持'
# 在case_type = 4 时的情形
elif case_type == 4:
    case_type_desc = '弹幕氛围' # 对case类型的描述
    case_uname = '不支持'  # type=1
    case_content = '不支持'  # type=1
    case_child_comments = '不支持'  # type=1
    case_danmaku_img = judge_info_data['data']['case_info']['danmu_img']  # type=4

# 投票情况
case_all_opinion = judge_info_data['data']['vote_info']['all_count']
case_good_opinion = judge_info_data['data']['vote_info']['counts'][0]
case_normal_opinion = judge_info_data['data']['vote_info']['counts'][1]
case_bad_opinion = judge_info_data['data']['vote_info']['counts'][2]
case_denied_opinion = judge_info_data['data']['vote_info']['counts'][3]

# 抓取众议观点基础参数
judge_content_resp = requests.get(judge_content_API, headers=headers)
judge_content_data = judge_content_resp.text
# 返回Python类型
judge_content_data = json.loads(judge_content_data)
# 众议观点总数
case_comment_num = int(judge_content_data['data']['total'])
# 每页只有20条众议观点
if case_comment_num % 20 != 0:
    page = int((case_comment_num - case_comment_num % 20) / 20 + 1)
else:
    page = int(case_comment_num / 20)
# 数值初始化
r = 0
page_num = 1
times = 0
# 输出
print("**********************************************************************")
print("案件简介:")
print("案件类型:", case_type_desc, "案件类型id:", case_type)
print("案件标题:", case_content_title, '|', "AV号:", case_avid, "cid:", case_cid)
print("----------------------------------------------------------------------")
print("案件详情:")
print("涉案角色昵称:", case_uname, "涉案评论:", case_child_comments)
print("涉案弹幕截图:", case_danmaku_img)
print("投票冷却时间:", case_vote_cd, "秒")
print("----------------------------------------------------------------------")
print("投票情况:")
print("总投票数:", case_all_opinion)
print("好:", case_good_opinion, "普通:", case_normal_opinion, "差:", case_bad_opinion, "无法判断:", case_denied_opinion)
print("----------------------------------------------------------------------")
print("众议观点:")
for page in range(1, page + 1):
    comment_API = 'https://api.bilibili.com/x/credit/v2/jury/case/opinion?case_id={}&pn={}&ps=20'.format(case_id, page_num)
    comment_resp = requests.get(comment_API, headers=headers)
    comment_data = json.loads(comment_resp.text)
    r_max = len(comment_data['data']['list'])
    print('=====当前是第', page_num, '页=====')
    for r in range(0, r_max):
        comment_opid = comment_data['data']['list'][r]['opid']
        comment_mid = comment_data['data']['list'][r]['mid']
        comment_uname = comment_data['data']['list'][r]['uname']
        comment_vote_text = comment_data['data']['list'][r]['vote_text']
        comment_content = comment_data['data']['list'][r]['content']
        comment_anonymous = comment_data['data']['list'][r]['anonymous']
        if comment_anonymous == 0:
            comment_anonymous = '实名'
        else:
            comment_anonymous = '匿名'
        comment_like = comment_data['data']['list'][r]['like']
        comment_hate = comment_data['data']['list'][r]['hate']
        print("*****这是第", times + 1, "条评论****")
        print("opid:", comment_opid, "|", "uid:", comment_mid)
        print("发送者:", comment_uname, "|", "状态:", comment_anonymous)
        print("众议观点:", comment_vote_text, "众议内容:", comment_content)
        print("赞:", comment_like, "|", "踩:", comment_hate)
        times = times + 1
    page_num = page_num + 1
    # 如遇管控策略，导致计算出的页数和实际数量不符，则结束程序
    if len(comment_data['data']['list']) == 0:
        break