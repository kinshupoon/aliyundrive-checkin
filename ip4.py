import requests
from bs4 import BeautifulSoup
import csv
import ipaddress

url = 'http://ip.bczs.net/city'
response = requests.get(url)

if response.status_code == 200:
  html_doc = response.text
  soup = BeautifulSoup(html_doc, 'html.parser')

  table_body = soup.find('tbody')
  rows = table_body.find_all('tr')

  codes = []  # 定义空列表

  data = []
  for row in rows:
    cols = row.find_all('td')
    code = cols[0].text.strip()
    name_tag = cols[1].a
    name = name_tag.text.strip() if name_tag else cols[1].text.strip()
    full_name_tag = cols[2].a
    full_name = full_name_tag.text.strip(
    ) if full_name_tag else cols[2].text.strip()
    level = cols[3].text.strip()

    codes.append((code, name))  # 将元组(code, name)添加到codes列表中
    data.append((code, name, full_name, level))

# 将抓取的数据写入CSV文件
with open('国内城市IP.csv', mode='w', newline='', encoding='utf-8-sig') as file:
  writer = csv.writer(file)
  writer.writerow(["代码", "区划名称", "区划全称", "级别"])  # 添加标题行
  for row in data:
    writer.writerow(row)


def process_url(url):
  response = requests.get(url)

  if response.status_code == 200:
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')

    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')

    data = []
    for row in rows:
      cols = row.find_all('td')
      start_ip = cols[0].text
      end_ip = cols[1].text
      quantity = int(cols[2].text)  # 将数量转换为整数
      network = cols[3].text
      title = cols[0].a['title']  # 获取title属性
      data.append([start_ip, end_ip, quantity, network, title,
                   url])  # 添加城市信息到data列表中，并添加来源URL
    return data
  else:
    print(f"Failed to retrieve the page: {url}")
    return [], 0


# 从上面的代码段获取codes列表
codes = [code[0] for code in codes]
urls = [f'http://ip.bczs.net/city/{code}' for code in codes]

all_data = []
total_quantities = {}  # 创建一个字典，用于存储每个网址的IP数量总和
for url in urls:
  data = process_url(url)
  all_data.extend(data)  # 将每个URL的数据合并到all_data列表中

with open('ip_ranges.csv', mode='w', newline='', encoding='utf-8-sig') as file:
  writer = csv.writer(file)
  writer.writerow(["起始IP", "结束IP", "数量", "网络", "城市", "来源"])  # 添加来源列
  for row in all_data:
    writer.writerow(row)

#将ip地址范围转为cidr地址
# 读取csv文件
data = []
with open('ip_ranges.csv', 'r', encoding='utf-8-sig') as file:
  reader = csv.reader(file)
  next(reader)  # 跳过第一行说明文字
  for row in reader:
    data.append(row)

# 处理并输出结果
output_data = []
for entry in data:
  start_ip = ipaddress.ip_address(entry[0])
  end_ip = ipaddress.ip_address(entry[1])

  # 计算CIDR地址
  cidr_list = list(ipaddress.summarize_address_range(start_ip, end_ip))
  cidr_str_list = [str(cidr) for cidr in cidr_list]
  quantity_list = [cidr.num_addresses for cidr in cidr_list]

  # 将每个CIDR地址及其数量添加到输出数据列表中
  for cidr_str, quantity in zip(cidr_str_list, quantity_list):
    network = entry[3]
    city_info = entry[4].split("：")[-1] if len(entry) > 4 else ""  # 避免索引错误
    city = city_info.split("IP地址段:")[0]  # 提取"广东省茂名市"部分
    output_data.append([cidr_str, quantity, network, city])

# 将结果写入新的CSV文件
with open('cidr_ip.csv', 'w', newline='', encoding='utf-8-sig') as file:
  writer = csv.writer(file)
  writer.writerow(['CIDR', 'Quantity', 'Network', 'City'])  # 写入标题行
  writer.writerows(output_data)
