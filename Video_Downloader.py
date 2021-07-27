import qrcode
import requests
import json
from lxml import html
from PIL import Image

# 配置loginAPI,headers
login_api = 'https://passport.bilibili.com/qrcode/getLoginUrl'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

# 配置返回总数据
login_resp = requests.get(login_api, headers=headers)
login_data = login_resp.text
login_data_selector = html.fromstring(login_data)

# 返回Python数据类型
login_data = json.loads(login_data)

login_url = login_data['data']['url']
oauthKey = login_data['data']['oauthKey']

# 获得登录URL并转为二维码展示
login_qrcode = qrcode.make(login_url)
login_qrcode.save("./img/login.png")
login_qrcode = Image.open("./img/login.png")
login_qrcode.show()

print(login_url)
print(oauthKey)