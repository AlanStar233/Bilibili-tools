import os.path
import requests
import json
import time
import sqlite3 as sqlite

# 数据库初始化
judgement_exist = os.path.exists("judgement.db")
if judgement_exist == 1:
    print("\033[93m数据库已存在!\033[0m")
else:
    # 创建数据库文件
    judgement_db = sqlite.connect("judgement.db")
    print("\033[92m数据库创建成功!\033[0m")
    # 创建游标
    judgement_cursor = judgement_db.cursor()
    judgement_cursor.execute('''CREATE TABLE judgement
    (case_id char(50) not null,
    opid int not null, 
    uid int not null,
    uname char(50) not null,
    vote int not null,
    content char(200) not null,
    anonymous int not null,
    like int not null,
    hate int not null,
    like_status int not null,
    vote_time int not null,
    insiders int not null);''')
    judgement_db.commit()
    judgement_db.close()

# 定义cookie并判定
cookie_file_exist = os.path.exists("cookie.txt")
if cookie_file_exist == 1:  # 如果cookie文件存在
    print("\033[93mcookie文件存在!\033[0m")
    with open("./cookie.txt", "r") as doc:
        bili_cookie = doc.read()
    if bili_cookie == '':
        print("\033[31mcookie文件为空!请填入cookie!\033[0m")
        os.system(pause)
        os.system(exit())
else:                       # 如果cookie文件不存在
    os.mknod("cookie.txt")
    print("\033[31mcookie文件不存在,已创建,请自行补充!\033[0m")
    os.system(pause)
    os.system(exit())

# 定义请求头部
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "cookie": bili_cookie
}

# 定义基本变量
pn = 1
i = 0
j = 0
# 定义 case_id 作为输入内容
case_id = input("请输入需要查询的case_id:")

# 定义API
judgement_API = 'https://api.bilibili.com/x/credit/v2/jury/case/opinion?case_id={}&pn={}&ps=20'.format(case_id, pn)

# 请求数据并格式化json
judgement_data = requests.get(judgement_API, headers=headers)
judgement_data = judgement_data.text
judgement_data = json.loads(judgement_data)

# 提取观点总数
total_count = judgement_data['data']['total']
page_num = int(total_count / 20) + 1

# 表头
# print("|观点id|\t", "UID|\t", "用户名|\t", "投票权重(?)|\t", "观点|\t", "是否匿名|\t", "赞|\t", "踩|\t", "点赞状态|\t", "投票时间戳|\t", "insiders|")

for pn in range(1, page_num + 1):
    # 循环请求数据
    judgement_API = 'https://api.bilibili.com/x/credit/v2/jury/case/opinion?case_id={}&pn={}&ps=20'.format(case_id, pn)
    judgement_data = requests.get(judgement_API, headers=headers)
    judgement_data = judgement_data.text
    judgement_data = json.loads(judgement_data)
    page_lens = len(judgement_data['data']['list'])     # 求单page结构个数
    for i in range(0, page_lens):
        opid = judgement_data['data']['list'][i]['opid']
        uid = judgement_data['data']['list'][i]['mid']
        uname = judgement_data['data']['list'][i]['uname']
        vote = judgement_data['data']['list'][i]['vote']
        content = judgement_data['data']['list'][i]['content']
        anonymous = judgement_data['data']['list'][i]['anonymous']
        like = judgement_data['data']['list'][i]['like']
        hate = judgement_data['data']['list'][i]['hate']
        like_status = judgement_data['data']['list'][i]['like_status']
        vote_time = judgement_data['data']['list'][i]['vote_time']
        insiders = judgement_data['data']['list'][i]['insiders']
        # 数据写入
        judgement_db = sqlite.connect("judgement.db")
        judgement_cursor = judgement_db.cursor()
        judgement_cursor.execute(
            '''INSERT INTO "main"."judgement" ("case_id", "opid", "uid","uname", "vote", "content", "anonymous", "like", "hate", "like_status", "vote_time", "insiders") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
            (case_id, opid, uid, uname, vote, content, anonymous, like, hate, like_status, vote_time, insiders))
        judgement_db.commit()
        judgement_db.close()
        # print("|", opid, "\t|", uid, "\t|", uname, "\t|", vote, "\t|", content, "\t|", anonymous, "\t|", like, "\t|", hate, "\t|", like_status, "\t|", vote_time, "\t|", insiders, "\t|")

print("\033[92m写入已完成!\033[0m")