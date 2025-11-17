# 🚀 快速开始指南

## 30 秒快速启动（Windows）

```bash
# 1. 运行安装脚本
setup.bat

# 2. 编辑 .env 文件，填入 API 密钥
notepad .env

# 3. 启动应用
start.bat

# 4. 打开浏览器
# http://localhost:8501
```

## 5 分钟完整设置

### 第 1 步：获取 API 密钥

1. **Claude API 密钥**
   - 访问: https://console.anthropic.com/
   - 创建 API 密钥
   - 格式: `sk-ant-api-...`

2. **Tavily API 密钥**
   - 访问: https://tavily.com/
   - 注册并获取密钥
   - 格式: `tvly-...`

### 第 2 步：安装项目

```bash
# 克隆或下载项目
cd intelligent-chatbot

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

### 第 3 步：配置 API 密钥

```bash
# 复制配置文件
cp .env.sample .env

# 编辑 .env 文件
notepad .env  # Windows
# nano .env    # macOS/Linux
```

在 `.env` 文件中填入：

```env
ANTHROPIC_API_KEY=sk-ant-api-your-key-here
TAVILY_API_KEY=tvly-your-key-here
```

### 第 4 步：启动应用

**终端 1（后端）：**
```bash
python app.py
```

**终端 2（前端）：**
```bash
streamlit run streamlit_app.py
```

### 第 5 步：开始使用

1. 打开浏览器：http://localhost:8501
2. 在侧边栏输入 API 密钥（或已在 .env 配置）
3. 选择智能体模式（快速/深度思考）
4. 选择 Claude 模型（Haiku/Sonnet/Opus）
5. 在输入框输入问题
6. 查看实时响应和工具调用

## Docker 快速启动

```bash
# 配置 .env 文件
cp .env.sample .env
# 编辑 .env 文件

# 启动容器
docker-compose up --build

# 访问应用
# http://localhost:8501
```

## 常见问题快速解决

### ❌ 后端服务未运行

```bash
# 确保在正确目录
cd intelligent-chatbot

# 激活虚拟环境
venv\Scripts\activate

# 启动后端
python app.py
```

### ❌ API 密钥错误

1. 检查密钥格式：
   - Claude: `sk-ant-api-...`
   - Tavily: `tvly-...`

2. 确认密钥有效且有配额

3. 在侧边栏重新输入密钥

### ❌ 依赖安装失败

```bash
# 更新 pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### ❌ 端口占用

```bash
# Windows
netstat -ano | findstr :8080
netstat -ano | findstr :8501

# macOS/Linux
lsof -i :8080
lsof -i :8501

# 修改端口（app.py 或 streamlit_app.py）
```

## 最小测试示例

### 测试后端健康

```bash
curl http://localhost:8080/health
# 应返回: {"status":"ok"}
```

### 测试简单对话

1. 打开前端：http://localhost:8501
2. 输入："你好"
3. 查看响应（无需工具调用）

### 测试 Web 搜索

1. 输入："当前 AI 最新进展"
2. 查看工具调用：TavilySearch
3. 查看来源链接

## 目录结构

```
intelligent-chatbot/
├── backend/              # 后端模块
│   ├── agent.py         # LangGraph 智能体
│   ├── llm_config.py    # LLM 配置
│   ├── prompts.py       # 提示词
│   └── utils.py         # 工具函数
├── app.py               # FastAPI 服务器
├── streamlit_app.py     # Streamlit 前端
├── requirements.txt     # 依赖
├── .env.sample          # 配置模板
├── setup.bat            # 安装脚本
└── start.bat            # 启动脚本
```

## 端口说明

| 服务 | 端口 | URL |
|------|------|-----|
| Streamlit 前端 | 8501 | http://localhost:8501 |
| FastAPI 后端 | 8080 | http://localhost:8080 |
| API 文档 | 8080 | http://localhost:8080/docs |

## 下一步

- 📖 阅读完整文档：`README.md`
- 🔧 查看配置选项：`backend/llm_config.py`
- 🐛 遇到问题：查看 `README.md` 的常见问题部分
- 💡 提交反馈：[[GitHub]](https://.com/geekie-yuan/Yuan-s-Chat-Agents.git)

---

**快速帮助**
- 博客: https://blog.geekie.site
- 作者: Yuan
