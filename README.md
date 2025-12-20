# 🤖 Yuan's  ChatAgents
<div align="center">

**一个集成了 Web 搜索、内容提取和深度思考能力的智能体助手**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

[English](./README_EN.md) | **简体中文**

</div>

---

## 📖 项目简介

这是一个能够联网搜索的智能聊天机器人：

1. **简单聊天机器人**（基于 Streamlit + LLM）
2. **Tavily Web 智能体**（基于 LangGraph + Tavily）

通过混合架构 Streamlit + LangGraph + Tavily，为LLM提供了强大的 Web 搜索、内容提取和深度思考的能力。

## ✨ 功能特性

### 🎯 核心功能
- **💬 交互式聊天界面**：基于Streamlit，构建简洁快捷的UI
- **🔍 实时 Web 搜索**：通过 Tavily 联网搜索最新信息
- **🕷️ 网站深度爬取**：深度爬取网站嵌套链接
- **📄 网页内容提取**：提取网页关键内容, 节省Token消耗
- **🧠 深度思考模式**：支持复杂查询的深度推理
- **⚡ 快速响应模式**：适合简单问题的快速回答
- **💭 对话记忆**：基于 LangGraph 的对话历史管理

### 🛠️ 高级特性
- **🔑 灵活的 API 密钥管理**：支持 Claude、Tavily 等多个 API
- **🎨 多模型支持**：支持 Claude (Haiku/Sonnet/Opus)、OpenAI(mini/nano/5.1)，预留 I/Groq 接口
- **📊 工具调用可视化**：实时展示Serch/Extract/Crawl过程
- **🎯 智能体类型切换**：快速模式 与 深度思考模式
- **💾 会话管理**：支持多会话，保留对话历史
- **🐳 Docker 支持**：一键容器化部署

## 🏗️ 架构设计

