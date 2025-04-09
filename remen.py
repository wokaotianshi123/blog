import requests

# 目标URL与文件配置
URL = "https://api.web.360kan.com/v1/rank?cat=7&callback=__jp0"
OUTPUT_FILE = "remen.txt"

try:
    # 1. 发起请求并解析JSONP
    response = requests.get(URL, timeout=10)
    content = response.text.strip()
    
    # 处理JSONP格式（移除回调函数包裹）
    if content.startswith('__jp0(') and content.endswith(');'):
        json_data = content[6:-2]  # 精准切片，跳过__jp0(和末尾的);
    else:
        raise ValueError("Invalid JSONP format")
    
    # 2. 解析数据并提取标题
    data = json.loads(json_data)
    raw_titles = [item['title'] for item in data.get('data', []) if 'title' in item]
    
    # 3. 保持顺序去重（Python 3.7+字典有序特性）
    unique_titles = list(dict.fromkeys(raw_titles))  # 保留首次出现顺序
    
    # 4. 写入文件（追加模式+UTF-8 BOM防止乱码）
    with open(OUTPUT_FILE, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(unique_titles))
    
    # 5. 结果反馈
    print(f"✨ 成功处理{len(raw_titles)}条数据，去重后保存{len(unique_titles)}条到{OUTPUT_FILE}")
    print("🔍 示例去重项：", end='')
    for title in unique_titles[:3]:  # 显示前3个去重标题
        print(f"「{title}」", end=' ')
    print()

except requests.exceptions.RequestException as e:
    print(f"🚨 网络请求失败：{str(e)}")
except (json.JSONDecodeError, KeyError) as e:
    print(f"🚨 数据解析失败：{str(e)}")
except Exception as e:
    print(f"🚨 发生未知错误：{str(e)}")
