# ☕ Java案例标准化模板

> Java技术案例开发标准模板  
> 版本：1.0.0  
> 作者：OpenDemo团队  

---

## 📋 模板使用说明

此模板用于创建所有Java技术案例，确保案例的一致性和高质量标准。

---

## 🎯 案例命名规范

### 目录命名规则
```
java-{功能领域}-{具体技术}-demo
```

**示例：**
- `java-string-operations-demo`
- `java-file-io-demo` 
- `java-exception-handling-demo`

### 包名规范
```
com.opendemo.java.{功能领域}.{具体技术}
```

**示例：**
- `com.opendemo.java.string.StringOperationsDemo`
- `com.opendemo.java.io.FileIODemo`

---

## 📁 标准目录结构

```
java-case-name-demo/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── opendemo/
│   │               └── java/
│   │                   └── {domain}/
│   │                       ├── Application.java          # 主程序入口
│   │                       ├── service/                  # 业务逻辑层
│   │                       ├── model/                    # 数据模型
│   │                       └── util/                     # 工具类
│   └── test/
│       └── java/
│           └── com/
│               └── opendemo/
│                   └── java/
│                       └── {domain}/
│                           └── ApplicationTest.java      # 测试类
├── pom.xml                                              # Maven配置文件
├── build.gradle                                         # Gradle配置文件(可选)
├── README.md                                            # 案例说明文档
└── metadata.json                                        # 元数据配置
```

---

## 📄 README.md 标准模板

```markdown
# 🎯 Java {技术名称} 实战案例

> 本案例演示如何使用Java {技术名称} 解决 {具体问题/场景}

## 📚 学习目标

完成本案例后，您将能够：
- ✅ 掌握 {核心技术点1}
- ✅ 理解 {核心技术点2} 
- ✅ 应用 {核心技术点3}
- ✅ 解决 {实际应用场景}

## 🛠️ 环境准备

### 系统要求
- **JDK版本**: {推荐版本，如 OpenJDK 11+}
- **构建工具**: Maven 3.6+ 或 Gradle 7+
- **IDE推荐**: IntelliJ IDEA / Eclipse / VS Code
- **操作系统**: Windows/Linux/macOS

### 依赖安装
```bash
# Maven项目
mvn clean install

# Gradle项目  
./gradlew build
```

## 📁 项目结构详解

```
项目根目录/
├── src/main/java/com/opendemo/java/{domain}/
│   ├── Application.java              # 程序主入口
│   ├── {功能类1}.java                # 核心功能实现
│   ├── {功能类2}.java                # 辅助功能实现
│   └── model/
│       └── {数据模型}.java           # 数据模型定义
├── src/test/java/                    # 测试代码目录
└── {配置文件}                        # pom.xml 或 build.gradle
```

## 🚀 快速开始

### 步骤1：环境配置
{详细说明环境配置步骤，包括JDK安装、IDE配置等}

### 步骤2：项目初始化
```bash
# 克隆或创建项目
git clone {项目地址} 或 mkdir {项目名}

# 进入项目目录
cd {项目名}

# 下载依赖
mvn dependency:resolve
```

### 步骤3：代码编写
{提供核心代码示例和关键实现要点}

### 步骤4：编译运行
```bash
# 编译项目
mvn compile

# 运行程序
mvn exec:java -Dexec.mainClass="com.opendemo.java.{domain}.Application"

# 或直接运行jar包
java -jar target/{项目名}.jar
```

## 🔍 核心代码解析

### 主要类说明
**Application.java** - 程序入口类
```java
{提供核心代码示例，包含详细注释}
```

**{功能类}.java** - {功能说明}
```java
{提供关键功能实现代码}
```

### 关键技术点
1. **{技术点1}**: {详细解释和实现原理}
2. **{技术点2}**: {详细解释和实现原理}
3. **{技术点3}**: {详细解释和实现原理}

## 🧪 测试验证

### 单元测试
```java
{提供单元测试代码示例}
```

### 运行测试
```bash
# Maven测试
mvn test

# Gradle测试
./gradlew test
```

### 预期输出
```
{展示程序正常运行的预期输出结果}
```

## ⚠️ 常见问题与解决方案

### Q1: {常见问题1}
**问题描述**: {问题详细描述}
**解决方案**: {解决步骤和代码示例}

### Q2: {常见问题2}
**问题描述**: {问题详细描述}
**解决方案**: {解决步骤和代码示例}

## 📚 扩展学习

### 相关技术文档
- [{技术1官方文档}]({链接})
- [{技术2教程}]({链接})
- [Java {相关版本} 新特性]({链接})

### 进阶学习路径
1. {进阶学习方向1}
2. {进阶学习方向2}
3. {进阶学习方向3}

### 企业级应用场景
- {应用场景1}: {简要说明}
- {应用场景2}: {简要说明}
- {应用场景3}: {简要说明}

## 🎯 最佳实践建议

1. **代码规范**: 遵循Google Java Style Guide
2. **异常处理**: 合理使用try-catch-finally结构
3. **资源管理**: 及时关闭IO流和数据库连接
4. **性能优化**: 避免重复创建对象，合理使用缓存

---
> **💡 提示**: {相关的技术提示或注意事项}
```