![Untitled-2025-12-21-0038](https://img.geekie.site/i/adImg/2025/12/21/022423.png)

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端** | Streamlit | 简洁的 Python Web 框架 |
| **后端** | FastAPI | 高性能异步 API 框架 |
| **智能体** | LangGraph | 智能体编排框架 |
| **LLM** | Claude OpenAI | 主要语言模型 |
| **工具** | Tavily | Web 搜索/提取/爬取 |
| **其他** | Docker, python-dotenv | 容器化与配置管理 |

## 🚀 快速开始

### 环境要求

- **Python**: 3.11+
- **API 密钥**:
  - [Anthropic Claude API](https://console.anthropic.com/)
  - [Tavily API](https://tavily.com/)

### 安装步骤

#### 1. 克隆仓库

```bash
git clone <your-repo-url>
cd intelligent-chatbot
```

#### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

```bash
# 复制示例配置文件
cp .env.sample .env

# 编辑 .env 文件，填入你的 API 密钥
# ANTHROPIC_API_KEY=sk-ant-api-your-key-here
# TAVILY_API_KEY=tvly-your-key-here
```

#### 5. 启动应用

**方法 A：分别启动（推荐开发）**

```bash
# 终端 1：启动后端
python app.py

# 终端 2：启动前端
streamlit run streamlit_app.py
```

**方法 B：使用 Docker Compose**

```bash
docker-compose up --build
```

#### 6. 访问应用

- **前端**: http://localhost:8501
- **后端 API**: http://localhost:8080
- **API 文档**: http://localhost:8080/docs

## 📖 使用指南

### 基本使用

1. **配置 API 密钥**
   - 在侧边栏输入 Claude 和 Tavily API 密钥
   - 或在 `.env` 文件中预先配置

2. **选择智能体模式**
   - **⚡ 快速模式**: 适合简单问题，快速响应
     - 使用 `basic` 搜索深度，速度快、成本低
     - 返回 3 条搜索结果（平衡配置）
     - 爬取限制：5 个页面
     - 不包含图片（减少响应体积）
     - TavilySearch 和 TavilyExtract 均使用基础级别
   - **🧠 深度思考模式**: 适合复杂查询，深度研究
     - 使用 `advanced` 搜索深度，结果更全面但成本更高
     - 返回 5 条搜索结果
     - 爬取限制：15 个页面
     - 包含图片（支持视觉内容）
     - TavilySearch 和 TavilyExtract 均使用高级级别
   - **🎯 高级参数支持**:
     - `topic`: 搜索主题分类（general/news/finance）
     - `time_range`: 时间范围过滤（day/week/month/year）

3. **选择 Claude 模型**
   - **Haiku**: 快速且经济
   - **Sonnet**: 平衡性能（推荐）
   - **Opus**: 最强性能

4. **开始对话**
   - 在输入框输入问题
   - 实时查看工具调用过程
   - 获取带引用的详细答案

### 高级功能

#### 工具调用展示

智能体会根据问题自动选择合适的工具：

- **🔍 TavilySearch**: 搜索相关网页
- **📄 TavilyExtract**: 提取网页内容
- **🕷️ TavilyCrawl**: 深度爬取网站

每个工具调用都会在 UI 中实时展示：
- 工具名称和类型
- 输入参数
- 输出摘要和来源链接

#### 会话管理

- 每个会话有唯一 ID
- 支持对话历史记忆
- 点击"新建会话"开始新对话

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 | ✅ | - |
| `TAVILY_API_KEY` | Tavily API 密钥 | ✅ | - |
| `OPENAI_API_KEY` | OpenAI API 密钥 | ✅ | - |
| `GROQ_API_KEY` | Groq API 密钥（未来） | ❌ | - |
| `PORT` | 后端端口 | ✅ | 8080 |

### 智能体配置

在 `streamlit_app.py` 中可自定义：

```python
# 请求频率限制
MIN_TIME_BETWEEN_REQUESTS = datetime.timedelta(seconds=1)

# 对话历史长度
HISTORY_LENGTH = 10

# 后端 URL
BACKEND_URL = "http://localhost:8080"
```

在 `backend/llm_config.py` 中可添加新的 LLM 模型。

## 📁 项目结构

```
intelligent-chatbot/
├── backend/                    # 后端模块
│   ├── __init__.py
│   ├── agent.py               # Web 智能体（LangGraph）
│   ├── llm_config.py          # LLM 配置管理
│   ├── prompts.py             # 提示词模板
│   ├── session_manager.py     # 会话管理器
│   └── utils.py               # 工具函数
├── data/                       # 数据目录
│   └── sessions/              # 会话数据存储
├── docs/                       # 文档目录
│   └── TAVILY_PARAMETERS.md   # Tavily 参数说明
├── .streamlit/                 # Streamlit 配置
├── app.py                      # FastAPI 后端服务器
├── streamlit_app.py            # Streamlit 前端应用
├── requirements.txt            # Python 依赖
├── .env                        # 环境变量（本地）
├── .env.sample                 # 环境变量示例
├── .gitignore                  # Git 忽略文件
├── Dockerfile                  # Docker 镜像
├── docker-compose.yml          # Docker Compose 配置
├── favicon.ico                 # 网站图标
├── PROJECT_SUMMARY.md          # 项目概述
├── QUICK_START.md              # 快速开始指南
├── README.md                   # 项目文档（中文）
└── README_EN.md                # 项目文档（英文）
```

## 🎯 功能演示

### 示例对话 1：简单问答（快速模式）

**用户**: 什么是人工智能？

**智能体**:
- 无需工具调用
- 直接基于基础知识回答
- 响应时间 < 3 秒

### 示例对话 2：实时搜索（快速模式）

**用户**: 当前最新的 AI 技术趋势是什么？

**智能体**:
1. 🔍 调用 TavilySearch（topic=news, time_range=month）
2. 📊 展示搜索结果
3. 💬 生成带引用的答案

### 示例对话 3：深度研究（深度思考模式）

**用户**: 分析一下 LangChain 和 LangGraph 的区别，并给出使用建议

**智能体**:
1. 🔍 搜索 LangChain 官方文档
2. 📄 提取关键页面内容
3. 🔍 搜索 LangGraph 文档
4. 📄 提取对比信息
5. 🧠 深度分析并生成详细报告

## 🐛 常见问题

### 1. 后端服务无法启动

**问题**: `ConnectionRefusedError` 或后端状态显示"未运行"

**解决方案**:
```bash
# 检查端口占用
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # macOS/Linux

# 确保后端已启动
python app.py
```

### 2. API 密钥错误

**问题**: `401 Unauthorized` 或 "API 密钥验证失败"

**解决方案**:
- 检查 API 密钥格式：
  - Claude: `sk-ant-api-...`
  - Tavily: `tvly-...`
- 确认密钥未过期且有足够配额
- 检查 `.env` 文件或侧边栏输入

### 3. 工具调用失败

**问题**: 工具调用超时或返回错误

**解决方案**:
- 检查网络连接
- 确认 Tavily API 配额充足
- 降低并发请求数量

### 4. 流式响应中断

**问题**: 响应中途停止或不完整

**解决方案**:
- 增加请求超时时间
- 检查后端日志（`app.py` 输出）
- 确认 LLM 配额充足

## 🔮 未来计划

- [ ] 支持更多 LLM 提供商（Groq, etc.）
- [ ] 添加文件上传和分析功能
- [ ] 实现对话导出（Markdown/PDF）
- [ ] 优化流式响应性能

## 🤝 贡献

欢迎贡献！请随时提交 Issue 或 Pull Request。

### 贡献流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。

## 👤 作者

**Yuan**

- 📝 博客: [https://blog.geekie.site](https://blog.geekie.site)
- 📧 邮箱: [yuan.sn@outlook.com](mailto:yuan.sn@outlook.com)
- 🔗 GitHub: [geekie-yuan](https://github.com/geekie-yuan)

## 🙏 致谢

本项目基于以下开源项目构建：

- [Streamlit](https://streamlit.io/) - 简洁的 Python Web 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 API 框架
- [LangChain](https://www.langchain.com/) - LLM 应用框架
- [LangGraph](https://langchain-ai.github.io/langgraph/) - 智能体编排框架
- [Anthropic Claude](https://www.anthropic.com/) - 强大的语言模型
- [Tavily](https://tavily.com/) - AI 优化的搜索 API



---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个星标！**

Made with ❤️ by Yuan

</div>
