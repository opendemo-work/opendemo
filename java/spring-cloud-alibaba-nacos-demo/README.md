# Spring Cloud Alibaba Nacos Demo

Spring Cloud Alibaba Nacos服务注册与配置管理演示项目。

## 什么是Nacos

Nacos（Dynamic Naming and Configuration Service）是阿里巴巴开源的动态服务发现、配置管理和服务管理平台。它提供：
- **服务注册与发现**：支持DNS和RPC服务发现
- **动态配置管理**：支持配置的动态推送
- **服务健康监测**：支持服务的健康检查

## 与Eureka对比

| 特性 | Nacos | Eureka |
|------|-------|--------|
| 服务发现 | ✅ | ✅ |
| 配置管理 | ✅ | ❌ |
| 健康检查 | 多种方式 | 客户端心跳 |
| 一致性 | AP+CP | AP |
| 社区活跃度 | 高（国内主流） | 低（已停更） |

## 技术栈

- Spring Boot 2.7
- Spring Cloud Alibaba 2021.0.5.0
- Nacos Server 2.x

## 项目结构

```
spring-cloud-alibaba-nacos-demo/
├── src/main/java/com/example/demo/
│   ├── NacosDemoApplication.java      # 应用入口
│   └── controller/
│       └── ConfigController.java      # 配置管理
├── src/main/resources/
│   └── bootstrap.yml                  # Nacos配置
├── pom.xml
└── README.md
```

## 快速开始

### 1. 启动Nacos Server

```bash
# 下载Nacos
curl -O https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.tar.gz
tar -xzf nacos-server-2.2.3.tar.gz
cd nacos/bin

# 单机模式启动
sh startup.sh -m standalone

# 访问Nacos控制台
open http://localhost:8848/nacos
# 默认账号密码: nacos/nacos
```

### 2. 配置中心添加配置

1. 登录Nacos控制台
2. 进入 **配置管理** → **配置列表**
3. 点击 **+ 新建配置**
4. 填写信息：
   - Data ID: `nacos-demo-dev.yaml`
   - Group: `DEFAULT_GROUP`
   - 配置格式: `YAML`
   - 配置内容:
```yaml
user:
  name: NacosUser
  age: 25
app:
  message: Hello from Nacos Config Center!
```

### 3. 启动应用

```bash
mvn spring-boot:run
```

### 4. 验证服务注册

```bash
# 查看服务是否注册成功
curl http://localhost:8080/config

# 响应示例
{
  "user.name": "NacosUser",
  "user.age": 25,
  "app.message": "Hello from Nacos Config Center!",
  "source": "Nacos Config Center"
}
```

### 5. 验证配置动态刷新

1. 在Nacos控制台修改配置
2. 修改 `app.message` 的值
3. 无需重启应用，直接访问：
```bash
curl http://localhost:8080/config/message
```
4. 可以看到配置已动态更新

## 核心注解说明

### @EnableDiscoveryClient
```java
@SpringBootApplication
@EnableDiscoveryClient  // 启用Nacos服务发现
public class NacosDemoApplication { }
```

### @RefreshScope
```java
@RestController
@RefreshScope  // 支持配置动态刷新
public class ConfigController {
    @Value("${app.message}")
    private String appMessage;
}
```

## 配置详解

### bootstrap.yml
```yaml
spring:
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848    # Nacos服务器地址
        namespace: public              # 命名空间
        group: DEFAULT_GROUP           # 分组
      config:
        server-addr: localhost:8848    # 配置中心地址
        file-extension: yaml           # 配置文件格式
        refresh-enabled: true          # 启用动态刷新
```

## 多环境配置

### 命名空间隔离
```
namespace: dev     # 开发环境
namespace: test    # 测试环境  
namespace: prod    # 生产环境
```

### Group分组
```
group: DEFAULT_GROUP    # 默认组
group: PAY_GROUP        # 支付服务组
group: ORDER_GROUP      # 订单服务组
```

## 服务调用

Nacos集成了Ribbon实现客户端负载均衡：

```java
@Autowired
private RestTemplate restTemplate;

@GetMapping("/call/{service}")
public String callService(@PathVariable String service) {
    // 通过服务名调用
    return restTemplate.getForObject(
        "http://" + service + "/hello", 
        String.class
    );
}
```

## 学习要点

1. Nacos架构设计（注册中心+配置中心）
2. 服务注册与发现的原理
3. 配置动态刷新的实现机制
4. 多环境隔离方案
5. 与Spring Cloud生态的集成

## 参考

- [Nacos官方文档](https://nacos.io/zh-cn/docs/what-is-nacos.html)
- [Spring Cloud Alibaba](https://github.com/alibaba/spring-cloud-alibaba)
