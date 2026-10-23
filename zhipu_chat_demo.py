import requests

# 1. 把你的 API Key 放这里（注意双引号不要漏掉，里面直接粘贴你复制的长串）
api_key = ""

# 2. 智谱的接口地址
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 3. 构造请求头（带上你的通行证）
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 4. 构造发给大模型的 JSON 数据
data = {
    "model": "glm-4-flash",  # glm-4-flash 是免费模型，适合测试
    "messages": [
        {"role": "system", "content": "你是一个脾气暴躁的客服，回答问题非常不耐烦。"},
        {"role": "user", "content": "请问我的快递什么时候到？"}
    ]
}

# 5. 发送 POST 请求
try:
    print("正在向大模型发送请求...")
    response = requests.post(url, headers=headers, json=data)
    
    # 6. 解析返回的 JSON
    result = response.json()
    
    # 提取 AI 的回答
    if "choices" in result:
        ai_reply = result["choices"][0]["message"]["content"]
        print("\n=== 大模型回复 ===")
        print(ai_reply)
        print("==================\n")
        print("🎉 恭喜！你成功跑通了第一个 AI 请求！")
    else:
        print("接口有响应，但没拿到正常回答，返回内容如下：")
        print(result)

except Exception as e:
    print(f"糟糕，出错了: {e}")