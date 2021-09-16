import requests
import json
import time
from lxml import html

# 定义uid，api，headers
uid = input('请输入用户UID:')
api = 'http://api.bilibili.com/x/space/acc/info?mid={}'.format(uid)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# 配置response和user_data
resp = requests.get(api, headers=headers)
user_data = resp.text
selector = html.fromstring(user_data)

# 返回Python数据类型
user_data = json.loads(user_data)

# 定义查询变量
# 个人信息
NickName = user_data['data']['name']  # 昵称
sign = user_data['data']['sign']  # 用户签名
level = user_data['data']['level']  # 用户等级
sex = user_data['data']['sex']  # 用户性别
silence = user_data['data']['silence']  # 0为正常，1为封禁
birthday = user_data['data']['birthday']  # 若进行隐私设置则为空
fans_badge = user_data['data']['fans_badge']  # 是否有粉丝勋章

# 认证信息
official_role = user_data['data']['official']['role']  # 0:无认证  1,2:个人认证  3,4,5,6:企业认证
official_title = user_data['data']['official']['title']  # 认证信息
official_desc = user_data['data']['official']['desc']  # 认证备注
official_type = user_data['data']['official']['type']  # 是否认证 -1:未认证 0:认证

# VIP信息
VIP_type = user_data['data']['vip']['type']  # VIP类型 0:无 1:月度大会员 2:年度大会员
VIP_status = user_data['data']['vip']['status']  # VIP状态 0:无 1:有
VIP_due_date = user_data['data']['vip']['due_date']  # VIP到期日期 (Unix时间戳)
VIP_label = user_data['data']['vip']['label']['text']  # VIP标签 即文案，有:大会员 年度大会员 十年大会员 百年大会员

# 直播间状态
LiveRoom_roomStatus = user_data['data']['live_room']['roomStatus']  # 直播间状态 0:无房间 1:有房间
LiveRoom_liveStatus = user_data['data']['live_room']['liveStatus']  # 直播状态 0:未开播 1:直播中
LiveRoom_url = user_data['data']['live_room']['url']  # 直播间地址
LiveRoom_title = user_data['data']['live_room']['title']  # 直播间标题
LiveRoom_Cover = user_data['data']['live_room']['cover']  # 直播间封面地址
LiveRoom_online = user_data['data']['live_room']['online']  # 直播间人气
LiveRoom_roomid = user_data['data']['live_room']['roomid']  # 直播间ID(短号)

# 状态转换
# ------------------------------------------------------------

# 个人信息

# 用户封禁状态转换
if silence == 0:
    silence = '正常'
elif silence == 1:
    silence = '已封禁'

# 用户生日转换
if birthday == '':
    birthday = '隐私设置，无法访问'

# 用户粉丝勋章状态转换
if fans_badge == 1:
    fans_badge = '是'
elif fans_badge == 0:
    fans_badge = '否'

# ------------------------------------------------------------

# 认证信息

# 是否认证状态转换(原num)
official_type = str(official_type)
if official_type == '-1':
    official_type = '未认证'
elif '0' <= official_type <= '1':
    official_type = '已认证'

# 认证类别状态转换
official_role_status = ''
if official_role == 0:
    official_role_status = '未认证'
elif 1 <= official_role <= 2:
    official_role_status = '个人认证'
elif 3 <= official_role <= 6:
    official_role_status = '企业认证'
elif official_role == 7:
    official_role_status = '个人认证'
elif official_role == 8:
    official_role_status = '专业领域认证'

# 认证类型
official_role_type = ''
if official_role == 0:
    official_role_type = '未认证'
elif official_role == 1:
    official_role_type = '知名UP主认证'
elif official_role == 2:
    official_role_type = '个人身份认证'
elif official_role == 3:
    official_role_type = '企业认证'
elif official_role == 4:
    official_role_type = '政府认证'
elif official_role == 5:
    official_role_type = '媒体认证'
elif official_role == 6:
    official_role_type = '组织认证'
elif official_role == 7:
    official_role_type = '个人领域认证'
elif official_role == 8:
    official_role_type = '职业资质认证'
# 认证备注状态转换
if official_desc == '':
    official_desc = '无'

# ------------------------------------------------------------

# VIP信息

# VIP类型状态转换(原num)
VIP_type = str(VIP_type)
if VIP_type == '0':
    VIP_type = '无'
elif VIP_type == '1':
    VIP_type = '月度大会员'
elif VIP_type == '2':
    VIP_type = '年度大会员'

# VIP状态 状态转换(原num)
VIP_status = str(VIP_status)
if VIP_status == '0':
    VIP_status = '已失效'
elif VIP_status == '1':
    VIP_status = '生效中'

# VIP到期日期 格式化
VIP_due_date = VIP_due_date/1000
# print('VIP_due_date type:', type(VIP_due_date))
VIP_due_date = time.strftime('%Y{Y}%m{m}%d{d} %H:%M:%S', time.localtime(VIP_due_date)).format(Y='年', m='月', d='日')

# ------------------------------------------------------------

# 直播间状态

# 是否拥有直播间 状态转换(原num)
LiveRoom_roomStatus = str(LiveRoom_roomStatus)
if LiveRoom_roomStatus == '0':
    LiveRoom_roomStatus = '无房间'
elif LiveRoom_roomStatus == '1':
    LiveRoom_roomStatus = '有房间'

# 直播状态 状态转换(原num)
LiveRoom_liveStatus = str(LiveRoom_liveStatus)
if LiveRoom_liveStatus == '0':
    LiveRoom_liveStatus = '未开播'
elif LiveRoom_liveStatus == '1':
    LiveRoom_liveStatus = '直播中'

# 直播间标题 状态转换
if LiveRoom_title == '':
    LiveRoom_title = '该直播间暂无标题'

# 直播间封面地址 状态转换
if LiveRoom_Cover == '':
    LiveRoom_Cover = '该直播间暂无封面'

# ------------------------------------------------------------

# 打印结果
print('------------------------------')
print('用户个人信息:')
print('UID:', uid)
print('用户名:', NickName)
print('用户性别:', sex)
print('用户等级:', 'lv', level)
print('用户签名:', sign)
print('用户状态:', silence)
print('生日:', birthday)
print('是否拥有自己的粉丝勋章:', fans_badge)
print('------------------------------')
print('认证信息:')
print('是否认证:', official_type)
print('认证类别:', official_role_status, '认证类型:', official_role_type, '认证代码:', official_role)
print('认证信息:', official_title)
print('认证备注:', official_desc)
print('------------------------------')
print('VIP类型:', VIP_type)
print('VIP标签:', VIP_label)
print('VIP状态:', VIP_status)
print('VIP到期日期:', VIP_due_date)
print('------------------------------')
print('直播间状态:')
print('是否拥有直播间:', LiveRoom_roomStatus)
print('直播间地址:', LiveRoom_url)
print('直播间ID:', LiveRoom_roomid)
print('直播间标题:', LiveRoom_title)
print('直播间封面地址:', LiveRoom_Cover)
print('直播状态:', LiveRoom_liveStatus)
print('直播间人气', LiveRoom_online)
print('※注意:直播间若在未开播状态下，直播间人气将保留上次直播结束时的数据')
print('------------------------------')