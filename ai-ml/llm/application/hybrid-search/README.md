<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Hybrid Search 混合搜索

> 本案例详解 RAG 中的混合搜索技术，结合向量检索和关键词检索

## 📐 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hybrid Search 架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Query: "Python programming best practices"                     │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Query Processing                           │   │
│  │  ┌─────────────────┐  ┌─────────────────┐             │   │
│  │  │ Dense Embedding │  │ Keyword Extract │             │   │
│  │  │   (向量化)       │  │    (分词)       │             │   │
│  │  └─────────────────┘  └─────────────────┘             │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Retrieval                              │   │
│  │  ┌─────────────────┐  ┌─────────────────┐             │   │
│  │  │ Vector Search   │  │  BM25 Search   │             │   │
│  │  │ (语义相似度)    │  │  (关键词匹配)   │             │   │
│  │  └────────┬────────┘  └────────┬────────┘             │   │
│  │           │                    │                       │   │
│  │           └──────────┬─────────┘                       │   │
│  │                      ▼                                  │   │
│  │              ┌─────────────┐                          │   │
│  │              │   RRF Fusion │  ← Reciprocal Rank Fusion│   │
│  │              └─────────────┘                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                      │                                         │
│                      ▼                                         │
│              Top-K Results                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 💻 核心实现

### RRF 融合

```python
def reciprocal_rank_fusion(results_list, k=60):
    """RRF 融合多个检索结果"""
    scores = {}
    
    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = doc['id']
            # RRF 分数
            score = 1 / (k + rank + 1)
            scores[doc_id] = scores.get(doc_id, 0) + score
    
    # 排序
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs
```

## 🔗 相关案例

- `rag-fundamentals` - RAG 基础
- `reranking-optimization` - 重排序优化
- `embedding-model-selection` - Embedding 模型选择

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
