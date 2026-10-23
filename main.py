import os  # 用来读取系统环境变量
from fastapi import FastAPI
import requests
from pydantic import BaseModel

# 1. 启动 FastAPI 服务
app = FastAPI(title="我的第一个AI后端接口")

# 2. 你的通行证
api_key = os.getenv("ZHIPU_API_KEY")

if not api_key:
    print("警告：没有找到环境变量 ZHIPU_API_KEY，请检查配置！")

# 3. 定义前端传过来的数据格式（告诉后端：你要给我发一个叫 prompt 的字符串）
class ChatRequest(BaseModel):
    prompt: str

# 4. 路由定义：当别人用 POST 方法访问 /chat 这个地址时，执行这个函数
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    # 组装发给大模型的数据
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": request.prompt}]
    }
    
    # 发送请求
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # 提取回答
    if "choices" in result:
        ai_reply = result["choices"][0]["message"]["content"]
        # 把结果返回给前端（这是一个 JSON 格式）
        return {"status": "success", "reply": ai_reply}
    else:
        return {"status": "error", "message": "大模型没理我", "detail": result}