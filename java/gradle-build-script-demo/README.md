<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Gradle 构建脚本演示

## 项目简介

本项目是一个 Gradle 构建脚本演示，通过一个简单的任务管理应用来展示 Gradle 构建工具的核心概念。项目同时包含 `build.gradle`（主要构建文件）和 `pom.xml`（兼容性构建文件），帮助开发者对比理解 Gradle 和 Maven 两种主流 Java 构建工具的差异。

通过本项目，你将掌握 Gradle 的 DSL 语法、Task 机制、依赖管理、插件系统以及多项目构建等核心概念。

---

## 目录

1. [Gradle 与 Maven 对比](#1-gradle-与-maven-对比)
2. [build.gradle 语法详解](#2-buildgradle-语法详解)
3. [Gradle Task 机制](#3-gradle-task-机制)
4. [依赖管理](#4-依赖管理)
5. [Gradle 插件系统](#5-gradle-插件系统)
6. [多项目构建（Multi-Project Build）](#6-多项目构建multi-project-build)
7. [项目代码结构说明](#7-项目代码结构说明)
8. [快速开始](#8-快速开始)
9. [常见问题](#9-常见问题)
10. [参考资料](#10-参考资料)

---

## 1. Gradle 与 Maven 对比

Gradle 和 Maven 是 Java 生态中最流行的两个构建工具。以下是核心对比：

### 构建脚本语言

| 特性 | Gradle | Maven |
|------|--------|-------|
| 脚本语言 | Groovy / Kotlin DSL | XML |
| 可编程性 | 完全可编程 | 声明式 |
| 可读性 | 高 | 中等 |
| 灵活性 | 非常灵活 | 约定驱动 |

### 构建性能

| 特性 | Gradle | Maven |
|------|--------|-------|
| 增量构建 | ✅ 只编译变更的部分 | ❌ 全量构建 |
| 构建缓存 | ✅ 本地 + 远程缓存 | ❌ 无缓存 |
| 并行构建 | ✅ 天然支持 | ⚠️ 需要配置 |
| Daemon 进程 | ✅ 常驻后台加速 | ❌ 每次启动新 JVM |

### 依赖管理

| 特性 | Gradle | Maven |
|------|--------|-------|
| 依赖解析策略 | 最短路径 + 最新版本 | 最短路径 + 最近声明 |
| 版本冲突处理 | 自动解决 | 需手动排除 |
| 动态版本 | ✅ 支持 | ⚠️ 有限支持 |
| BOM 支持 | ✅ `platform()` | ✅ `<dependencyManagement>` |

### 选择建议

- **新项目推荐 Gradle**：构建速度快、脚本灵活、Android 官方推荐
- **企业级项目可用 Maven**：成熟稳定、团队熟悉度高、生态完善
- **混合使用**：本项目同时提供两种构建文件，方便对比学习

---

## 2. build.gradle 语法详解

本项目的 `build.gradle` 文件结构如下：

### 插件声明

```groovy
plugins {
    id 'java'
    id 'application'
}
```

- `java` 插件提供 Java 编译、测试、打包功能
- `application` 插件提供运行主类的 `run` 任务

### 项目坐标

```groovy
group = 'com.opendemo.java'
version = '1.0.0'
sourceCompatibility = '11'
targetCompatibility = '11'
```

### 仓库配置

```groovy
repositories {
    mavenCentral()                          // Maven Central 仓库
    maven { url 'https://maven.aliyun.com/repository/public' }  // 阿里云镜像
    google()                                // Google 仓库（Android）
    mavenLocal()                            // 本地 Maven 仓库
}
```

### 依赖声明

```groovy
dependencies {
    implementation 'org.slf4j:slf4j-api:2.0.7'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.9.2'
}
```

Gradle 的依赖配置（Configurations）对应 Maven 的 Scope：

| Gradle Configuration | Maven Scope | 说明 |
|---------------------|-------------|------|
| `implementation` | `compile` | 编译和运行时需要 |
| `api` | `compile`（传递依赖） | 编译、运行时、且传递给依赖方 |
| `compileOnly` | `provided` | 仅编译时需要 |
| `runtimeOnly` | `runtime` | 仅运行时需要 |
| `testImplementation` | `test` | 仅测试编译和运行时需要 |
| `testCompileOnly` | `test`（provided） | 仅测试编译时需要 |
| `testRuntimeOnly` | `test`（runtime） | 仅测试运行时需要 |

---

## 3. Gradle Task 机制

Task 是 Gradle 构建的核心概念。每个 Task 包含一组动作（Action），按顺序执行。

### Task 基本操作

```groovy
// 定义 Task
tasks.register('hello') {
    doLast {
        println 'Hello, Gradle!'
    }
}

// 带依赖的 Task
tasks.register('buildAndHello') {
    dependsOn 'build'
    doLast {
        println 'Build completed!'
    }
}
```

### Task 类型

```groovy
// Copy 类型 Task
tasks.register('copyDocs', Copy) {
    from 'src/docs'
    into 'build/docs'
}

// Delete 类型 Task
tasks.register('cleanTemp', Delete) {
    delete 'temp'
}

// Exec 类型 Task
tasks.register('runScript', Exec) {
    commandLine 'python', 'scripts/build.py'
}
```

### 自定义 Task

```groovy
tasks.register('printBuildInfo') {
    group = 'Custom'
    description = '打印项目构建信息'
    doLast {
        println "Project: ${project.name}"
        println "Version: ${project.version}"
        println "Build Dir: ${layout.buildDirectory.get()}"
    }
}
```

### Task 依赖关系

```groovy
tasks.register('taskA') {
    doLast { println 'Task A' }
}

tasks.register('taskB') {
    dependsOn 'taskA'
    doLast { println 'Task B (after A)' }
}

tasks.register('taskC') {
    dependsOn 'taskA', 'taskB'
    doLast { println 'Task C (after A and B)' }
}
```

### 常用内置 Task

| Task | 说明 |
|------|------|
| `compileJava` | 编译 Java 源代码 |
| `compileTestJava` | 编译测试代码 |
| `test` | 执行单元测试 |
| `jar` | 打包 JAR 文件 |
| `clean` | 清理构建输出 |
| `build` | 完整构建 |
| `run` | 运行应用程序 |

---

## 4. 依赖管理

### 依赖版本管理

推荐使用版本目录（Version Catalog）统一管理版本：

```groovy
// gradle/libs.versions.toml
[versions]
junit = "5.9.2"
slf4j = "2.0.7"

[libraries]
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter", version.ref = "junit" }
slf4j-api = { module = "org.slf4j:slf4j-api", version.ref = "slf4j" }
```

### 依赖排除

```groovy
implementation('com.example:library:1.0') {
    exclude group: 'org.unwanted', module: 'unwanted-module'
}
```

### 强制版本

```groovy
configurations.all {
    resolutionStrategy {
        force 'com.google.guava:guava:32.1.1-jre'
    }
}
```

### 平台依赖（BOM）

```groovy
implementation platform('org.springframework.boot:spring-boot-dependencies:2.7.12')
implementation 'org.springframework.boot:spring-boot-starter-web'
```

---

## 5. Gradle 插件系统

### 核心 Java 插件

```groovy
plugins {
    id 'java'
}
```

Java 插件自动创建以下 SourceSet：

| SourceSet | 目录 | 说明 |
|-----------|------|------|
| `main` | `src/main/java` | 主源代码 |
| `test` | `src/test/java` | 测试代码 |

### Application 插件

```groovy
plugins {
    id 'application'
}

application {
    mainClass = 'com.opendemo.java.gradle.GradleBuildDemo'
    applicationDefaultJvmArgs = ['-Xms256m', '-Xmx512m']
}
```

### 常用第三方插件

| 插件 | 功能 |
|------|------|
| `com.github.johnrengelman.shadow` | 创建 Fat JAR |
| `org.springframework.boot` | Spring Boot 支持 |
| `com.diffplug.spotless` | 代码格式化 |
| `org.sonarqube` | 代码质量分析 |
| `com.google.protobuf` | Protobuf 编译 |
| `org.flywaydb.flyway` | 数据库迁移 |

---

## 6. 多项目构建（Multi-Project Build）

### 项目结构

```
multi-project-root/
├── settings.gradle
├── build.gradle                  (根项目配置)
├── shared/                       (子项目)
│   └── build.gradle
├── api/                          (子项目)
│   └── build.gradle
└── app/                          (子项目)
    └── build.gradle
```

### settings.gradle

```groovy
rootProject.name = 'multi-project-root'
include 'shared', 'api', 'app'
```

### 子项目依赖

```groovy
// app/build.gradle
dependencies {
    implementation project(':shared')
    implementation project(':api')
}
```

### 公共配置

```groovy
// 根 build.gradle
subprojects {
    apply plugin: 'java'
    repositories {
        mavenCentral()
    }
    dependencies {
        implementation 'org.slf4j:slf4j-api:2.0.7'
    }
}
```

---

## 7. 项目代码结构说明

本项目模拟了一个任务管理系统，代码按职责分层：

### model/Task.java

任务实体类，包含：
- UUID 自动生成 ID
- 标题、描述、状态字段
- 自动更新时间戳

### service/TaskService.java

业务逻辑层，提供：
- 任务创建、查询、完成、取消操作
- 按状态过滤任务
- 异常处理

### repository/TaskRepository.java

内存数据存储，使用 `ConcurrentHashMap` 实现：
- CRUD 操作
- 按条件查询
- 线程安全

---

## 8. 快速开始

### 前置条件

- JDK 11 或更高版本
- Gradle 8.x 或使用项目自带的 Gradle Wrapper

### 使用 Gradle 构建

```bash
cd java/gradle-build-script-demo

# 编译项目
./gradlew compileJava

# 运行测试
./gradlew test

# 打包项目
./gradlew build

# 运行应用
./gradlew run

# 查看所有 Task
./gradlew tasks

# 打印构建信息（自定义 Task）
./gradlew printBuildInfo
```

### 使用 Maven 构建（兼容模式）

```bash
mvn clean compile
mvn test
mvn package
```

---

## 9. 常见问题

### Q1: Gradle Wrapper 是什么？

Gradle Wrapper 是一个脚本，允许在没有安装 Gradle 的机器上运行 Gradle 构建。它会自动下载指定版本的 Gradle。

```bash
# 生成 Wrapper
gradle wrapper --gradle-version 8.1.1

# 使用 Wrapper
./gradlew build        # Linux/macOS
gradlew.bat build      # Windows
```

### Q2: 如何加速 Gradle 构建？

```properties
# gradle.properties
org.gradle.daemon=true          # 启用 Daemon
org.gradle.parallel=true        # 并行构建
org.gradle.caching=true         # 构建缓存
org.gradle.jvmargs=-Xmx2g       # 增大 JVM 内存
```

### Q3: 如何查看依赖树？

```bash
./gradlew dependencies
./gradlew :app:dependencies     # 查看特定子项目
```

### Q4: build.gradle 和 settings.gradle 的区别？

- `settings.gradle`：声明包含哪些子项目，仅在根项目存在
- `build.gradle`：定义构建逻辑和配置，每个项目（包括子项目）都有

---

## 10. 参考资料

- [Gradle 官方文档](https://docs.gradle.org/)
- [Gradle Build Language Reference](https://docs.gradle.org/current/dsl/)
- [Gradle vs Maven](https://docs.gradle.org/current/userguide/migrating_from_maven.html)
- [Gradle Plugin Portal](https://plugins.gradle.org/)
- [Gradle Version Catalog](https://docs.gradle.org/current/userguide/platforms.html)

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
