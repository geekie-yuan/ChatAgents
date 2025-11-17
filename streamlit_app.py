"""
Streamlit 智能聊天机器人前端
集成 Tavily Web Agent 功能，支持深度思考模式
"""

import streamlit as st
import requests
import json
import datetime
import time
import uuid
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="Yuan's Chat Agents",
    page_icon="./favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 配置常量 ====================
BACKEND_URL = "http://localhost:8080"
MIN_TIME_BETWEEN_REQUESTS = datetime.timedelta(seconds=1)
HISTORY_LENGTH = 10  # 保留最近10条消息用于上下文

# ==================== 样式配置 ====================
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    .tool-card {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        background-color: #f0f2f6;
    }
    .tool-search {
        border-left: 3px solid #4CAF50;
    }
    .tool-extract {
        border-left: 3px solid #2196F3;
    }
    .tool-crawl {
        border-left: 3px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 工具函数 ====================

def initialize_session():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_request_time" not in st.session_state:
        st.session_state.last_request_time = None

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "tool_calls" not in st.session_state:
        st.session_state.tool_calls = []

    # API 密钥 - 从环境变量加载默认值
    if "claude_api_key" not in st.session_state:
        st.session_state.claude_api_key = os.getenv("ANTHROPIC_API_KEY", "")

    if "tavily_api_key" not in st.session_state:
        st.session_state.tavily_api_key = os.getenv("TAVILY_API_KEY", "")

    # 智能体配置
    if "agent_type" not in st.session_state:
        st.session_state.agent_type = "fast"

    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = "claude"

    if "llm_model" not in st.session_state:
        st.session_state.llm_model = "sonnet"


def format_time(timestamp: datetime.datetime) -> str:
    """格式化时间戳"""
    return timestamp.strftime("%H:%M:%S")


def check_backend_health() -> bool:
    """检查后端服务健康状态"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False


def stream_agent_response(user_input: str, config: Dict) -> tuple:
    """
    调用后端智能体并流式接收响应

    Args:
        user_input: 用户输入
        config: 配置字典（API 密钥、智能体类型等）

    Returns:
        (完整响应文本, 工具调用列表)
    """
    # 准备请求头
    headers = {
        "Content-Type": "application/json",
    }

    # 添加 API 密钥到请求头
    if config.get("tavily_api_key"):
        headers["X-Tavily-Key"] = config["tavily_api_key"]
    if config.get("claude_api_key"):
        headers["X-Claude-Key"] = config["claude_api_key"]

    # 准备请求体
    payload = {
        "input": user_input,
        "thread_id": config.get("thread_id", str(uuid.uuid4())),
        "agent_type": config.get("agent_type", "fast"),
        "llm_provider": config.get("llm_provider", "claude"),
        "llm_model": config.get("llm_model", "sonnet"),
    }

    # 发送流式请求
    try:
        response = requests.post(
            f"{BACKEND_URL}/stream_agent",
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        response.raise_for_status()

        full_response = ""
        tool_calls = []

        # 处理流式响应
        for line in response.iter_lines():
            if line:
                try:
                    event = json.loads(line.decode('utf-8'))

                    if event["type"] == "chatbot":
                        # 聊天机器人响应
                        full_response += event["content"]
                        yield event["content"], None

                    elif event["type"] == "tool_start":
                        # 工具开始调用
                        tool_calls.append({
                            "type": "start",
                            "tool_name": event["tool_name"],
                            "tool_type": event["tool_type"],
                            "operation_index": event["operation_index"],
                            "content": event["content"]
                        })
                        yield None, tool_calls[-1]

                    elif event["type"] == "tool_end":
                        # 工具调用结束
                        tool_calls.append({
                            "type": "end",
                            "tool_name": event["tool_name"],
                            "tool_type": event["tool_type"],
                            "operation_index": event["operation_index"],
                            "content": event["content"]
                        })
                        yield None, tool_calls[-1]

                    elif event["type"] == "error":
                        # 错误事件
                        st.error(f"❌ {event['content']}")
                        return

                except json.JSONDecodeError:
                    continue

        return full_response, tool_calls

    except requests.exceptions.RequestException as e:
        st.error(f"❌ 请求失败: {str(e)}")
        return None, []


def render_tool_call(tool_event: Dict):
    """渲染工具调用卡片"""
    tool_type = tool_event.get("tool_type", "search")
    tool_name = tool_event.get("tool_name", "未知工具")

    # 工具图标和颜色
    tool_icons = {
        "search": "🔍",
        "extract": "📄",
        "crawl": "🕷️"
    }

    tool_colors = {
        "search": "#4CAF50",
        "extract": "#2196F3",
        "crawl": "#FF9800"
    }

    icon = tool_icons.get(tool_type, "🔧")
    color = tool_colors.get(tool_type, "#757575")

    if tool_event["type"] == "start":
        with st.status(f"{icon} 正在使用 {tool_name}...", expanded=False):
            st.write(f"**输入**: {tool_event.get('content', 'N/A')}")
    elif tool_event["type"] == "end":
        with st.expander(f"{icon} {tool_name} 完成", expanded=False):
            content = tool_event.get('content', {})
            if isinstance(content, dict):
                if 'summary' in content:
                    st.write("**摘要**:")
                    st.write(content['summary'][:500] + "..." if len(content.get('summary', '')) > 500 else content.get('summary', ''))
                if 'urls' in content and content['urls']:
                    st.write("**来源链接**:")
                    for url in content['urls'][:5]:  # 最多显示5个链接
                        st.write(f"- {url}")
            else:
                st.write(str(content)[:500] + "..." if len(str(content)) > 500 else str(content))


# ==================== 侧边栏配置 ====================

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("⚙️ 配置")

        # ===== API 密钥管理 =====
        with st.expander("🔑 API 密钥", expanded=True):
            # Claude API 密钥
            claude_key = st.text_input(
                "Claude API 密钥",
                type="password",
                value=st.session_state.claude_api_key,
                help="输入您的 Anthropic API 密钥（sk-ant-api...）"
            )
            if claude_key != st.session_state.claude_api_key:
                st.session_state.claude_api_key = claude_key

            # Tavily API 密钥
            tavily_key = st.text_input(
                "Tavily API 密钥",
                type="password",
                value=st.session_state.tavily_api_key,
                help="输入您的 Tavily API 密钥（用于 Web 搜索）"
            )
            if tavily_key != st.session_state.tavily_api_key:
                st.session_state.tavily_api_key = tavily_key

            # 密钥状态指示
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.claude_api_key:
                    st.success("✅ Claude")
                else:
                    st.error("❌ Claude")
            with col2:
                if st.session_state.tavily_api_key:
                    st.success("✅ Tavily")
                else:
                    st.error("❌ Tavily")

        # ===== 智能体配置 =====
        with st.expander("🤖 智能体设置", expanded=True):
            # 智能体模式
            agent_type = st.radio(
                "智能体模式",
                options=["fast", "deep"],
                format_func=lambda x: "⚡ 快速模式" if x == "fast" else "🧠 深度思考模式",
                index=0 if st.session_state.agent_type == "fast" else 1,
                help="快速模式：快速响应，适合简单问题\n深度思考模式：深度研究，适合复杂查询"
            )
            if agent_type != st.session_state.agent_type:
                st.session_state.agent_type = agent_type

            # LLM 提供商（当前仅支持 Claude）
            st.session_state.llm_provider = "claude"
            st.info("当前仅支持 Claude，未来将添加更多模型")

            # Claude 模型选择
            model_options = {
                "haiku": "Haiku（快速且经济）",
                "sonnet": "Sonnet（平衡性能）",
                "opus": "Opus（最强性能）"
            }

            selected_model = st.selectbox(
                "Claude 模型",
                options=list(model_options.keys()),
                format_func=lambda x: model_options[x],
                index=list(model_options.keys()).index(st.session_state.llm_model),
                help="选择 Claude 模型版本"
            )
            if selected_model != st.session_state.llm_model:
                st.session_state.llm_model = selected_model

        # ===== 后端状态 =====
        st.divider()
        st.subheader("📊 系统状态")

        backend_healthy = check_backend_health()
        if backend_healthy:
            st.success("✅ 后端服务正常")
        else:
            st.error("❌ 后端服务未运行")
            st.info("请确保后端服务已启动：\n```bash\npython app.py\n```")

        # ===== 会话管理 =====
        st.divider()
        st.subheader("💬 会话管理")
        st.caption(f"会话 ID: {st.session_state.thread_id[:8]}...")

        if st.button("🔄 新建会话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.session_state.tool_calls = []
            st.rerun()

        # ===== 关于 =====
        st.divider()
        with st.expander("ℹ️ 关于"):
            st.markdown("""
            **Yuan's Chat Agents**

            一个集成了 Web 搜索、内容提取和深度思考能力的智能助手。

            **功能特点**:
            - 🔍 实时 Web 搜索
            - 📄 网页内容提取
            - 🕷️ 网站深度爬取
            - 🧠 深度思考推理
            - 💬 对话记忆

            **技术栈**:
            - Streamlit (前端)
            - FastAPI (后端)
            - LangGraph (智能体框架)
            - Tavily (Web 工具)
            - Claude (语言模型)

            **作者**: Yuan
            **博客**: [blog.geekie.site](https://blog.geekie.site)
            """)


# ==================== 主应用 ====================

def main():
    """主应用程序"""
    initialize_session()

    # 标题
    st.title("🤖 Yuan's Chat Agents")
    st.caption("集成 Web 搜索与深度思考能力的智能助手")

    # 渲染侧边栏
    render_sidebar()

    # 检查后端服务
    if not check_backend_health():
        st.error("❌ 后端服务未运行，请先启动后端服务")
        st.code("python app.py", language="bash")
        st.stop()

    # 显示历史消息
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg.get("timestamp")

        with st.chat_message(role):
            if timestamp:
                st.caption(f"🕒 {format_time(timestamp)}")
            st.markdown(content)

            # 显示工具调用（如果有）
            if role == "assistant" and "tool_calls" in msg and msg["tool_calls"]:
                with st.expander(f"🔧 查看工具调用 ({len([t for t in msg['tool_calls'] if t['type'] == 'end'])} 次)", expanded=False):
                    for tool_call in msg["tool_calls"]:
                        if tool_call["type"] == "end":
                            render_tool_call(tool_call)

    # 聊天输入
    if prompt := st.chat_input("输入您的问题..."):
        # 检查请求频率限制
        current_time = datetime.datetime.now()
        if (st.session_state.last_request_time and
                current_time - st.session_state.last_request_time < MIN_TIME_BETWEEN_REQUESTS):

            remaining = MIN_TIME_BETWEEN_REQUESTS - (current_time - st.session_state.last_request_time)
            st.warning(f"请等待 {remaining.total_seconds():.1f} 秒后再发送消息")
            st.stop()

        # 添加用户消息
        user_msg = {
            "role": "user",
            "content": prompt,
            "timestamp": current_time
        }
        st.session_state.messages.append(user_msg)

        # 显示用户消息
        with st.chat_message("user"):
            st.caption(f"🕒 {format_time(current_time)}")
            st.markdown(prompt)

        # 生成助手回复
        with st.chat_message("assistant"):
            timestamp_placeholder = st.empty()
            message_placeholder = st.empty()
            tool_container = st.container()

            timestamp_placeholder.caption(f"🕒 {format_time(datetime.datetime.now())}")

            try:
                # 准备配置
                config = {
                    "tavily_api_key": st.session_state.tavily_api_key,
                    "claude_api_key": st.session_state.claude_api_key,
                    "thread_id": st.session_state.thread_id,
                    "agent_type": st.session_state.agent_type,
                    "llm_provider": st.session_state.llm_provider,
                    "llm_model": st.session_state.llm_model,
                }

                # 流式接收响应
                full_response = ""
                tool_calls = []

                with st.spinner("🤔 正在板砖..."):
                    for content, tool_event in stream_agent_response(prompt, config):
                        if content:
                            # 更新响应文本
                            full_response += content
                            message_placeholder.markdown(full_response + "▌")

                        if tool_event:
                            # 记录工具调用
                            tool_calls.append(tool_event)

                            # 实时显示工具调用
                            with tool_container:
                                render_tool_call(tool_event)

                # 显示最终响应
                message_placeholder.markdown(full_response)

                # 保存助手消息
                assistant_msg = {
                    "role": "assistant",
                    "content": full_response,
                    "timestamp": datetime.datetime.now(),
                    "tool_calls": tool_calls
                }
                st.session_state.messages.append(assistant_msg)

                # 更新请求时间
                st.session_state.last_request_time = current_time

            except Exception as e:
                error_msg = f"抱歉，发生了错误: {str(e)}"
                message_placeholder.error(error_msg)

                # 保存错误消息
                error_msg_obj = {
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.datetime.now()
                }
                st.session_state.messages.append(error_msg_obj)


if __name__ == "__main__":
    main()
