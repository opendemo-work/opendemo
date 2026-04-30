# SpEL 表达式语言演示

> 深入理解 Spring Expression Language，掌握表达式解析、对象属性访问、集合操作和函数调用

## 🎯 学习目标

- ✅ 理解 SpEL 的作用和基本语法
- ✅ 掌握 SpelExpressionParser 的使用
- ✅ 学会对象属性访问和方法调用
- ✅ 掌握集合过滤、投影操作
- ✅ 了解 SpEL 在 @Value、@PreAuthorize 中的应用

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **ExpressionParser** | SpEL 表达式解析器 |
| **EvaluationContext** | 表达式求值上下文 |
| **Expression** | 解析后的表达式对象 |
| **#variable** | 变量引用 |
| **#this** | 当前迭代元素 |
| **T(class)** | 静态类型引用 |

---

## 🛠️ SpEL 运算符

```
┌──────────────────────────────────────────────┐
│              SpEL 运算符                      │
├──────────────────────────────────────────────┤
│  算术: +  -  *  /  %  ^                      │
│  比较: <  >  <=  >=  ==  !=                   │
│  逻辑: and  or  not  !                        │
│  条件: ? : (三元)  ?: (Elvis)                  │
│  安全: ?. (安全导航)                            │
│  正则: matches                                 │
│  类型: T(java.lang.Math)                      │
└──────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. 基础表达式

```java
ExpressionParser parser = new SpelExpressionParser();

// 字面量
parser.parseExpression("'Hello World'").getValue();    // "Hello World"
parser.parseExpression("42").getValue();                // 42
parser.parseExpression("true").getValue();              // true

// 算术运算
parser.parseExpression("1 + 2").getValue();             // 3
parser.parseExpression("2 * 3").getValue();             // 6

// 字符串拼接
parser.parseExpression("'Hello' + ' ' + 'World'").getValue();
```

### 2. 对象属性和方法

```java
User user = new User(1L, "张三", 25, "ADMIN", true);
StandardEvaluationContext context = new StandardEvaluationContext(user);

parser.parseExpression("name").getValue(context);          // "张三"
parser.parseExpression("age > 18").getValue(context);      // true
parser.parseExpression("isAdmin()").getValue(context);     // true
parser.parseExpression("getDisplayName()").getValue(context);
```

### 3. 集合操作

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
context.setVariable("numbers", numbers);

// 过滤 (?.[])
parser.parseExpression("#numbers.?[#this % 2 == 0]").getValue(context);
// → [2, 4, 6, 8, 10]

// 投影 (.![])
parser.parseExpression("#numbers.![#this * 2]").getValue(context);
// → [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// 第一个匹配
parser.parseExpression("#numbers.^[#this > 5]").getValue(context);
// → 6
```

### 4. 静态方法和变量

```java
// 静态方法调用
parser.parseExpression("T(java.lang.Math).random()").getValue();

// 变量引用
context.setVariable("name", "张三");
parser.parseExpression("#name").getValue(context);

// Elvis 运算符
parser.parseExpression("name ?: 'Unknown'").getValue(context);

// 安全导航
parser.parseExpression("name?.length()").getValue(context);
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/spel-demo
mvn spring-boot:run
```

### 2. 观察输出

```
=== SpEL 表达式演示 ===

--- 基础表达式 ---
1 + 2 = 3
2 * 3 = 6
'Hello' + ' ' + 'World' = Hello World
true AND false = false
10 > 5 = true
T(Math).random() = 0.72345...

--- 对象属性访问 ---
name = 张三
age = 25
active = true
isAdmin = true
displayName = 张三 (ADMIN)

--- 集合操作 ---
过滤偶数: [2, 4, 6, 8, 10]
第一个>5: 6
投影*2: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

---

## 📁 项目结构

```
spel-demo/
├── src/main/java/com/example/demo/
│   ├── SpelApplication.java              # 应用入口
│   ├── model/
│   │   └── User.java                     # 用户模型
│   └── service/
│       └── SpelService.java              # SpEL服务
├── src/test/java/com/example/demo/
│   └── SpelDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 SpEL 在 Spring 中的应用

| 场景 | 示例 |
|------|------|
| @Value | `@Value("#{systemProperties['os.name']}")` |
| @PreAuthorize | `@PreAuthorize("hasRole('ADMIN')")` |
| @Cacheable | `@Cacheable(key = "#user.id")` |
| @Conditional | `@ConditionalOnExpression("...'true'}")` |
| XML 配置 | `<property name="#" value="#{bean.property}"/>` |

---

## 🔧 SpEL 集合操作符

| 操作符 | 语法 | 说明 |
|--------|------|------|
| 过滤 | `.?[condition]` | 返回满足条件的元素 |
| 第一个 | `.^[condition]` | 返回第一个满足条件的元素 |
| 最后一个 | `.$[condition]` | 返回最后一个满足条件的元素 |
| 投影 | `.![expression]` | 对每个元素应用表达式 |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Conditional Demo](../conditional-demo/) - 条件装配中的 SpEL
- [Spring Security](../spring-security-basics-demo/) - 安全表达式

---

*最后更新：2026年4月*
