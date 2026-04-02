# Elasticsearch Integration Demo

Spring Data Elasticsearch集成演示项目，演示如何使用Elasticsearch进行全文搜索。

## 技术栈

- Spring Boot 2.7
- Spring Data Elasticsearch
- Elasticsearch 7.x/8.x

## 项目结构

```
elasticsearch-integration-demo/
├── src/main/java/com/example/demo/
│   ├── ElasticsearchDemoApplication.java  # 应用入口
│   ├── config/
│   │   └── ElasticsearchConfig.java       # ES配置
│   ├── controller/
│   │   └── ProductController.java         # 商品控制器
│   ├── entity/
│   │   └── Product.java                   # 商品实体
│   ├── repository/
│   │   └── ProductRepository.java         # ES仓库
│   └── service/
│       └── ProductService.java            # 商品服务
├── src/main/resources/
│   ├── application.yml                    # 应用配置
│   └── elasticsearch-settings.json        # ES索引设置
├── pom.xml
└── README.md
```

## Elasticsearch简介

### 什么是Elasticsearch

Elasticsearch是一个开源的分布式搜索和分析引擎，基于Apache Lucene构建。它提供：
- 近实时的全文搜索
- 分布式存储和分析
- RESTful API
- 水平可扩展

### 核心概念

| 概念 | 说明 | 类比关系型数据库 |
|------|------|------------------|
| Index | 索引，存储数据的逻辑容器 | Database |
| Type | 类型（ES 7.x已移除） | Table |
| Document | 文档，基本数据单元 | Row |
| Field | 字段 | Column |
| Mapping | 映射，定义字段类型 | Schema |
| Shard | 分片，数据水平分割 | Partition |
| Replica | 副本，数据冗余备份 | Replica |

## 核心注解说明

### @Document

```java
@Document(indexName = "products", shards = 1, replicas = 0)
public class Product { }
```

- `indexName`: 索引名称
- `shards`: 主分片数
- `replicas`: 副本分片数

### @Field

```java
@Field(type = FieldType.Text, analyzer = "ik_max_word")
private String name;

@Field(type = FieldType.Keyword)
private String category;

@Field(type = FieldType.Double)
private Double price;
```

FieldType类型：
- `Text`: 会被分词，用于全文搜索
- `Keyword`: 不会被分词，用于精确匹配、排序、聚合
- `Integer/Long/Double/Float`: 数值类型
- `Date`: 日期类型
- `Boolean`: 布尔类型

### @Id

```java
@Id
private String id;
```

标记文档ID字段。

## 快速开始

### 1. 启动Elasticsearch

使用Docker启动：

```bash
docker run -d --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
  elasticsearch:7.17.0
```

验证启动：

```bash
curl http://localhost:9200
```

### 2. 启动应用

```bash
mvn spring-boot:run
```

### 3. 初始化数据

```bash
curl -X POST http://localhost:8080/api/products/init
```

### 4. 搜索测试

```bash
# 关键词搜索
curl "http://localhost:8080/api/products/search?keyword=手机"

# 分类查询
curl http://localhost:8080/api/products/category/手机

# 价格范围
curl "http://localhost:8080/api/products/price-range?min=3000&max=8000"

# 分页查询
curl "http://localhost:8080/api/products/category/手机/page?page=0&size=5"

# 添加商品
curl -X POST http://localhost:8080/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "id": "10",
    "name": "iPad Air",
    "description": "苹果平板电脑",
    "price": 4999,
    "category": "平板",
    "brand": "Apple",
    "stock": 50
  }'
```

## Repository方法

### 自动生成的方法

Spring Data Elasticsearch会自动实现以下方法：

```java
// 根据名称包含查询（分词搜索）
List<Product> findByNameContaining(String name);

// 根据分类查询
List<Product> findByCategory(String category);

// 根据价格范围查询
List<Product> findByPriceBetween(Double minPrice, Double maxPrice);

// 分页查询
Page<Product> findByCategory(String category, Pageable pageable);
```

### 自定义查询

使用`@Query`注解自定义ES DSL：

```java
@Query("{" +
        "  \"bool\": {" +
        "    \"must\": [" +
        "      { \"match\": { \"name\": \"?0\" } }," +
        "      { \"range\": { \"price\": { \"lte\": ?1 } } }" +
        "    ]" +
        "  }" +
        "}")
List<Product> findByNameAndMaxPrice(String name, Double maxPrice);
```

## Elasticsearch REST API

### 索引操作

```bash
# 创建索引
curl -X PUT http://localhost:9200/my-index

# 查看索引
curl http://localhost:9200/my-index

# 删除索引
curl -X DELETE http://localhost:9200/my-index
```

### 文档操作

```bash
# 添加文档
curl -X POST http://localhost:9200/products/_doc/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone", "price": 5999}'

# 查询文档
curl http://localhost:9200/products/_doc/1

# 搜索
curl -X POST "http://localhost:9200/products/_search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "match": {
        "name": "iPhone"
      }
    }
  }'

# 删除文档
curl -X DELETE http://localhost:9200/products/_doc/1
```

## Query DSL示例

### Match Query（全文搜索）

```json
{
  "query": {
    "match": {
      "name": "苹果手机"
    }
  }
}
```

### Term Query（精确匹配）

```json
{
  "query": {
    "term": {
      "category": "手机"
    }
  }
}
```

### Range Query（范围查询）

```json
{
  "query": {
    "range": {
      "price": {
        "gte": 3000,
        "lte": 8000
      }
    }
  }
}
```

### Bool Query（组合查询）

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": "手机" } }
      ],
      "filter": [
        { "range": { "price": { "lte": 5000 } } },
        { "term": { "brand": "小米" } }
      ]
    }
  }
}
```

## 中文分词

### IK分词器

```bash
# 安装IK分词器（需要在Elasticsearch中安装）
bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.17.0/elasticsearch-analysis-ik-7.17.0.zip
```

### 分词模式

- `ik_max_word`: 细粒度模式，会分出更多词
- `ik_smart`: 智能模式，会做最粗粒度的拆分

### 测试分词

```bash
curl -X POST "http://localhost:9200/_analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "analyzer": "ik_max_word",
    "text": "苹果手机"
  }'
```

## 生产环境建议

### 1. 集群配置

```yaml
# elasticsearch.yml
cluster.name: my-cluster
node.name: node-1
network.host: 0.0.0.0
discovery.seed_hosts: ["host1", "host2", "host3"]
cluster.initial_master_nodes: ["node-1", "node-2", "node-3"]
```

### 2. 索引模板

```json
{
  "index_patterns": ["products-*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "price": { "type": "double" }
    }
  }
}
```

### 3. 性能优化

- 批量操作：使用Bulk API
- 适当分片：避免过多分片
- 预加载：index.store.preload
- 刷新间隔：index.refresh_interval

## 学习要点

1. Elasticsearch核心概念和架构
2. Spring Data Elasticsearch的使用
3. 全文搜索 vs 精确匹配
4. Query DSL的基本用法
5. 中文分词处理
6. 索引设计和性能优化
