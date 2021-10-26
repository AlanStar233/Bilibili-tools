import requests
import json
import qrcode
from PIL import Image
import time
import win32api,win32con
from win10toast import ToastNotifier
import os
from lxml import html
from urllib.parse import urlparse

# 预定义login_api，headers
# 此处api不能使用https协议
login_api = 'http://passport.bilibili.com/qrcode/getLoginUrl'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

login_resp = requests.get(login_api, headers=headers)
login_data = login_resp.text

# 返回Python数据类型
login_data = json.loads(login_data)

code = login_data['code']
ts = login_data['ts']
url = login_data['data']['url']
oauthKey = login_data['data']['oauthKey']

print('code:', code)
print('时间戳:', ts)
print('url:', url)
print('登录密钥:', oauthKey)

# 生成二维码，以供扫描
qrcode_img = qrcode.make(url)
qrcode_img.save('./img/login.png')
qrcode_img = Image.open('./img/login.png')
qrcode_img.show()

# 线程睡眠15秒，等待扫码完毕
# win32api.MessageBox(0, "请在15秒内完成登录", "提示", win32con.MB_OK)
toaster = ToastNotifier()
toaster.show_toast("提示", "请在15秒内完成登录!")
time.sleep(15)

# 再次引用，检查code， true:已确认 -4:已扫描 -5:二维码超时或错误(检查密钥有效性)
check_api = 'http://passport.bilibili.com/qrcode/getLoginInfo?oauthKey={}'.format(oauthKey)
check_login = requests.post(check_api, headers=headers)
check_login_data = check_login.text

# 返回Python数据类型
check_login_data = json.loads(check_login_data)
check_code = check_login_data['code']
check_ts = check_login_data['ts']
check_url = check_login_data['data']['url']

if check_code == 0:
    toaster.show_toast("登录状态", "登录成功!")
elif check_code == -4:
    toaster.show_toast("登录状态", "已扫描，但未完成登录!")
elif check_code == -5:
    toaster.show_toast("登录状态", "二维码超时或错误!请检查密钥有效性或重新执行程序!")

print(check_url)
