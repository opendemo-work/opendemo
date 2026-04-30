# RestTemplate HTTP客户端演示

> 深入理解 Spring RestTemplate，掌握 GET/POST/PUT/DELETE 请求、超时配置和拦截器

## 🎯 学习目标

- ✅ 掌握 RestTemplate 的核心 HTTP 方法
- ✅ 学会超时、拦截器等高级配置
- ✅ 理解 exchange() 通用请求方法
- ✅ 了解请求头和响应体的处理

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **RestTemplate** | Spring 提供的同步 HTTP 客户端 |
| **HttpEntity** | HTTP 请求/响应实体（包含头和体） |
| **ResponseEntity** | 带状态码的 HTTP 响应 |
| **RequestFactory** | 底层 HTTP 请求工厂 |
| **Interceptor** | 请求拦截器，用于统一处理 |

---

## 🛠️ RestTemplate 方法一览

```
┌────────────────────────────────────────────────────┐
│              RestTemplate 核心方法                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  getForObject(url, class)           GET 获取对象    │
│  getForEntity(url, class)           GET 获取实体    │
│  postForObject(url, req, class)     POST 获取对象   │
│  postForEntity(url, req, class)     POST 获取实体   │
│  put(url, req)                      PUT 更新       │
│  delete(url)                        DELETE 删除    │
│  exchange(url, method, entity, cls) 通用请求       │
│  headForHeaders(url)                HEAD 获取头    │
│  optionsForAllow(url)               OPTIONS 获取   │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. RestTemplate 配置

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    public RestTemplate restTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(5000);
        factory.setReadTimeout(10000);

        RestTemplate restTemplate = new RestTemplate(factory);

        // 添加拦截器
        restTemplate.setInterceptors(List.of((request, body, execution) -> {
            request.getHeaders().add("X-Request-Id", String.valueOf(System.currentTimeMillis()));
            return execution.execute(request, body);
        }));

        return restTemplate;
    }
}
```

### 2. GET 请求

```java
public String getPostById(int id) {
    String url = "https://jsonplaceholder.typicode.com/posts/" + id;
    ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
    return response.getBody();
}
```

### 3. POST 请求

```java
public String createPost(Map<String, Object> postData) {
    String url = "https://jsonplaceholder.typicode.com/posts";
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<Map<String, Object>> entity = new HttpEntity<>(postData, headers);

    ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
    return response.getBody();
}
```

### 4. exchange() 通用方法

```java
public ResponseEntity<String> exchangeRequest(String url, HttpMethod method,
        Map<String, String> headers, String body) {
    HttpHeaders httpHeaders = new HttpHeaders();
    headers.forEach(httpHeaders::add);
    HttpEntity<String> entity = new HttpEntity<>(body, httpHeaders);

    return restTemplate.exchange(url, method, entity, String.class);
}
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/rest-template-demo
mvn spring-boot:run
```

### 2. 测试 API 调用

```bash
# GET 请求示例
curl "https://jsonplaceholder.typicode.com/posts/1"

# POST 请求示例
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"test","body":"content","userId":1}' \
  "https://jsonplaceholder.typicode.com/posts"
```

---

## 📁 项目结构

```
rest-template-demo/
├── src/main/java/com/example/demo/
│   ├── RestTemplateApplication.java          # 应用入口
│   ├── config/
│   │   └── RestTemplateConfig.java           # RestTemplate配置
│   └── service/
│       ├── HttpService.java                  # HTTP基础服务
│       └── ExternalApiService.java           # 外部API调用服务
├── src/test/java/com/example/demo/
│   └── RestTemplateDemoTest.java             # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 HTTP 方法对照

| 方法 | RestTemplate API | HTTP Method |
|------|-----------------|-------------|
| 获取 | `getForObject()` / `getForEntity()` | GET |
| 创建 | `postForObject()` / `postForEntity()` | POST |
| 更新 | `put()` | PUT |
| 删除 | `delete()` | DELETE |
| 通用 | `exchange()` | 任意 |

---

## 🔧 超时配置说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `connectTimeout` | 建立连接超时 | 5000ms |
| `readTimeout` | 读取数据超时 | 10000ms |

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring Cloud Feign](../spring-cloud-feign-demo/) - 声明式 HTTP 客户端
- [Spring MVC Web](../spring-mvc-web-demo/) - REST API

---

*最后更新：2026年4月*
