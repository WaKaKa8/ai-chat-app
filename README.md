# 📈 金融研报智能分析引擎 (AI FinTech Agent)

基于 Python 开发的大模型应用落地实践项目。本项目从最基础的 API 调用脚本出发，逐步演进为包含 RESTful 后端接口与 Web 图形化界面的完整前后端分离 AI 应用。项目深度结合了**金融业务场景**，并通过高级**提示词工程（Prompt Engineering）**将大模型改造为严谨、结构化、防幻觉的金融风控专家。

## 🛠 技术栈

- **开发语言**: Python 3
- **大模型接口**: 智谱 GLM-4-Flash API
- **后端框架**: FastAPI + Uvicorn (实现 RESTful API 规范)
- **数据校验**: Pydantic
- **前端界面**: Gradio
- **网络请求**: Requests
- **提示词工程**: Few-Shot Prompting, Chain-of-Thought (CoT), 结构化 JSON 输出
- **安全实践**: 基于环境变量 (`os.getenv`) 隔离 API Key，防止密钥泄露。

## 🌟 核心特性 (Prompt Engineering 实战)

本项目在 `main.py` 中通过高级 Prompt 技巧对大模型进行了深度约束，以适配金融行业对数据准确性的极高要求：
1. **角色设定**：赋予模型“严谨的金融风控专家”人设。
2. **Few-Shot Prompting**：提供经典的正负面金融案例，强制对齐大模型的“利好/利空”业务标签。
3. **Chain-of-Thought (CoT)**：要求模型严格按照“提取数据 -> 分析逻辑 -> 评估风险 -> 综合评级”四步法进行推演，降低模型幻觉。
4. **JSON 强约束**：强制模型输出纯 JSON 格式，方便后端代码直接进行数据解析与入库。
5. **安全兜底 (Fallback)**：加入了防闲聊、防恶意注入规则。若输入非金融文本，模型会自动拒绝并返回错误提示。

## 📂 项目结构

本项目包含三个核心文件，展示了应用架构的演进过程：

1. **`zhipu_chat_demo.py` (基础脚本)**
   - 纯命令行版本的 API 调用。演示了 HTTP POST 请求的构造、大模型 JSON 响应的解析，以及通过 System Prompt 为 AI 设定角色。

2. **`main.py` (后端 API)**
   - **核心功能**：基于 FastAPI 构建的 RESTful API 后端。
   - **实现细节**：定义了 `/chat` 的 POST 路由接口，使用 Pydantic 定义请求体进行数据校验。内部集成了复杂的金融分析 Prompt，接收前端请求后转发给大模型，并将结构化 JSON 返回给前端。

3. **`frontend.py` (前端界面)**
   - **核心功能**：基于 Gradio 构建的交互式 Web 聊天界面。
   - **实现细节**：将用户的输入通过 `requests.post` 发送给本地运行的 FastAPI 后端，并实时渲染 AI 的回复。

## 🚀 本地运行指南

### 1. 安装依赖
打开终端，运行以下命令：
pip install fastapi uvicorn requests gradio pydantic

### 2. 配置环境变量
在运行代码前，请确保已在操作系统中配置了智谱的 API Key 环境变量：

**Windows (PowerShell):**
setx ZHIPU_API_KEY "你的API_KEY"

**Mac / Linux:**
export ZHIPU_API_KEY="你的API_KEY"

---

### 3. 运行方式一：基础命令行脚本
如果你想测试最底层的 API 交互，可以直接运行基础脚本：
python zhipu_chat_demo.py
*(终端将直接打印出大模型的结构化分析回复)*

---

### 4. 运行方式二：前后端分离完整应用

**步骤 A：启动后端 (终端 1)**
uvicorn main:app --reload
*(后端服务将运行在 http://127.0.0.1:8000，可通过访问 http://127.0.0.1:8000/docs 查看自动生成的 Swagger 接口文档)*

**步骤 B：启动前端 (终端 2)**
python frontend.py
*(前端网页将运行在 http://127.0.0.1:7860，在浏览器打开即可输入财经新闻进行智能分析)*

## 💡 后续迭代计划
- [ ] 引入大模型多轮对话记忆 (History 传递)，实现连续追问分析
- [ ] 接入 SQLite 数据库，持久化存储历史分析记录
- [ ] 结合 RAG (检索增强生成) 技术，实现基于长篇招股书/研报 PDF 的问答助手