import requests
import json  # 新增必要的json模块导入

# 目标URL与文件配置
URL = "https://api.web.360kan.com/v1/rank?cat=7&callback=__jp0"
OUTPUT_FILE = "remen.txt"

try:
    # 1. 发起请求并解析JSONP
    response = requests.get(URL, timeout=10)
    content = response.text.strip()
    
    # 严格校验JSONP格式
    if not (content.startswith('__jp0(') and content.endswith(');')):
        raise ValueError("Invalid JSONP format: 缺少回调函数包裹")
    
    # 精准提取JSON数据（跳过__jp0(和末尾的);）
    json_data = content[6:-2]
    
    # 2. 解析数据并提取标题（新增数据格式校验）
    try:
        data = json.loads(json_data)  # 明确使用json模块
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {str(e)}") from e  # 保留原始异常链
    
    if not isinstance(data, dict) or 'data' not in data:
        raise KeyError("响应数据结构异常，缺少'data'字段")
    
    raw_titles = []
    for item in data['data']:
        if isinstance(item, dict) and 'title' in item:
            raw_titles.append(item['title'])
    
    # 3. 保持顺序去重（Python 3.7+字典有序特性）
    unique_titles = list(dict.fromkeys(raw_titles))
    
    # 4. 写入文件（追加模式+UTF-8 BOM防止乱码）
    with open(OUTPUT_FILE, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(unique_titles))
    
    # 5. 结果反馈（新增数据统计）
    print(f"✅ 任务完成：")
    print(f"  ▶ 原始数据: {len(raw_titles)}条")
    print(f"  ▶ 去重后: {len(unique_titles)}条（去重率{len(raw_titles)-len(unique_titles)}/{len(raw_titles)}）")
    print(f"  ▶ 保存路径: {OUTPUT_FILE}（当前目录）")
    print("  ▶ 示例标题: " + ' | '.join(unique_titles[:3]))

except requests.exceptions.RequestException as e:
    print(f"🌐 网络错误: {str(e)}")
except (KeyError, ValueError) as e:
    print(f"📡 数据格式错误: {str(e)}")
except Exception as e:
    print(f"⚠️ 意外错误: {str(e)}", file=sys.stderr)  # 错误输出到stderr
    raise  # 保留异常堆栈便于调试

finally:
    if 'response' in locals() and not response.ok:
        print(f"状态码警告: HTTP {response.status_code}")
