<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Maven 项目结构规范演示

## 项目简介

本项目是一个完整的 Maven 项目结构规范演示，旨在帮助开发者理解 Maven 项目的标准目录布局、`pom.xml` 配置文件的各个组成部分、Maven 生命周期（Lifecycle）的各个阶段（Phase）、依赖管理（Dependency Management）的范围（Scope）以及构建插件（Plugin）的配置方式。

通过本项目，你将掌握如何创建符合 Maven 规范的 Java 项目，理解各层代码的组织方式，并学会使用 Maven 进行项目的编译、测试和打包。

---

## 目录

1. [Maven 标准目录结构](#1-maven-标准目录结构)
2. [pom.xml 文件结构详解](#2-pomxml-文件结构详解)
3. [Maven 生命周期与阶段](#3-maven-生命周期与阶段)
4. [依赖范围（Scope）](#4-依赖范围scope)
5. [Maven Profile 配置](#5-maven-profile-配置)
6. [构建插件（Plugin）](#6-构建插件plugin)
7. [项目代码结构说明](#7-项目代码结构说明)
8. [快速开始](#8-快速开始)
9. [常见问题](#9-常见问题)
10. [参考资料](#10-参考资料)

---

## 1. Maven 标准目录结构

Maven 遵循 **Convention over Configuration（约定优于配置）** 的原则，定义了一套标准的目录结构。所有使用 Maven 的项目都应该遵循这个结构。

### 标准目录布局

```
project-root/
├── pom.xml                          # Project Object Model 配置文件
├── src/
│   ├── main/                        # 主代码目录
│   │   ├── java/                    # Java 源代码
│   │   │   └── com/opendemo/java/maven/
│   │   │       ├── MavenStructureDemo.java
│   │   │       ├── model/           # 数据模型（Entity / DTO）
│   │   │       ├── service/         # 业务逻辑层（Service Layer）
│   │   │       ├── util/            # 工具类（Utility Classes）
│   │   │       └── exception/       # 自定义异常
│   │   ├── resources/               # 资源文件（配置文件、静态资源等）
│   │   │   ├── application.properties
│   │   │   └── logback.xml
│   │   └── webapp/                  # Web 应用目录（仅 WAR 项目）
│   │       ├── WEB-INF/
│   │       └── index.html
│   └── test/                        # 测试代码目录
│       ├── java/                    # 测试 Java 代码
│       └── resources/               # 测试资源文件
└── target/                          # 构建输出目录（自动生成）
    ├── classes/                     # 编译后的 class 文件
    ├── test-classes/                # 编译后的测试 class 文件
    └── maven-project-structure-demo-1.0.0.jar
```

### 目录说明

| 目录 | 用途 | 说明 |
|------|------|------|
| `src/main/java` | 源代码 | 存放所有 Java 源文件，按包名组织 |
| `src/main/resources` | 资源文件 | 配置文件、属性文件、XML 等 |
| `src/main/webapp` | Web 资源 | 仅在 WAR 包项目中使用 |
| `src/test/java` | 测试代码 | 存放单元测试和集成测试 |
| `src/test/resources` | 测试资源 | 测试用的配置文件 |
| `target` | 构建输出 | Maven 自动生成的编译输出 |

---

## 2. pom.xml 文件结构详解

`pom.xml`（Project Object Model）是 Maven 项目的核心配置文件。以下是本项目的 `pom.xml` 结构分析：

### 基本坐标（GAV）

每个 Maven 项目通过 **GAV 坐标** 来唯一标识：

```xml
<groupId>com.opendemo.java</groupId>
<artifactId>maven-project-structure-demo</artifactId>
<version>1.0.0</version>
<packaging>jar</packaging>
```

- **groupId**：组织或公司的标识，通常使用域名的反写形式
- **artifactId**：项目的唯一标识符，即项目名称
- **version**：项目版本号，遵循 Semantic Versioning 语义化版本规范
- **packaging**：打包类型，可选 `jar`、`war`、`pom`、`ear` 等

### Properties 属性管理

```xml
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <junit.version>5.9.2</junit.version>
</properties>
```

Properties 用于集中管理版本号和配置参数，方便统一升级和维护。使用 `${property.name}` 引用。

### Dependencies 依赖声明

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>${junit.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

每个 `<dependency>` 声明一个外部依赖，通过 GAV 坐标从 Maven Central 仓库下载。

---

## 3. Maven 生命周期与阶段

Maven 定义了三套相互独立的生命周期（Lifecycle），每个生命周期包含多个阶段（Phase）。

### Clean 生命周期

| 阶段 | 说明 |
|------|------|
| `pre-clean` | 执行清理前的操作 |
| `clean` | 删除 `target` 目录 |
| `post-clean` | 执行清理后的操作 |

### Default 生命周期（核心）

| 阶段 | 说明 |
|------|------|
| `validate` | 验证项目结构是否正确 |
| `initialize` | 初始化构建状态 |
| `compile` | 编译源代码 |
| `test` | 运行单元测试 |
| `package` | 打包为 JAR/WAR |
| `verify` | 验证包的有效性 |
| `install` | 安装到本地仓库 |
| `deploy` | 部署到远程仓库 |

### Site 生命周期

| 阶段 | 说明 |
|------|------|
| `site` | 生成项目站点文档 |
| `site-deploy` | 部署站点文档 |

### 常用命令

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 编译项目
mvn compile

# 运行测试
mvn test

# 打包项目（会自动执行 compile 和 test）
mvn package

# 安装到本地仓库
mvn install

# 清理并打包
mvn clean package

# 跳过测试打包
mvn clean package -DskipTests
```

---

## 4. 依赖范围（Scope）

Maven 通过 `<scope>` 来控制依赖在不同构建阶段的可用性：

| Scope | 编译 | 测试 | 运行 | 说明 |
|-------|------|------|------|------|
| `compile`（默认） | ✅ | ✅ | ✅ | 全阶段可用 |
| `provided` | ✅ | ✅ | ❌ | 由 JDK 或容器提供 |
| `runtime` | ❌ | ✅ | ✅ | 仅运行时需要（如 JDBC 驱动） |
| `test` | ❌ | ✅ | ❌ | 仅测试阶段可用（如 JUnit） |
| `system` | ✅ | ✅ | ❌ | 需显式指定本地 JAR 路径 |
| `import` | - | - | - | 仅用于 dependencyManagement |

### 示例

```xml
<!-- 测试范围依赖 -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.2</version>
    <scope>test</scope>
</dependency>

<!-- 运行时依赖 -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
    <scope>runtime</scope>
</dependency>
```

---

## 5. Maven Profile 配置

Profile 允许针对不同环境使用不同的配置：

```xml
<profiles>
    <profile>
        <id>dev</id>
        <properties>
            <env>development</env>
        </properties>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
    </profile>
    <profile>
        <id>prod</id>
        <properties>
            <env>production</env>
        </properties>
    </profile>
</profiles>
```

激活 Profile 的方式：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 通过命令行激活
mvn clean package -Pprod

# 通过环境变量激活
mvn clean package -Denv=prod
```

---

## 6. 构建插件（Plugin）

Maven 通过插件来实现具体的构建功能。本项目使用了以下插件：

### maven-compiler-plugin

控制 Java 编译器的行为：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <source>11</source>
        <target>11</target>
        <encoding>UTF-8</encoding>
    </configuration>
</plugin>
```

### maven-surefire-plugin

负责执行单元测试：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.0.0-M9</version>
</plugin>
```

### 其他常用插件

| 插件 | 功能 |
|------|------|
| `maven-jar-plugin` | 创建 JAR 包 |
| `maven-source-plugin` | 生成源码包 |
| `maven-javadoc-plugin` | 生成 Javadoc 文档 |
| `maven-shade-plugin` | 创建包含所有依赖的 Fat JAR |
| `maven-assembly-plugin` | 创建自定义格式的分发包 |
| `maven-enforcer-plugin` | 强制执行项目约束规则 |

---

## 7. 项目代码结构说明

本项目遵循 **分层架构** 模式，代码按职责组织在不同的包中：

### model 包 — 数据模型层

`Student.java` 是一个标准的 Java Bean（POJO），包含：
- 私有字段（id, name, age, major）
- Getter/Setter 方法
- `equals()` 和 `hashCode()` 方法
- `toString()` 方法

### service 包 — 业务逻辑层

`StudentService.java` 封装了学生管理的业务逻辑：
- 增删改查操作（CRUD）
- 统计计算功能（平均年龄）
- 按条件过滤功能

### util 包 — 工具类

`MathUtils.java` 提供静态数学工具方法：
- `factorial()` 阶乘计算
- `isPrime()` 质数判断
- `fibonacci()` 斐波那契数列
- `gcd()` / `lcm()` 最大公约数 / 最小公倍数

### exception 包 — 自定义异常

`StudentNotFoundException.java` 是一个自定义运行时异常，用于在找不到学生记录时抛出。

---

## 8. 快速开始

### 前置条件

- JDK 11 或更高版本
- Maven 3.6+ 已安装并配置

### 编译项目

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
cd java/maven-project-structure-demo
mvn compile
```

### 运行测试

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn test
```

### 打包项目

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn clean package
```

### 运行主类

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.maven.MavenStructureDemo"
```

或者使用 `java` 命令直接运行：

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
java -cp target/maven-project-structure-demo-1.0.0.jar com.opendemo.java.maven.MavenStructureDemo
```

---

## 9. 常见问题

### Q1: Maven 编译报编码错误怎么办？

确保 `pom.xml` 中设置了正确的编码：

```xml
<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
```

### Q2: 依赖下载失败怎么办？

检查 Maven 的 `settings.xml` 镜像配置，推荐使用阿里云镜像：

```xml
<mirror>
    <id>aliyun</id>
    <mirrorOf>central</mirrorOf>
    <url>https://maven.aliyun.com/repository/central</url>
</mirror>
```

### Q3: 如何查看依赖树？

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn dependency:tree
```

### Q4: 如何查看有效 POM？

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
mvn help:effective-pom
```

---

## 10. 参考资料

- [Maven 官方文档](https://maven.apache.org/guides/)
- [Maven POM Reference](https://maven.apache.org/pom.html)
- [Maven Standard Directory Layout](https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html)
- [Maven Lifecycle Reference](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)
- [Maven Dependency Scope](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Dependency_Scope)

## 🎯 学习目标

完成本案例学习后，你将能够：

- ✅ 理解本案例涉及的核心概念
- ✅ 掌握相关的配置与命令
- ✅ 能够在本地环境中复现

## 🚀 快速开始

### 运行演示

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
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

🟡 中风险：会修改系统状态、安装软件或启动/停止服务，但影响范围相对可控。
> ⚠️ 生产安全提示：
> - 会修改本地环境或启动服务，建议在测试/开发环境先验证。
> - 注意检查依赖版本、端口占用和目标资源配置。
> - 生产环境执行前请经过变更评审和备份确认。
```bash
# 请根据实际案例替换
./scripts/demo.sh
```
