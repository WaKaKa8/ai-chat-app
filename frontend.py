import gradio as gr
import requests

# 这个函数就是网页上“发送”按钮点下后执行的动作
def chat_with_backend(message, history):
    url = "http://127.0.0.1:8000/chat"
    payload = {"prompt": message}
    
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        
        if result.get("status") == "success":
            return result["reply"]
        else:
            return f"后端出错了：{result.get('message')}"
            
    except Exception as e:
        return f"连接后端失败，请检查你的 FastAPI 服务是否启动了！错误：{e}"

# 画网页
demo = gr.ChatInterface(
    fn=chat_with_backend,
    title="金融研报智能分析引擎",
    description="基于大模型的财报提取与情感分析系统"
)

# 启动网页
if __name__ == "__main__":
    demo.launch()