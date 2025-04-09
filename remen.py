import requests
import json

# 定义目标URL
url = "https://api.web.360kan.com/v1/rank?cat=7&callback=__jp0"

# 发送HTTP请求获取内容
response = requests.get(url)
content = response.text

# 提取JSON数据（去掉回调函数前缀__jp0(）
json_start = content.find('{')
json_data = content[json_start:-2]  # 去掉最后的);

# 解析JSON
data = json.loads(json_data)
items = data.get('data', [])

# 提取所有title字段
titles = [item['title'] for item in items]

# 写入文件remen.txt，每个标题换行
with open('remen.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(titles))

print("数据已成功提取并保存到remen.txt")
