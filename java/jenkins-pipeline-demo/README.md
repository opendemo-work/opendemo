<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# Jenkins Pipeline CI/CD 流水线演示

## 项目简介

本项目是一个 Jenkins Pipeline CI/CD 流水线演示，通过模拟 Jenkins 构建过程来展示 CI/CD（持续集成/持续部署）的核心概念。项目包含声明式 Pipeline（`Jenkinsfile`）和脚本式 Pipeline（`Jenkinsfile.scripted`）两种语法，以及一个 Java 模拟构建管理系统。

通过本项目，你将掌握 Jenkins Pipeline 的两种语法风格、流水线阶段设计、构建代理（Agent）配置、环境变量管理、条件部署等核心概念。

---

## 目录

1. [CI/CD 基本概念](#1-cicd-基本概念)
2. [Jenkins Pipeline 语法](#2-jenkins-pipeline-语法)
3. [声明式 Pipeline 详解](#3-声明式-pipeline-详解)
4. [脚本式 Pipeline 详解](#4-脚本式-pipeline-详解)
5. [Pipeline 阶段设计](#5-pipeline-阶段设计)
6. [Agent 与环境配置](#6-agent-与环境配置)
7. [项目代码结构说明](#7-项目代码结构说明)
8. [快速开始](#8-快速开始)
9. [常见问题](#9-常见问题)
10. [参考资料](#10-参考资料)

---

## 1. CI/CD 基本概念

### 什么是 CI/CD？

CI/CD 是现代软件开发中的核心实践：

| 概念 | 全称 | 说明 |
|------|------|------|
| **CI** | Continuous Integration（持续集成） | 开发者频繁合并代码到主分支，每次合并自动触发构建和测试 |
| **CD** | Continuous Delivery（持续交付） | 代码通过所有测试后自动准备好发布，但需要手动触发部署 |
| **CD** | Continuous Deployment（持续部署） | 代码通过所有测试后自动部署到生产环境，无需人工干预 |

### CI/CD 流程

```
代码提交 → 自动构建 → 自动测试 → 代码质量检查 → 自动打包 → 自动部署
   ↑                                                          |
   └──────────── 失败时快速反馈 ←─────────────────────────────┘
```

### CI/CD 的好处

| 好处 | 说明 |
|------|------|
| **快速反馈** | 代码问题在提交后几分钟内被发现 |
| **降低风险** | 小批量、频繁部署比大批量、偶尔部署更安全 |
| **一致性** | 自动化流程消除人为错误 |
| **可追溯性** | 每次构建都有完整记录 |
| **快速交付** | 从代码到部署全自动化 |

---

## 2. Jenkins Pipeline 语法

Jenkins Pipeline 提供两种语法风格：

### 对比

| 特性 | 声明式 Pipeline | 脚本式 Pipeline |
|------|----------------|----------------|
| 语法结构 | 结构化、声明式 | 灵活、过程式 |
| 学习曲线 | 低 | 较高 |
| 可读性 | 高 | 中等 |
| 灵活性 | 有限制 | 完全灵活 |
| 错误处理 | `post` 块 | `try-catch` |
| 推荐场景 | 标准流水线 | 复杂逻辑 |

### 文件命名

- `Jenkinsfile`：Jenkins 默认识别的 Pipeline 定义文件
- 放在项目根目录，与源代码一起版本管理（Pipeline as Code）

---

## 3. 声明式 Pipeline 详解

本项目的 `Jenkinsfile` 采用声明式语法：

```groovy
pipeline {
    agent any                              // 构建代理

    environment {                          // 环境变量
        APP_NAME = 'jenkins-pipeline-demo'
    }

    stages {                               // 构建阶段
        stage('Build') {
            steps {
                sh 'mvn clean compile'     // 构建步骤
            }
        }
    }

    post {                                 // 后置处理
        success { echo '成功!' }
        failure { echo '失败!' }
    }
}
```

### 核心语法元素

#### agent（代理）

```groovy
agent any                    // 在任何可用节点执行
agent none                   // 不分配节点（stage 级别分配）
agent { label 'docker' }     // 在带 docker 标签的节点执行
agent {
    docker {
        image 'maven:3.9-eclipse-temurin-11'
        args '-v $HOME/.m2:/root/.m2'
    }
}
```

#### environment（环境变量）

```groovy
environment {
    APP_NAME = 'my-app'
    VERSION = "${env.BUILD_ID}"
    DEPLOY_ENV = credentials('deploy-env')    // 从 Jenkins 凭据中获取
}
```

#### when（条件判断）

```groovy
when { branch 'main' }                    // 仅在 main 分支执行
when { environment name: 'DEPLOY', value: 'prod' }
when { expression { return env.BUILD_ID.toInteger() > 10 } }
```

#### post（后置处理）

```groovy
post {
    always {            // 无论成功失败都执行
        cleanWs()
    }
    success {           // 构建成功时执行
        echo 'Deploy success!'
    }
    failure {           // 构建失败时执行
        echo 'Build failed!'
    }
    unstable {          // 构建不稳定时执行
        echo 'Build unstable!'
    }
}
```

---

## 4. 脚本式 Pipeline 详解

本项目的 `Jenkinsfile.scripted` 采用脚本式语法：

```groovy
node {
    try {
        stage('Build') {
            sh 'mvn clean compile'
        }
        stage('Test') {
            sh 'mvn test'
        }
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        cleanWs()
    }
}
```

### 关键区别

| 声明式 | 脚本式 |
|--------|--------|
| `pipeline {}` 包裹 | `node {}` 包裹 |
| `stages { stage() {} }` | 直接使用 `stage('name') {}` |
| `post {}` 块 | `try-catch-finally` |
| `environment {}` 块 | `def var = value` |
| `agent` 声明 | `node` / `label` |

---

## 5. Pipeline 阶段设计

### 标准阶段设计

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Checkout │ → │  Build   │ → │   Test   │ → │ Package  │ → │  Deploy  │
│  检出代码 │   │  编译项目 │   │  运行测试 │   │  打包发布 │   │  部署上线 │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### 各阶段职责

| 阶段 | 职责 | 命令 |
|------|------|------|
| **Checkout** | 从 SCM 检出代码 | `checkout scm` |
| **Build** | 编译源代码 | `mvn compile` |
| **Test** | 执行单元测试和集成测试 | `mvn test` |
| **Package** | 打包为可部署产物 | `mvn package` |
| **Deploy** | 部署到目标环境 | `mvn deploy` 或自定义脚本 |

### 并行阶段

```groovy
stage('Parallel Tests') {
    parallel {
        stage('Unit Tests') {
            steps { sh 'mvn test' }
        }
        stage('Integration Tests') {
            steps { sh 'mvn verify -Pintegration' }
        }
        stage('Code Quality') {
            steps { sh 'mvn sonar:sonar' }
        }
    }
}
```

### 手动确认

```groovy
stage('Deploy to Production') {
    input {
        message "确认部署到生产环境？"
        ok "确认部署"
    }
    steps {
        sh './deploy.sh production'
    }
}
```

---

## 6. Agent 与环境配置

### Agent 类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| `any` | 任意可用节点 | 简单项目 |
| `label` | 指定标签节点 | 按环境分配 |
| `docker` | Docker 容器 | 隔离构建环境 |
| `kubernetes` | K8s Pod | 动态扩缩容 |

### Docker Agent 示例

```groovy
pipeline {
    agent {
        docker {
            image 'maven:3.9-eclipse-temurin-11'
            args '-v $HOME/.m2:/root/.m2 -v $HOME/.gradle:/root/.gradle'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

### 工具配置

```groovy
tools {
    maven 'Maven 3.9'
    jdk 'JDK 11'
    gradle 'Gradle 8.1'
}
```

### 环境变量来源

| 来源 | 说明 | 示例 |
|------|------|------|
| `environment` 块 | Pipeline 内定义 | `APP_NAME = 'demo'` |
| Jenkins 全局配置 | Manage Jenkins 配置 | `JAVA_HOME` |
| `credentials()` | Jenkins 凭据管理 | `DB_PASSWORD = credentials('db-pwd')` |
| 内置变量 | Jenkins 自动提供 | `env.BUILD_ID`, `env.BRANCH_NAME` |

---

## 7. 项目代码结构说明

### Jenkinsfile（声明式）

包含完整的五个阶段：Checkout → Build → Test → Package → Deploy，使用 `when` 条件控制仅 `main` 分支执行部署。

### Jenkinsfile.scripted（脚本式）

使用 `try-catch-finally` 结构实现相同的构建流程，展示更灵活的错误处理方式。

### model/BuildInfo.java

构建信息模型类：
- 构建ID、项目名、分支
- 构建状态（RUNNING/SUCCESS/FAILURE）
- 内嵌 `StageInfo` 类记录每个阶段

### service/BuildService.java

构建管理服务：
- 启动构建、执行阶段、完成/失败构建
- 构建历史查询

---

## 8. 快速开始

### 前置条件

- JDK 11 或更高版本
- Maven 3.6+ 已安装并配置
- Jenkins（可选，用于实际运行 Pipeline）

### 编译项目

```bash
cd java/jenkins-pipeline-demo
mvn clean compile
```

### 运行测试

```bash
mvn test
```

### 运行主类

```bash
mvn exec:java -Dexec.mainClass="com.opendemo.java.jenkins.JenkinsPipelineDemo"
```

### 在 Jenkins 中运行

1. 创建 Jenkins Pipeline 任务
2. 配置 SCM 指向本项目仓库
3. Script Path 设置为 `Jenkinsfile`
4. 触发构建

---

## 9. 常见问题

### Q1: Jenkinsfile 语法错误如何调试？

使用 Jenkins 的 **Pipeline Syntax** 页面生成代码片段，或使用 Blue Ocean 可视化编辑器。

### Q2: 如何在 Pipeline 中使用共享库？

```groovy
@Library('my-shared-library') _
pipeline { ... }
```

### Q3: 如何处理多环境部署？

```groovy
stage('Deploy') {
    when {
        anyOf {
            branch 'main'
            branch 'staging'
        }
    }
    steps {
        script {
            if (env.BRANCH_NAME == 'main') {
                sh './deploy.sh production'
            } else {
                sh './deploy.sh staging'
            }
        }
    }
}
```

### Q4: 声明式和脚本式如何选择？

- 优先使用**声明式**：结构清晰、易于维护
- 需要复杂逻辑时使用**脚本式**：如循环、条件判断、异常处理

---

## 10. 参考资料

- [Jenkins Pipeline 官方文档](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Jenkins Shared Libraries](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
- [Pipeline as Code](https://www.jenkins.io/doc/book/pipeline-as-code/)
- [Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)

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
