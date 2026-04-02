# Exception Handling Demo

全局异常处理演示项目，演示Spring Boot的统一异常处理机制。

## 技术栈

- Spring Boot 2.7
- @RestControllerAdvice

## 核心概念

使用@RestControllerAdvice实现全局异常处理，统一返回错误格式。

## 测试接口

```bash
# 资源不存在异常
curl http://localhost:8080/api/users/999

# 业务异常
curl -X POST "http://localhost:8080/api/users?name="

# 系统异常
curl http://localhost:8080/api/users/error
```
