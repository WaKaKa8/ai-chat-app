import os  # 用来读取系统环境变量
from fastapi import FastAPI
import requests
from pydantic import BaseModel
import sqlite3

# 启动 FastAPI 服务
app = FastAPI(title="我的第一个AI后端接口")
# 连接数据库（如果没有这个文件，会自动创建 finance.db）
conn = sqlite3.connect('finance.db', check_same_thread=False)
cursor = conn.cursor()
# 创建一张表，用来存聊天记录
cursor.execute('CREATE TABLE IF NOT EXISTS history (user TEXT, ai TEXT)')
conn.commit()

# 你的通行证
api_key = os.getenv("ZHIPU_API_KEY")
if not api_key:
    print("警告：没有找到环境变量 ZHIPU_API_KEY，请检查配置！")

# 定义前端传过来的数据格式（告诉后端：你要给我发一个叫 prompt 的字符串）
class ChatRequest(BaseModel):
    prompt: str

# 4. 路由定义：当别人用 POST 方法访问 /chat 这个地址时，执行这个函数
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    #【查记忆】：从数据库里把最近的 3 条聊天记录拿出来
    cursor.execute("SELECT user, ai FROM history ORDER BY rowid DESC LIMIT 3")
    rows = cursor.fetchall()
    rows.reverse() # 倒序变正序
    # 组装给大模型的数据
    messages = [
        {
            "role": "system",
            "content": '''你是一个严谨的金融风控专家。请分析用户输入的新闻。
                【重要规则】：
                    如果用户当前的提问信息不全（比如只说“情况如何”没给具体数字），你必须去【历史聊天记录】中寻找相关的数据补充进来分析！
                为了确保准确性，你必须按照以下【思维链（CoT）】步骤进行思考：
                    第一步：提取新闻中的正负面核心数据（营收、利润等）。
                    第二步：分析数据之间的逻辑矛盾（例如为何营收涨利润跌）。
                    第三步：评估重大风险点（如违规、调查）。
                    第四步：综合以上逻辑，给出评级（利好/利空/中性）。

               【Few-Shot 示例】：
                    输入：公司宣布回购10%的股份，耗资5亿元。
                    输出：{"公司":"未知", "提取数据":"回购10%股份", "逻辑分析":"公司现金流充裕，管理层认为股价低估", "风险点":"无", "评级":"利好", "理由":"回购彰显信心"}

                    输入：公司董事长因涉嫌内幕交易被拘留。
                    输出：{"公司":"未知", "提取数据":"董事长被拘留", "逻辑分析":"核心管理层动荡", "风险点":"涉嫌违法", "评级":"利空", "理由":"严重影响公司声誉和经营"}

               【严格输出要求】：
                    请严格输出纯 JSON 格式，不要包含任何 Markdown 标记（如 ```json）。输出字段必须为：{"公司": "xxx", "提取数据": "xxx", "逻辑分析": "xxx", "风险点": "xxx", "评级": "xxx", "理由": "xxx"}
                '''
            }
    ]    
    # 把历史记忆塞进去
    for u, a in rows:
        messages.append({"role": "user", "content": u})
        messages.append({"role": "assistant", "content": a})       
    # 把当前用户的问题塞进去
    messages.append({"role": "user", "content": request.prompt})
    print("--- 发给大模型的数据 ---")
    print(messages)

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "glm-4-flash",
        "messages": messages
    }
    
    # 发送请求
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # 提取回答
    if "choices" in result:
        ai_reply = result["choices"][0]["message"]["content"]
        #【存记忆】：解析成功后，写进数据库
        cursor.execute("INSERT INTO history (user, ai) VALUES (?, ?)", (request.prompt, ai_reply))
        conn.commit() # 必须提交！
        # 把结果返回给前端（这是一个 JSON 格式）
        return {"status": "success", "reply": ai_reply}
    else:
        return {"status": "error", "message": "大模型没理我", "detail": result}