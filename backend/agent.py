import logging
from typing import Callable, Any
from langchain_core.language_models import BaseChatModel
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import json
import ast

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_output_summarizer(summary_llm: BaseChatModel) -> Callable[[str, str], dict]:
    """
    创建输出摘要器

    Args:
        summary_llm: 用于生成摘要的语言模型

    Returns:
        摘要函数
    """
    def summarize_output(tool_output: str, user_message: str = "") -> dict:
        """
        对工具输出进行摘要处理

        Args:
            tool_output: 工具原始输出
            user_message: 用户消息（用于上下文）

        Returns:
            包含摘要、URL 和 favicon 的字典
        """
        if not tool_output or tool_output.strip() == "":
            return {"summary": tool_output, "urls": []}

        # 尝试解析 JSON 格式的工具输出
        try:
            parsed_output = json.loads(tool_output)
        except (json.JSONDecodeError, TypeError):
            try:
                parsed_output = ast.literal_eval(tool_output)
            except (ValueError, SyntaxError):
                return {"summary": tool_output, "urls": []}

        # 提取 URL、favicon 和内容
        urls = []
        favicons = []
        content = ""

        if isinstance(parsed_output, dict) and 'results' in parsed_output:
            items = parsed_output['results']
        elif isinstance(parsed_output, list):
            items = parsed_output
        else:
            return {"summary": tool_output, "urls": [], "favicons": []}

        # 从结果中提取信息
        for item in items:
            if isinstance(item, dict):
                if 'url' in item:
                    urls.append(item['url'])
                if 'favicon' in item:
                    favicons.append(item['favicon'])
                if 'raw_content' in item:
                    content += item['raw_content'] + "\n\n"

        # 生成摘要
        if content:
            summary_prompt = f"""请将以下内容总结为相关格式，以帮助回答用户的问题。
            重点关注对回答以下问题最有用的关键信息：{user_message}
            删除冗余信息并突出最重要的发现。

            内容：
            {content[:3000]}  # 限制内容长度

            请提供一个清晰、有组织的摘要，捕捉与用户问题相关的基本信息：
            """
            try:
                summary = summary_llm.invoke(summary_prompt).content
            except Exception as e:
                logger.error(f"摘要生成失败: {e}")
                summary = content[:500]  # 回退到截断内容
        else:
            summary = tool_output

        return {"summary": summary, "urls": urls, "favicons": favicons}

    return summarize_output


class WebAgent:
    """
    Web 智能体类，集成 Tavily 搜索、提取和爬取功能
    """

    def __init__(self, checkpointer: MemorySaver = None):
        """
        初始化 Web 智能体

        Args:
            checkpointer: LangGraph 检查点存储器（用于对话记忆）
        """
        self.checkpointer = checkpointer

    def build_graph(
        self,
        api_key: str,
        llm: BaseChatModel,
        prompt: str,
        summary_llm: BaseChatModel,
        user_message: str = ""
    ):
        """
        构建并编译 LangGraph 工作流

        Args:
            api_key: Tavily API 密钥
            llm: 主要语言模型（用于智能体推理）
            prompt: 系统提示词
            summary_llm: 用于摘要的语言模型
            user_message: 用户原始消息（用于摘要上下文）

        Returns:
            编译后的 LangGraph 智能体
        """
        if not api_key:
            raise ValueError("错误：未提供 Tavily API 密钥")

        # 创建 Tavily 工具
        search = TavilySearch(
            max_results=10,
            tavily_api_key=api_key,
            include_favicon=True,
            search_depth="advanced",
            include_answer=False,
        )

        extract = TavilyExtract(
            extract_depth="advanced",
            tavily_api_key=api_key,
            include_favicon=True,
        )

        crawl = TavilyCrawl(
            tavily_api_key=api_key,
            include_favicon=True,
            limit=15
        )

        # 创建输出摘要器
        output_summarizer = create_output_summarizer(summary_llm)

        # 为 Extract 工具添加摘要功能
        class SummarizingTavilyExtract(TavilyExtract):
            def _run(self, *args, **kwargs):
                kwargs.pop('run_manager', None)
                result = super()._run(*args, **kwargs)
                return output_summarizer(str(result), user_message)

            async def _arun(self, *args, **kwargs):
                kwargs.pop('run_manager', None)
                result = await super()._arun(*args, **kwargs)
                return output_summarizer(str(result), user_message)

        # 为 Crawl 工具添加摘要功能
        class SummarizingTavilyCrawl(TavilyCrawl):
            def _run(self, *args, **kwargs):
                kwargs.pop('run_manager', None)
                result = super()._run(*args, **kwargs)
                return output_summarizer(str(result), user_message)

            async def _arun(self, *args, **kwargs):
                kwargs.pop('run_manager', None)
                result = await super()._arun(*args, **kwargs)
                return output_summarizer(str(result), user_message)

        # 创建带摘要的工具实例
        extract_with_summary = SummarizingTavilyExtract(
            extract_depth=extract.extract_depth,
            tavily_api_key=api_key,
            include_favicon=extract.include_favicon,
            description=extract.description
        )

        crawl_with_summary = SummarizingTavilyCrawl(
            tavily_api_key=api_key,
            include_favicon=crawl.include_favicon,
            limit=crawl.limit,
            description=crawl.description
        )

        # 创建 ReAct 智能体
        return create_react_agent(
            prompt=prompt,
            model=llm,
            tools=[search, extract_with_summary, crawl_with_summary],
            checkpointer=self.checkpointer,
        )
