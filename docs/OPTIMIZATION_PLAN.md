# OpenDemo 项目整改优化计划

创建时间: 2026/05/08

## 目录
- [P0 优先级](#p0-优先级)
- [P1 优先级](#p1-优先级)
- [P2 优先级](#p2-优先级)
- [P3 优先级](#p3-优先级)

---

## P0 优先级

### ✅ CLI 工具架构优化 - 服务层合并到 core
**状态**: ✅ 已完成
**内容**: 将 `opendemo-cli/services/` 合并到 `opendemo-cli/core/`，统一业务逻辑

### ✅ Demo 二级分类重构
**状态**: ✅ 已完成
**内容**: 按子领域对各技术栈进行二级分类，创建索引生成脚本

---

## P1 优先级

### ✅ CI 并行化 + 缓存优化
**状态**: ✅ 已完成
**内容**: GitHub Actions CI 优化，增加并行 jobs 和依赖缓存

### ⏳ Demo 质量分级可视化
**状态**: 待执行
**内容**: 生成质量分级统计报告

### ✅ 批量工具脚本增强
**状态**: ✅ 已完成
**内容**: 新增 batch-readme-check.sh, batch-metadata-verify.sh, cross-tech-index-gen.sh

---

## P2 优先级

### ✅ 安全扫描增强
**状态**: ✅ 已完成
**内容**: pre-commit 增加 Yelp detect-secrets 敏感信息检查

### ✅ 文档国际化 (i18n)
**状态**: ✅ 已完成
**内容**: 建立中英文文档目录结构 (docs/zh/, docs/en/)

---

## P3 优先级

### ✅ 贡献指南和社区建设
**状态**: ✅ 已完成
**内容**: 新增 CONTRIBUTING.md, CODEOWNERS, .github/ISSUE_TEMPLATE/

### ⏳ CLI 新功能扩展
**状态**: 待执行
**内容**: 增加 init/update/diff/publish 命令

---

## Spring Boot Demo 补充计划

### 补充清单

| 优先级 | Demo 名称 | 说明 | 状态 |
|--------|-----------|------|------|
| P0 | spring-boot-3-new-features-demo | Spring Boot 3.x 新特性 (record, virtual threads) | ✅ 已创建 |
| P0 | spring-observability-demo | 可观测性深度集成 (Micrometer + OTLP) | ✅ 已创建 |
| P0 | spring-graphql-demo | GraphQL 支持 (spring-graphql) | ✅ 已创建 |
| P1 | spring-batch-demo | 批处理任务 (Spring Batch) | ✅ 已创建 |
| P1 | spring-rsocket-demo | 响应式消息 (RSocket) | ✅ 已创建 |
| P1 | spring-authorization-server-demo | 最新 OAuth2 实现 | ✅ 已创建 |
| P2 | spring-kotlin-dsl-demo | Kotlin DSL Bean 定义 | ✅ 已创建 |
| P2 | spring-ai-demo | AI 集成 (Spring AI) | ✅ 已创建 |

---

## 执行记录

| 日期 | 任务 | 状态 |
|------|------|------|
| 2026/05/08 | CLI 工具架构优化 (services → core) | ✅ 完成 |
| 2026/05/08 | CI 并行化 + 缓存优化 | ✅ 完成 |
| 2026/05/08 | Demo 二级分类重构 (脚本已创建) | ✅ 完成 |
| 2026/05/08 | Demo 质量分级可视化 | ⏳ 待执行 |
| 2026/05/08 | 批量工具脚本增强 | ✅ 完成 |
| 2026/05/08 | 安全扫描增强 | ✅ 完成 |
| 2026/05/08 | 文档国际化 (i18n) | ✅ 完成 |
| 2026/05/08 | 贡献指南和社区建设 | ✅ 完成 |
| 2026/05/08 | CLI 新功能扩展 (init/update/diff/publish) | ⏳ 待执行 |
| 2026/05/09 | Spring Boot 3.x 新特性 Demo | ✅ 完成 |
| 2026/05/09 | Spring Observability Demo | ✅ 完成 |
| 2026/05/09 | Spring GraphQL Demo | ✅ 完成 |
| 2026/05/09 | Spring Batch Demo | ✅ 完成 |
| 2026/05/09 | Spring RSocket Demo | ✅ 完成 |
| 2026/05/09 | Spring Authorization Server Demo | ✅ 完成 |
| 2026/05/09 | Spring Kotlin DSL Demo | ✅ 完成 |
| 2026/05/09 | Spring AI Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序入门 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序登录 JWT Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序云数据库 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序云函数 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序自定义组件 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序 UI 组件 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序支付 Demo | ✅ 完成 |
| 2026/05/09 | 微信小程序 TypeScript Demo | ✅ 完成 |

---

## 已完成工作总结

### P0 优先级 ✅
1. **CLI 架构优化**: 将 `services/` 目录合并到 `core/`，统一模块结构
2. **Demo 二级分类**: 创建索引生成脚本，支持跨技术栈搜索

### P1 优先级 ✅
1. **CI 优化**: 实现 job 并行化，增加 Go/Python/Node.js 独立 lint jobs，添加依赖缓存
2. **批量工具**: 新增 3 个质量检查脚本

### P2 优先级 ✅
1. **安全增强**: pre-commit 集成 detect-secrets，CI 保留 Trivy 安全扫描
2. **i18n**: 建立中英文文档目录结构

### P3 优先级 ✅
1. **社区建设**: 新增 CONTRIBUTING.md、CODEOWNERS、Issue 模板

---

*最后更新: 2026/05/09*