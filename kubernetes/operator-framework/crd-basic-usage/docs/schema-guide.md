# OpenAPI Schema设计指南

本文档详细说明如何为CRD设计高质量的OpenAPI v3 Schema。

## Schema基础结构

```yaml
schema:
  openAPIV3Schema:
    type: object
    properties:
      spec:    # 用户期望状态
      status:  # 实际运行状态
```

## 字段类型定义

### 基本类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `string` | 字符串 | `"nginx:1.21"` |
| `integer` | 整数 | `3` |
| `number` | 数字（含小数） | `1.5` |
| `boolean` | 布尔值 | `true` |
| `object` | 对象 | `{cpu: "100m"}` |
| `array` | 数组 | `[1, 2, 3]` |

### 类型验证规则

**字符串验证**：
```yaml
image:
  type: string
  minLength: 1
  maxLength: 255
  pattern: '^[a-z0-9-]+$'  # 正则表达式
  enum: ["dev", "prod"]     # 枚举值
```

**数字验证**：
```yaml
replicas:
  type: integer
  minimum: 1
  maximum: 100
  multipleOf: 2  # 必须是2的倍数
  exclusiveMinimum: true  # 不包含最小值
```

**对象验证**：
```yaml
resources:
  type: object
  required: ["cpu"]  # 必填字段
  properties:
    cpu:
      type: string
    memory:
      type: string
  additionalProperties: false  # 不允许额外字段
```

**数组验证**：
```yaml
ports:
  type: array
  minItems: 1
  maxItems: 10
  uniqueItems: true  # 元素唯一
  items:
    type: integer
```

## 高级特性

### 1. 字段默认值

```yaml
replicas:
  type: integer
  default: 1  # 用户未指定时使用默认值
```

### 2. 字段描述

```yaml
image:
  type: string
  description: "容器镜像地址，格式如 nginx:1.21"
```

### 3. 字段格式

```yaml
createdAt:
  type: string
  format: date-time  # RFC3339格式
  
email:
  type: string
  format: email  # 邮箱格式
```

### 4. 条件验证（oneOf/anyOf/allOf）

```yaml
# 二选一
storage:
  oneOf:
  - required: ["emptyDir"]
  - required: ["persistentVolumeClaim"]
```

## 最佳实践

### 1. 必填字段设计

只将真正必须的字段标记为required：
```yaml
spec:
  type: object
  required:
  - replicas
  - image
  properties:
    replicas:
      type: integer
    image:
      type: string
    port:
      type: integer
      default: 8080  # 可选字段提供默认值
```

### 2. 合理的验证规则

- 副本数：1-100
- 端口号：1-65535
- 镜像名：符合Docker命名规范
- CPU/内存：Kubernetes资源格式

### 3. 清晰的字段组织

```yaml
spec:
  properties:
    # 基础配置
    replicas:
    image:
    
    # 网络配置
    ports:
    service:
    
    # 资源配置
    resources:
      properties:
        requests:
        limits:
```

### 4. 使用枚举限制选择

```yaml
phase:
  type: string
  enum:
  - Pending
  - Running
  - Failed
  - Succeeded
```

## 常见错误及解决

### 错误1：Schema嵌套过深

❌ 避免：
```yaml
spec.config.database.mysql.connection.pool.maxSize
```

✅ 推荐：
```yaml
spec.database.maxConnections
```

### 错误2：过于宽松的验证

❌ 避免：
```yaml
port:
  type: integer  # 没有范围限制
```

✅ 推荐：
```yaml
port:
  type: integer
  minimum: 1
  maximum: 65535
```

### 错误3：缺少description

❌ 避免：
```yaml
ttl:
  type: integer
```

✅ 推荐：
```yaml
ttl:
  type: integer
  description: "资源生存时间（秒），0表示永不过期"
```

## 参考链接

- [OpenAPI 3.0 Schema Specification](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.0.md)
- [Kubernetes API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
# OpenAPI Schema设计指南

本文档详细说明如何为CRD设计高质量的OpenAPI v3 Schema。

## Schema基础结构

```yaml
schema:
  openAPIV3Schema:
    type: object
    properties:
      spec:    # 用户期望状态
      status:  # 实际运行状态
```

## 字段类型定义

### 基本类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `string` | 字符串 | `"nginx:1.21"` |
| `integer` | 整数 | `3` |
| `number` | 数字（含小数） | `1.5` |
| `boolean` | 布尔值 | `true` |
| `object` | 对象 | `{cpu: "100m"}` |
| `array` | 数组 | `[1, 2, 3]` |

### 类型验证规则

**字符串验证**：
```yaml
image:
  type: string
  minLength: 1
  maxLength: 255
  pattern: '^[a-z0-9-]+$'  # 正则表达式
  enum: ["dev", "prod"]     # 枚举值
```

**数字验证**：
```yaml
replicas:
  type: integer
  minimum: 1
  maximum: 100
  multipleOf: 2  # 必须是2的倍数
  exclusiveMinimum: true  # 不包含最小值
```

**对象验证**：
```yaml
resources:
  type: object
  required: ["cpu"]  # 必填字段
  properties:
    cpu:
      type: string
    memory:
      type: string
  additionalProperties: false  # 不允许额外字段
```

**数组验证**：
```yaml
ports:
  type: array
  minItems: 1
  maxItems: 10
  uniqueItems: true  # 元素唯一
  items:
    type: integer
```

## 高级特性

### 1. 字段默认值

```yaml
replicas:
  type: integer
  default: 1  # 用户未指定时使用默认值
```

### 2. 字段描述

```yaml
image:
  type: string
  description: "容器镜像地址，格式如 nginx:1.21"
```

### 3. 字段格式

```yaml
createdAt:
  type: string
  format: date-time  # RFC3339格式
  
email:
  type: string
  format: email  # 邮箱格式
```

### 4. 条件验证（oneOf/anyOf/allOf）

```yaml
# 二选一
storage:
  oneOf:
  - required: ["emptyDir"]
  - required: ["persistentVolumeClaim"]
```

## 最佳实践

### 1. 必填字段设计

只将真正必须的字段标记为required：
```yaml
spec:
  type: object
  required:
  - replicas
  - image
  properties:
    replicas:
      type: integer
    image:
      type: string
    port:
      type: integer
      default: 8080  # 可选字段提供默认值
```

### 2. 合理的验证规则

- 副本数：1-100
- 端口号：1-65535
- 镜像名：符合Docker命名规范
- CPU/内存：Kubernetes资源格式

### 3. 清晰的字段组织

```yaml
spec:
  properties:
    # 基础配置
    replicas:
    image:
    
    # 网络配置
    ports:
    service:
    
    # 资源配置
    resources:
      properties:
        requests:
        limits:
```

### 4. 使用枚举限制选择

```yaml
phase:
  type: string
  enum:
  - Pending
  - Running
  - Failed
  - Succeeded
```

## 常见错误及解决

### 错误1：Schema嵌套过深

❌ 避免：
```yaml
spec.config.database.mysql.connection.pool.maxSize
```

✅ 推荐：
```yaml
spec.database.maxConnections
```

### 错误2：过于宽松的验证

❌ 避免：
```yaml
port:
  type: integer  # 没有范围限制
```

✅ 推荐：
```yaml
port:
  type: integer
  minimum: 1
  maximum: 65535
```

### 错误3：缺少description

❌ 避免：
```yaml
ttl:
  type: integer
```

✅ 推荐：
```yaml
ttl:
  type: integer
  description: "资源生存时间（秒），0表示永不过期"
```

## 参考链接

- [OpenAPI 3.0 Schema Specification](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.0.md)
- [Kubernetes API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)