---

## 📄 metadata.json 标准格式

```json
{
  "name": "java-{技术名称}-demo",
  "language": "java",
  "keywords": ["java", "{技术关键词1}", "{技术关键词2}", "{应用场景}"],
  "description": "Java {技术名称} {具体应用场景} 完整示例",
  "difficulty": "{beginner|intermediate|advanced}",
  "author": "OpenDemo Team",
  "created_at": "{YYYY-MM-DD}",
  "updated_at": "{YYYY-MM-DD}",
  "version": "1.0.0",
  "dependencies": {
    "java_version": "{版本要求，如 11+}",
    "build_tool": "{maven|gradle}",
    "frameworks": ["{框架名}:{版本号}"]
  },
  "verified": true,
  "estimated_time": "{预计学习时间，如 1-2小时}",
  "prerequisites": ["{前置知识1}", "{前置知识2}"],
  "learning_outcomes": [
    "掌握{核心技术点1}",
    "理解{核心技术点2}",
    "能够应用{技术}解决{具体问题}"
  ],
  "related_cases": ["{相关案例1}", "{相关案例2}"],
  "validation_commands": [
    "mvn compile",
    "mvn test",
    "java -jar target/app.jar"
  ]
}
```

---

## 💻 代码质量标准

### Java代码规范
```java
// 1. 包声明和导入
package com.opendemo.java.{domain};

import java.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * {类功能描述}
 * 
 * @author OpenDemo Team
 * @since 1.0.0
 */
public class {ClassName} {
    
    // 2. 日志记录器
    private static final Logger logger = LoggerFactory.getLogger({ClassName}.class);
    
    // 3. 常量定义
    private static final String CONSTANT_NAME = "value";
    
    // 4. 成员变量
    private String instanceVariable;
    
    // 5. 构造函数
    public {ClassName}() {
        // 初始化逻辑
    }
    
    // 6. 公共方法
    /**
     * {方法功能描述}
     * 
     * @param param {参数说明}
     * @return {返回值说明}
     * @throws {异常类型} {异常说明}
     */
    public ReturnType methodName(ParameterType param) throws Exception {
        try {
            // 核心逻辑
            logger.info("Executing method with param: {}", param);
            return result;
        } catch (Exception e) {
            logger.error("Error occurred: ", e);
            throw e;
        }
    }
}
```

### 测试代码规范
```java
package com.opendemo.java.{domain};

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * {类名}测试类
 */
class {ClassName}Test {
    
    private {ClassName} instance;
    
    @BeforeEach
    void setUp() {
        instance = new {ClassName}();
    }
    
    @Test
    void testMethod_ShouldReturnExpectedResult() {
        // Given
        String input = "test input";
        String expected = "expected result";
        
        // When
        String actual = instance.testMethod(input);
        
        // Then
        assertEquals(expected, actual, "Should return expected result");
    }
}
```

---

## ✅ 质量检查清单

在发布案例前，请确认以下事项：

### 文档完整性 ✓
- [ ] README.md 文档完整且≥800字
- [ ] 包含详细的学习目标说明
- [ ] 提供完整的环境配置指南
- [ ] 包含逐步操作指导
- [ ] 有常见问题解答部分
- [ ] 提供扩展学习资源

### 代码质量 ✓
- [ ] 遵循Java命名规范
- [ ] 代码注释完整清晰
- [ ] 包含必要的日志记录
- [ ] 异常处理合理
- [ ] 资源管理正确
- [ ] 通过编译检查

### 测试验证 ✓
- [ ] 包含单元测试
- [ ] 测试覆盖率≥80%
- [ ] 所有测试通过
- [ ] 提供测试运行说明

### 配置文件 ✓
- [ ] pom.xml/gradle.build 配置正确
- [ ] metadata.json 信息完整准确
- [ ] 依赖版本明确指定

---

## 🚀 案例发布流程

1. **创建分支**: `git checkout -b java-{case-name}-demo`
2. **按照模板开发**: 遵循上述标准规范
3. **本地测试**: 确保所有功能正常运行
4. **代码审查**: 团队成员进行代码质量检查
5. **文档审核**: 确认文档完整性和准确性
6. **合并主干**: `git merge main && git push origin main`
7. **更新索引**: 在java/README.md中添加案例信息

---

> **📌 注意**: 所有Java案例都应遵循此模板，保持项目的一致性和专业性。