<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Maven 多模块项目架构演示

## 项目简介

本项目是一个 Maven 多模块（Multi-Module）项目架构演示，展示如何使用 Maven 管理具有多个子模块的 Java 项目。项目采用**分层架构**设计，包含公共基础模块、业务服务模块和 Web 应用模块，模块之间通过 Maven 依赖机制进行关联。

通过本项目，你将掌握 Maven 多模块项目的结构设计、父子 POM 继承机制、模块间依赖管理、`dependencyManagement` 统一版本控制等核心概念。

---

## 目录

1. [多模块项目架构概述](#1-多模块项目架构概述)
2. [父子 POM 继承机制](#2-父子pom继承机制)
3. [dependencyManagement 版本控制](#3-dependencymanagement版本控制)
4. [模块间依赖关系](#4-模块间依赖关系)
5. [多模块构建与聚合](#5-多模块构建与聚合)
6. [分层架构设计原则](#6-分层架构设计原则)
7. [项目代码结构说明](#7-项目代码结构说明)
8. [快速开始](#8-快速开始)
9. [常见问题](#9-常见问题)
10. [参考资料](#10-参考资料)

---

## 1. 多模块项目架构概述

### 什么是多模块项目？

Maven 多模块项目允许将一个大型项目拆分为多个相互关联的子模块。每个子模块是一个独立的 Maven 项目，拥有自己的 `pom.xml` 和源代码目录，同时通过父 POM 进行统一管理。

### 项目结构

```
multi-module-project-demo/
├── pom.xml                           (父 POM，packaging=pom)
├── multi-module-common/              (公共基础模块)
│   ├── pom.xml                       (子模块 POM，继承父 POM)
│   └── src/main/java/
│       └── com/opendemo/java/modules/common/
│           ├── model/BaseEntity.java       (基础实体类)
│           ├── util/StringUtils.java       (字符串工具类)
│           └── exception/BusinessException.java  (业务异常)
├── multi-module-service/             (业务服务模块)
│   ├── pom.xml                       (依赖 common 模块)
│   └── src/main/java/
│       └── com/opendemo/java/modules/service/
│           ├── UserService.java            (用户服务)
│           └── OrderService.java           (订单服务)
├── multi-module-web/                 (Web 应用模块)
│   ├── pom.xml                       (依赖 service 模块)
│   └── src/main/java/
│       └── com/opendemo/java/modules/web/
│           ├── Application.java            (应用入口)
│           └── controller/UserController.java  (用户控制器)
├── README.md
└── metadata.json
```

### 多模块项目的优势

| 优势 | 说明 |
|------|------|
| **关注点分离** | 每个模块专注于特定功能领域 |
| **代码复用** | 公共模块可被多个模块复用 |
| **独立构建** | 可以单独编译、测试某个模块 |
| **统一管理** | 父 POM 统一管理版本和插件 |
| **团队协作** | 不同团队负责不同模块 |
| **部署灵活** | 可按模块独立部署 |

---

## 2. 父子 POM 继承机制

Maven POM 继承类似 Java 的类继承。子模块通过 `<parent>` 声明父 POM，自动继承父 POM 中的配置。

### 父 POM 配置

```xml
<groupId>com.opendemo.java</groupId>
<artifactId>multi-module-project-demo</artifactId>
<version>1.0.0</version>
<packaging>pom</packaging>        <!-- 父 POM 必须使用 pom 打包类型 -->
<modules>
    <module>multi-module-common</module>
    <module>multi-module-service</module>
    <module>multi-module-web</module>
</modules>
```

关键点：
- 父 POM 的 `<packaging>` 必须为 `pom`
- `<modules>` 声明所有子模块的目录名
- 父 POM 中定义公共的 `<properties>`、`<dependencies>`、`<plugins>`

### 子模块 POM 配置

```xml
<parent>
    <groupId>com.opendemo.java</groupId>
    <artifactId>multi-module-project-demo</artifactId>
    <version>1.0.0</version>
</parent>
<artifactId>multi-module-common</artifactId>
```

关键点：
- 子模块通过 `<parent>` 引用父 POM
- 子模块的 `groupId` 和 `version` 可以省略（自动继承）
- 子模块只需声明自己的 `artifactId`

### 继承的内容

子模块自动继承父 POM 中的以下配置：

| 继承项 | 示例 |
|--------|------|
| `groupId` | `com.opendemo.java` |
| `version` | `1.0.0` |
| `properties` | `maven.compiler.source=11` |
| `dependencies` | 公共依赖 |
| `dependencyManagement` | 版本管理 |
| `build.plugins` | 构建插件 |
| `repositories` | 仓库配置 |

---

## 3. dependencyManagement 版本控制

父 POM 中的 `<dependencyManagement>` 用于统一管理依赖版本，子模块声明依赖时无需指定版本号。

### 父 POM 声明

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>${slf4j.version}</version>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 子模块引用（无需版本号）

```xml
<dependencies>
    <dependency>
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-api</artifactId>
        <!-- 版本由父 POM 管理 -->
    </dependency>
</dependencies>
```

### dependencyManagement vs dependencies

| 特性 | `dependencyManagement` | `dependencies` |
|------|----------------------|----------------|
| 是否自动引入依赖 | ❌ 只声明版本，不引入 | ✅ 直接引入依赖 |
| 子模块是否必须使用 | ❌ 可选使用 | ✅ 所有子模块都会继承 |
| 用途 | 统一版本管理 | 提供公共依赖 |

---

## 4. 模块间依赖关系

本项目的模块依赖关系如下：

```
multi-module-web (Web 层)
    └── depends on → multi-module-service (Service 层)
                         └── depends on → multi-module-common (Common 层)
```

### 依赖声明

```xml
<!-- multi-module-service/pom.xml -->
<dependency>
    <groupId>com.opendemo.java</groupId>
    <artifactId>multi-module-common</artifactId>
    <version>${project.version}</version>
</dependency>

<!-- multi-module-web/pom.xml -->
<dependency>
    <groupId>com.opendemo.java</groupId>
    <artifactId>multi-module-service</artifactId>
    <version>${project.version}</version>
</dependency>
```

### 依赖传递性

由于 Maven 的依赖传递机制：
- `web` 模块依赖 `service` 模块
- `service` 模块依赖 `common` 模块
- 因此 `web` 模块可以间接使用 `common` 模块的类

### 避免循环依赖

多模块项目中**严禁循环依赖**：

```
# 错误示例（循环依赖）
A → B → C → A   ❌

# 正确示例（单向依赖）
A → B → C       ✅
```

---

## 5. 多模块构建与聚合

### 构建命令

```bash
# 构建所有模块（按依赖顺序）
mvn clean install

# 构建指定模块及其依赖
mvn clean install -pl multi-module-web -am

# 只构建指定模块（不构建依赖）
mvn clean compile -pl multi-module-common

# 跳过测试
mvn clean install -DskipTests
```

### Maven Reactor

Maven Reactor 负责确定模块的构建顺序：

1. 解析所有模块的依赖关系
2. 构建**有向无环图（DAG）**
3. 按拓扑排序确定构建顺序
4. 按顺序执行每个模块的生命周期阶段

本项目的构建顺序：

```
[INFO] Reactor Build Order:
[INFO]   multi-module-project-demo .............. (parent)
[INFO]   multi-module-common .................... (common)
[INFO]   multi-module-service ................... (service)
[INFO]   multi-module-web ........................ (web)
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-pl` | 指定模块 | `-pl multi-module-service` |
| `-am` | 同时构建依赖模块 | `-pl multi-module-web -am` |
| `-amd` | 同时构建依赖此模块的模块 | `-pl multi-module-common -amd` |
| `-rf` | 从指定模块开始构建 | `-rf multi-module-service` |

---

## 6. 分层架构设计原则

### 本项目的分层模型

```
┌─────────────────────────────┐
│        Web Layer            │  multi-module-web
│  (Controller / Application) │  处理HTTP请求，返回响应
├─────────────────────────────┤
│       Service Layer         │  multi-module-service
│  (UserService / OrderService)│  业务逻辑处理
├─────────────────────────────┤
│       Common Layer          │  multi-module-common
│  (Model / Util / Exception) │  公共基础设施
└─────────────────────────────┘
```

### 各层职责

| 层 | 模块 | 职责 |
|----|------|------|
| **Common** | `multi-module-common` | 提供基础实体、工具类、异常定义 |
| **Service** | `multi-module-service` | 封装业务逻辑，调用 Common 层 |
| **Web** | `multi-module-web` | 处理外部请求，调用 Service 层 |

### 设计原则

1. **单向依赖**：Web → Service → Common，不允许反向依赖
2. **接口隔离**：每个模块只暴露必要的类，内部实现细节隐藏
3. **单一职责**：每个模块只负责一个功能领域
4. **开闭原则**：通过继承 `BaseEntity` 扩展新实体，无需修改基础类

---

## 7. 项目代码结构说明

### common 模块

- **BaseEntity.java**：抽象基础实体类，提供 `id`、`createdAt`、`updatedAt` 公共字段
- **StringUtils.java**：字符串工具类，提供空判断、截断、反转等操作
- **BusinessException.java**：通用业务异常类，包含错误码和消息

### service 模块

- **UserService.java**：用户管理服务，提供用户创建、查询、删除功能
- **OrderService.java**：订单管理服务，提供订单创建、查询、统计功能，使用 `BusinessException` 处理异常

### web 模块

- **Application.java**：应用入口，演示模块间的协作
- **UserController.java**：模拟控制器，整合 UserService 和 OrderService 提供用户详情

---

## 8. 快速开始

### 前置条件

- JDK 11 或更高版本
- Maven 3.6+ 已安装并配置

### 构建所有模块

```bash
cd java/multi-module-project-demo
mvn clean install
```

### 构建指定模块

```bash
# 只构建 common 模块
mvn clean install -pl multi-module-common

# 构建 web 模块及其所有依赖
mvn clean install -pl multi-module-web -am
```

### 运行应用

```bash
# 编译并运行主类
mvn exec:java -pl multi-module-web -Dexec.mainClass="com.opendemo.java.modules.web.Application"
```

### 查看依赖树

```bash
mvn dependency:tree
```

---

## 9. 常见问题

### Q1: 子模块找不到父 POM 怎么办？

确保先在根目录执行 `mvn install` 安装父 POM 到本地仓库。

### Q2: 如何单独编译某个模块？

```bash
mvn compile -pl multi-module-service
```

### Q3: 模块间如何共享资源文件？

将共享的资源文件放在 `common` 模块的 `src/main/resources` 目录下，其他模块通过依赖自动获取。

### Q4: 如何处理模块间的版本不一致？

在父 POM 的 `<dependencyManagement>` 中统一管理所有依赖版本，子模块不要单独声明版本。

---

## 10. 参考资料

- [Maven Multi-Module Guide](https://maven.apache.org/guides/mini/guide-multiple-modules.html)
- [Maven POM Inheritance](https://maven.apache.org/pom.html#Inheritance)
- [Maven Reactor](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Maven_Reactor)
- [dependencyManagement Best Practices](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Importing_Dependencies)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

```bash
./scripts/demo.sh
```

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
