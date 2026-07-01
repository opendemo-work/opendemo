<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# RAG 文档分块策略

> 本案例详解 RAG 中的文档分块技术，涵盖固定窗口、语义分块、父子块等策略及其适用场景。

## 📐 分块策略概览

### 分块流程

```
Document → Preprocessing → Chunking → Embedding → Indexing
```

### 核心策略对比

| 策略 | 块大小 | 上下文保持 | 适用场景 |
|------|--------|------------|----------|
| 固定窗口 | 512 tokens | 低 | 通用场景 |
| 语义分块 | 可变 | 高 | 问答系统 |
| 父子块 | 可变 | 极高 | 复杂文档 |
| LLM 辅助 | 可变 | 最高 | 精确问答 |

## 💻 核心实现

### 固定窗口分块

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fixed_chunking(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)
```

### 语义分块

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

def semantic_chunking(documents, threshold=0.5):
    splitter = SemanticChunker(
        OpenAIEmbeddings(),
        breakpoint_threshold_threshold=threshold
    )
    return splitter.split_documents(documents)
```

### 父子块策略

```python
class ParentChunker:
    def __init__(self, parent_chunk_size=4000, child_chunk_size=500):
        self.parent_size = parent_chunk_size
        self.child_size = child_chunk_size
    
    def chunk_hierarchy(self, document):
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.parent_size
        )
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.child_size
        )
        
        parent_chunks = parent_splitter.split_documents([document])
        child_chunks = child_splitter.split_documents([document])
        
        return {
            "parents": parent_chunks,
            "children": child_chunks,
            "mapping": self._create_mapping(parent_chunks, child_chunks)
        }
    
    def _create_mapping(self, parents, children):
        mapping = {}
        for i, parent in enumerate(parents):
            for child in children:
                if child.page_content in parent.page_content:
                    mapping.setdefault(i, []).append(child)
        return mapping
```

## 📊 分块策略选择指南

```
┌─────────────────────────────────────────────────────┐
│                   分块策略选择流程                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  文档类型?                                           │
│      │                                              │
│      ├── 长文档/技术文档 → 父子块 / 语义分块            │
│      │                                              │
│      ├── 短文档/FAQ → 固定窗口 / 句子级                │
│      │                                              │
│      └── 表格/结构化数据 → 特殊处理                    │
│                                                     │
│  查询类型?                                           │
│      │                                              │
│      ├── 精确匹配 → 句子级 / 段落级                    │
│      │                                              │
│      └── 语义搜索 → 512-1024 tokens                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 📋 命令速查

```bash
pip install langchain langchain-experimental

# 运行分块对比
python chunking_strategies/compare.py

# 测试语义分块
python chunking_strategies/semantic.py
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `rag-retrieval-optimization` - 检索优化
- `hybrid-search` - 混合搜索

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的 AI/ML 核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
# 安装依赖
pip install -r requirements.txt

# 运行演示
python code/main.py
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的 AI/ML 核心概念。

### 2. 适用场景

- 场景 1：学术研究
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
python code/main.py
```
