# Filter Interceptor Demo

过滤器拦截器演示项目，演示Filter和Interceptor的使用。

## 技术栈

- Spring Boot 2.7
- Filter
- HandlerInterceptor

## Filter vs Interceptor

| 特性 | Filter | Interceptor |
|------|--------|-------------|
| 作用范围 | Servlet容器 | Spring MVC |
| 执行时机 | 请求前后 | Controller前后 |
| 获取Controller信息 | 否 | 是 |

## 执行顺序

Filter -> Interceptor -> Controller -> Interceptor -> Filter
