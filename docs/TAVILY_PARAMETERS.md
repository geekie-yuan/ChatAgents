# Tavily 参数配置说明

## 概述

本文档详细说明了智能体在 **快速模式（Fast）** 和 **深度思考模式（Deep）** 下的 Tavily 工具参数配置。

配置基于 [Tavily 官方文档](https://docs.tavily.com/documentation/integrations/langchain) 的最佳实践建议。

---

## 参数配置对比表

| 参数 | 快速模式（Fast） | 深度思考模式（Deep） | 说明 |
|------|-----------------|---------------------|------|
| **search_depth** | `basic` | `advanced` | 搜索深度，影响结果的全面性和成本 |
| **max_results** | `3` | `5` | 返回的搜索结果数量 |
| **include_images** | `False` | `True` | 是否包含图片 URL |
| **crawl_limit** | `5` | `15` | 爬取页面数量限制 |
| **extract_depth** | `basic` | `advanced` | 内容提取深度 |
| **topic** | `general` | `general` | 搜索主题（可选：general/news/finance） |
| **time_range** | `None` | `None` | 时间范围过滤（可选：day/week/month/year） |

---

## 详细说明

### 1. TavilySearch 配置

#### 快速模式（Fast）
```python
search = TavilySearch(
    max_results=3,              
    tavily_api_key=api_key,
    include_favicon=True,       
    search_depth="basic",       
    include_answer=False,       # 禁用直接答案，让 LLM 自己推理
    topic="general",           
    include_images=False,       
    time_range=None            
)
```


#### 深度思考模式（Deep）
```python
search = TavilySearch(
    max_results=5,              
    tavily_api_key=api_key,
    include_favicon=True,
    search_depth="advanced",    
    include_answer=False,
    topic="general",
    include_images=True,        
    time_range=None             
)
```


---

### 2. TavilyExtract 配置

#### 快速模式（Fast）
```python
extract = TavilyExtract(
    extract_depth="basic",      # 基础提取
    tavily_api_key=api_key,
    include_favicon=True,
    include_images=False,       # 不包含图片
)
```

#### 深度思考模式（Deep）
```python
extract = TavilyExtract(
    extract_depth="advanced",   # 高级提取，更详细
    tavily_api_key=api_key,
    include_favicon=True,
    include_images=True,        # 包含图片
)
```

**设计理由：**
- `extract_depth` 与 `search_depth` 保持一致
- `include_images` 与搜索配置保持一致

---

### 3. TavilyCrawl 配置

#### 快速模式（Fast）
```python
crawl = TavilyCrawl(
    tavily_api_key=api_key,
    include_favicon=True,
    limit=5                     
)
```

**设计理由：**
- `limit=5`：大幅减少爬取页面，显著提升速度
- 快速模式下，5 个页面通常足够回答简单问题

#### 深度思考模式（Deep）
```python
crawl = TavilyCrawl(
    tavily_api_key=api_key,
    include_favicon=True,
    limit=15                    
)
```

**设计理由：**
- `limit=15`：提供充足的爬取深度，支持复杂研究任务

---

## 高级参数说明

### topic（搜索主题）

**可选值：**
- `"general"`: 通用搜索（默认）
- `"news"`: 新闻搜索，优先返回新闻源
- `"finance"`: 财经搜索，专注财经信息

**使用场景：**
```python
# 新闻查询
agent.build_graph(..., topic="news")

# 财经查询
agent.build_graph(..., topic="finance")
```

### time_range（时间范围）

**可选值：**
- `"day"`: 最近一天
- `"week"`: 最近一周
- `"month"`: 最近一个月
- `"year"`: 最近一年
- `None`: 不限制（默认）

**使用场景：**
```python
# 查询最新新闻
agent.build_graph(..., topic="news", time_range="day")

# 查询本周财经动态
agent.build_graph(..., topic="finance", time_range="week")
```

---

## 成本与性能分析

### 快速模式（Fast）

**估算成本：**
- Search: 3 results × basic depth = ~6-9 credits
- Extract: basic depth = ~3-5 credits per call
- Crawl: 5 pages = ~5-10 credits
- **总计**: ~15-25 credits per query

**性能特点：**
- ✅ 响应速度快（1-3 秒）
- ✅ 成本低
- ⚠️ 结果深度有限
- ⚠️ 不包含视觉内容

**适用场景：**
- 简单事实查询
- 快速信息查找
- 高频率使用
- 成本敏感场景

---

### 深度思考模式（Deep）

**估算成本：**
- Search: 5 results × advanced depth = ~20-30 credits
- Extract: advanced depth = ~10-15 credits per call
- Crawl: 15 pages = ~15-30 credits
- **总计**: ~50-80 credits per query

**性能特点：**
- ✅ 结果全面深入
- ✅ 包含视觉内容
- ✅ 支持复杂分析
- ⚠️ 响应时间较长（3-8 秒）
- ⚠️ 成本较高

**适用场景：**
- 复杂研究任务
- 深度分析需求
- 需要视觉内容
- 质量优先场景

---

## 参数调优建议

### 1. 针对新闻查询优化
```python
agent.build_graph(
    mode="fast",
    topic="news",
    time_range="day"  # 只查最新新闻
)
```

### 2. 针对财经分析优化
```python
agent.build_graph(
    mode="deep",
    topic="finance",
    time_range="week"  # 本周财经动态
)
```

### 3. 针对研究类查询优化
```python
agent.build_graph(
    mode="deep",
    topic="general",
    time_range=None  # 不限制时间，获取最全面资料
)
```

### 4. 针对实时事件优化
```python
agent.build_graph(
    mode="fast",
    topic="news",
    time_range="day"  # 快速获取最新消息
)
```

---

## 未来优化方向

### 1. 动态参数调整
- 根据查询复杂度自动选择 mode
- 根据查询内容自动识别 topic
- 根据时间相关词汇自动设置 time_range

### 2. 领域过滤支持
```python
# 待实现
include_domains=["wikipedia.org", "github.com"]  # 只搜索指定域名
exclude_domains=["spam-site.com"]                # 排除指定域名
```

### 3. 成本控制
- 添加每次查询的成本上限
- 实现成本预估和警告机制

### 4. 缓存优化
- 对相同查询启用缓存
- 减少重复 API 调用

---

## 参考资料

1. [Tavily 官方文档](https://docs.tavily.com/documentation/integrations/langchain)
2. [LangChain Tavily 集成](https://python.langchain.com/docs/integrations/tools/tavily_search)
3. 项目内部文档：
   - `backend/agent.py` - 工具配置实现
   - `backend/prompts.py` - 提示词引导
   - `README.md` - 用户使用指南

---
