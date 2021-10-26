import requests
import json
import Special_Tools_Functions as Fun
from lxml import html
from urllib.parse import urlparse

# 共定义了以下几种方法
# dynamic_data(url)
# dynamic_id(url)
# reply_pages(dynamic_id)

# 获取dynamic_data
dynamic_url = input('URL:')
data = Fun.dynamic_data(dynamic_url)

# 获取dynamic_id
dynamic_id = Fun.dynamic_id(dynamic_url)

# 获得reply_pages
pages = Fun.reply_pages(Fun.dynamic_id(dynamic_url))

# 打印数据
print('动态ID:', dynamic_id)
print('回复共有', pages, '页')