# Profiles Demo

多环境配置演示项目，演示Spring Boot的Profile配置。

## 技术栈

- Spring Boot 2.7
- Spring Profiles

## 配置文件

- application.yml: 默认配置
- application-dev.yml: 开发环境
- application-prod.yml: 生产环境

## 激活方式

```bash
java -jar app.jar --spring.profiles.active=prod
```
