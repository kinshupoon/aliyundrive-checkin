import os
import requests
import re

# 从replit的secrets中读取值
enshanck = os.environ.get('ENSHANCK')
plustoken = os.environ.get('PUSHPLUS_TOKEN')
def Push(contents):
  # 推送加
  headers = {'Content-Type': 'application/json'}
  json_data = {
      "token": plustoken,
      'title': '恩山签到',
      'content': contents.replace('\n', '<br>'),
      "template": "json"
  }
  resp = requests.post('http://www.pushplus.plus/send',
                       json=json_data,
                       headers=headers).json()
  print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')


headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
    "Cookie": enshanck,
}

session = requests.session()
response = session.get(
    'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1',
    headers=headers)
try:
  coin = re.findall("恩山币: </em>(.*?)nb &nbsp;", response.text)[0]
  point = re.findall("<em>积分: </em>(.*?)<span", response.text)[0]
  res = f"恩山币：{coin}\n积分：{point}"
  print(res)
  Push(contents=res)
except Exception as e:
  res = str(e)
