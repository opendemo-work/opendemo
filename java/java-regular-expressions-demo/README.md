# Java正则表达式完整示例

## 🎯 案例概述

这是一个全面展示Java正则表达式应用的完整示例，涵盖了从基础匹配到高级数据处理的各种场景。

## 📚 学习目标

通过本示例你将掌握：
- 正则表达式基础语法和Java实现
- 文本验证、提取、替换的核心技术
- 复杂数据解析和配置文件处理
- 性能优化和最佳实践

## 🔧 核心知识点

### 1. 基础模式匹配
- `Pattern` 和 `Matcher` 类的使用
- 预编译正则表达式的优势
- 常用匹配方法：`find()`, `matches()`, `lookingAt()`

### 2. 文本提取技术
- 分组捕获 `(group)`
- 命名分组 `(?<name>pattern)`
- 多行匹配模式 `MULTILINE`

### 3. 文本替换策略
- `replaceAll()` 和 `replaceFirst()`
- 引用捕获组 `$1`, `$2`
- 字符串脱敏处理

### 4. 数据验证应用
- 邮箱、电话、URL格式验证
- 密码强度检查
- IPv4地址验证

### 5. 复杂数据解析
- CSV格式数据解析
- 配置文件解析
- 日志信息提取

### 6. 性能优化
- Pattern预编译的重要性
- 性能基准测试
- 正则表达式优化技巧

## 🚀 运行示例

```bash
# 编译项目
mvn compile

# 运行主程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.regex.RegularExpressionsDemo"

# 运行测试
mvn test
```

## 📖 代码详解

### 主要类结构

```java
public class RegularExpressionsDemo {
    // 预编译常用模式
    private static final Pattern EMAIL_PATTERN = Pattern.compile("...");
    private static final Pattern PHONE_PATTERN = Pattern.compile("...");
    
    // 六个核心演示方法
    public void demonstrateBasicMatching() { ... }      // 基础匹配
    public void demonstrateTextExtraction() { ... }     // 文本提取
    public void demonstrateTextReplacement() { ... }    // 文本替换
    public void demonstrateDataValidation() { ... }     // 数据验证
    public void demonstrateComplexParsing() { ... }     // 复杂解析
    public void demonstratePerformanceOptimization() { ... } // 性能优化
}
```

### 关键技术点

#### 1. 预编译模式的优势
```java
// 推荐：预编译模式（高效）
private static final Pattern EMAIL_PATTERN = Pattern.compile(regex);
Matcher matcher = EMAIL_PATTERN.matcher(text);

// 不推荐：重复编译（低效）
Matcher matcher = Pattern.compile(regex).matcher(text);
```

#### 2. 分组捕获示例
```java
Pattern pattern = Pattern.compile("(\\d{6})\\d{8}(\\d{4})");
Matcher matcher = pattern.matcher("身份证: 110101199001011234");
if (matcher.find()) {
    String prefix = matcher.group(1);  // "110101"
    String suffix = matcher.group(2);  // "1234"
}
```

#### 3. 性能对比测试
```java
// 预编译模式 vs 重复编译模式
long time1 = measureTime(() -> precompiledPattern.matcher(text).find());
long time2 = measureTime(() -> Pattern.compile(regex).matcher(text).find());
// 通常预编译快2-10倍
```

## 🧪 测试覆盖

测试类 `RegularExpressionsDemoTest` 包含以下测试：

✅ 邮箱格式验证测试  
✅ 电话号码验证测试  
✅ URL地址验证测试  
✅ IPv4地址验证测试  
✅ 文本提取功能测试  
✅ 文本替换功能测试  
✅ 密码强度验证测试  
✅ CSV数据解析测试  
✅ 配置文件解析测试  
✅ 性能对比测试  

## 🎯 实际应用场景

### 1. 表单数据验证
```java
// 验证用户输入
if (!EMAIL_PATTERN.matcher(email).matches()) {
    throw new ValidationException("邮箱格式不正确");
}
```

### 2. 敏感信息脱敏
```java
// 身份证脱敏
String masked = idCard.replaceAll("(\\d{6})\\d{8}(\\d{4})", "$1********$2");
```

### 3. 日志分析处理
```java
// 提取错误日志
Pattern errorPattern = Pattern.compile("ERROR (.+)");
Matcher matcher = errorPattern.matcher(logContent);
while (matcher.find()) {
    processError(matcher.group(1));
}
```

### 4. 配置文件解析
```java
// 解析key=value格式
Pattern configPattern = Pattern.compile("^([\\w.]+)=(.*)$");
Matcher matcher = configPattern.matcher(configLine);
if (matcher.matches()) {
    configMap.put(matcher.group(1), matcher.group(2));
}
```

## ⚡ 性能优化建议

### 1. 必须做的优化
- ✅ 预编译常用正则表达式模式
- ✅ 重用Pattern对象而不是重复编译
- ✅ 使用合适的量词避免回溯

### 2. 应该注意的问题
- ⚠️ 避免过于复杂的正则表达式
- ⚠️ 注意贪婪匹配vs非贪婪匹配
- ⚠️ 考虑使用字符串方法替代简单场景

### 3. 可以考虑的方案
- 💡 对于高频使用的模式考虑缓存
- 💡 复杂验证可拆分为多个简单正则
- 💡 大文本处理时考虑流式处理

## 📊 性能基准

典型性能对比（10000次匹配）：
- 预编译模式：~2ms
- 重复编译模式：~15ms
- 性能提升：约7-8倍

## 🔍 常见陷阱和解决方案

### 1. 回溯问题
```java
// 问题：可能导致灾难性回溯
String badRegex = "^(a+)+$";

// 解决：使用原子组或固化分组
String goodRegex = "^(?>a+)+$";
```

### 2. 贪婪匹配陷阱
```java
// 问题：可能匹配过多内容
String greedy = "<.+>";     // 匹配 <div>content</div>

// 解决：使用非贪婪匹配
String nonGreedy = "<.+?>"; // 只匹配 <div>
```

### 3. Unicode处理
```java
// 问题：默认不处理Unicode字符
String asciiOnly = "\\w+";  // 只匹配ASCII字母

// 解决：启用Unicode支持
String unicodeAware = "(?U)\\w+";  // 支持Unicode字母
```

## 📚 扩展学习资源

### 官方文档
- [Java Pattern类文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Pattern.html)
- [Java Matcher类文档](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Matcher.html)

### 推荐书籍
- 《精通正则表达式》- Jeffrey E.F. Friedl
- 《Java核心技术》- Cay S. Horstmann

### 在线工具
- [Regex101](https://regex101.com/) - 正则表达式在线测试
- [RegExr](https://regexr.com/) - 正则表达式学习工具

## 🔄 版本历史

- v1.0.0 (2024-01-15): 初始版本，包含基础正则表达式功能演示

---
**注意**: 本示例仅用于学习目的，请勿在生产环境中直接使用未经充分测试的正则表达式。