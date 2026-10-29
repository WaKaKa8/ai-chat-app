import os
import json
import requests

api_key = os.getenv("ZHIPU_API_KEY")
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# 1. 定义我们的“工具清单”（告诉大模型你会什么）
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "查询指定公司的最新股价",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "公司名称，例如：智谱科技、腾讯",
                    }
                },
                "required": ["company_name"]
            }
        }
    }
]

def chat_with_tools(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    data = {
        "model": "glm-4-flash",
        "messages": messages,
        "tools": tools  # <--- 关键：把工具清单发给大模型
    }
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    message = result["choices"][0]["message"]
    
    # 2. 检查大模型是不是想用工具
    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        func_name = tool_call["function"]["name"]
        args = json.loads(tool_call["function"]["arguments"])
        
        print(f"🤖 AI 决定调用工具: {func_name}，参数: {args}")
        
        # 3. 这里就是“你的代码”真正干活的地方！
        # 假设我们真的去数据库查了（这里用假数据模拟）
        if func_name == "get_stock_price":
            company = args.get("company_name")
            # 模拟查数据库的结果
            mock_price = "150.5 元"
            print(f"⚙️ 正在查询 {company} 的股价，查到结果为：{mock_price}")
            print(f"⚙️ 大模型第一次思考后的回答为：{message}")
            # 4. 把查到的结果，塞回给大模型，让它总结成人话
            messages.append(message) # 把AI要调工具的那句话加进去
            messages.append({
                "role": "tool",
                "content": f"{company}的当前股价是{mock_price}",
                "tool_call_id": tool_call["id"]
            })
            
            # 再次请求大模型
            data["messages"] = messages
            final_response = requests.post(url, headers=headers, json=data)
            final_answer = final_response.json()["choices"][0]["message"]["content"]
            print(f"⚙️ 再次请求大模型后，查到结果为：") 
            return final_answer
    else:
        return message["content"]

# 测试运行
print(chat_with_tools("智谱科技今天股价多少？"))
print("-------")
print(chat_with_tools("今天天气真好，给我讲个笑话吧。"))