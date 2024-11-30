import requests,re,os,urllib.parse

#配置恩山的cookie 到配置文件config.sh export enshanck='' 需要推送配置推送加token export plustoken=''
enshanck = os.environ.get('ENSHANCK')
#推送加 token
plustoken = os.environ.get('PUSHPLUS_TOKEN')

def Push(title, content):
    # 对 title 和 content 进行 URL 编码
    encoded_title = urllib.parse.quote(title)
    encoded_content = urllib.parse.quote(content)

    # 构造推送的 URL，带上编码后的 title 和 content
    push_url = f'https://php.hipjs.cloudns.org/api/wxpush.php?txt1={encoded_title}&txt2={encoded_content}'

    # 发送 GET 请求
    try:
        response = requests.get(push_url)
        if response.status_code == 200:
            print('推送成功')
        else:
            print(f'推送失败，状态码: {response.status_code}')
    except Exception as e:
        print(f'推送请求失败: {e}')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Cookie": enshanck,
}
session = requests.session()
response = session.get('https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1', headers=headers)
try:
    coin = re.findall("恩山币: </em>(.*?)&nbsp;", response.text)[0]
    point = re.findall("<em>积分: </em>(.*?)<span", response.text)[0]
    res = f"恩山币：{coin}\n积分：{point}"
    print(res)
    # 调用新的 Push 函数
    Push(title='恩山签到', content=res)
  
except Exception as e:
    res = str(e)
    print(f'提取信息失败: {res}')
