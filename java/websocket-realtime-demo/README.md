# WebSocket Realtime Demo

Spring WebSocket实时通信演示项目，演示如何使用WebSocket构建实时聊天应用。

## 技术栈

- Spring Boot 2.7
- Spring WebSocket
- HTML5 WebSocket API

## 项目结构

```
websocket-realtime-demo/
├── src/main/java/com/example/demo/
│   ├── WebSocketDemoApplication.java      # 应用入口
│   ├── config/
│   │   └── WebSocketConfig.java           # WebSocket配置
│   ├── controller/
│   │   └── ChatController.java            # REST控制器
│   ├── handler/
│   │   └── ChatWebSocketHandler.java      # WebSocket处理器
│   └── model/
│       └── ChatMessage.java               # 消息模型
├── src/main/resources/
│   └── static/
│       └── index.html                     # 聊天页面
├── pom.xml
└── README.md
```

## WebSocket简介

### 什么是WebSocket

WebSocket是一种在单个TCP连接上进行全双工通信的协议。特点：
- 双向通信：客户端和服务器可以同时发送消息
- 低延迟：连接建立后无需重复握手
- 轻量级：头部开销小

### WebSocket vs HTTP

| 特性 | HTTP | WebSocket |
|------|------|-----------|
| 通信方式 | 请求-响应 | 双向 |
| 连接 | 短连接 | 长连接 |
| 头部开销 | 大 | 小 |
| 实时性 | 差（需要轮询） | 好（服务器推送） |
| 适用场景 | REST API | 实时应用 |

### WebSocket连接过程

```
客户端                        服务器
  |                             |
  |----- HTTP Upgrade请求 ----->|
  |   Connection: Upgrade       |
  |   Upgrade: websocket        |
  |                             |
  |<---- 101 Switching --------|
  |       Protocols             |
  |                             |
  |==== WebSocket连接建立 =====|
  |                             |
  |<-----> 双向通信 <---------->|
  |                             |
```

## 核心组件说明

### WebSocketConfig - 配置类

```java
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
    
    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(chatWebSocketHandler, "/ws/chat")
                .setAllowedOrigins("*");  // 允许跨域
    }
}
```

### TextWebSocketHandler - 处理器

```java
@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {
    
    // 存储所有会话
    private final Set<WebSocketSession> sessions = new CopyOnWriteArraySet<>();
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        sessions.add(session);
    }
    
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        // 处理消息
        String payload = message.getPayload();
        // 广播给所有连接
        for (WebSocketSession s : sessions) {
            s.sendMessage(new TextMessage(payload));
        }
    }
    
    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        sessions.remove(session);
    }
}
```

## 快速开始

### 1. 启动应用

```bash
mvn spring-boot:run
```

### 2. 打开聊天室

在浏览器中访问：

```
http://localhost:8080
```

### 3. 多用户测试

打开多个浏览器窗口，使用不同昵称登录，即可看到实时聊天效果。

## WebSocket API

### 客户端JavaScript

```javascript
// 创建连接
const ws = new WebSocket('ws://localhost:8080/ws/chat');

// 连接建立
ws.onopen = function() {
    console.log('连接成功');
};

// 接收消息
ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('收到消息:', message);
};

// 连接关闭
ws.onclose = function() {
    console.log('连接关闭');
};

// 发送消息
ws.send(JSON.stringify({
    type: 'CHAT',
    sender: 'user1',
    content: 'Hello'
}));

// 关闭连接
ws.close();
```

### 服务端Java

```java
// 发送消息
session.sendMessage(new TextMessage("Hello"));

// 关闭连接
session.close();
```

## 消息协议

### 消息格式

```json
{
  "type": "CHAT",
  "sender": "用户名",
  "content": "消息内容",
  "timestamp": "2024-01-01T10:00:00"
}
```

### 消息类型

- `JOIN`: 用户加入
- `CHAT`: 普通聊天消息
- `LEAVE`: 用户离开
- `USER_LIST`: 在线用户列表

## 高级特性

### 心跳检测

```javascript
// 客户端心跳
setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'PING' }));
    }
}, 30000);
```

### 重连机制

```javascript
function connect() {
    ws = new WebSocket('ws://localhost:8080/ws/chat');
    
    ws.onclose = function() {
        // 3秒后重连
        setTimeout(connect, 3000);
    };
}
```

### 点对点消息

```java
// 存储用户和会话的映射
private Map<String, WebSocketSession> userSessions = new ConcurrentHashMap<>();

// 发送给特定用户
public void sendToUser(String username, String message) {
    WebSocketSession session = userSessions.get(username);
    if (session != null && session.isOpen()) {
        session.sendMessage(new TextMessage(message));
    }
}
```

## 生产环境建议

### 1. 使用STOMP协议

```java
@Configuration
@EnableWebSocketMessageBroker
public class StompConfig implements WebSocketMessageBrokerConfigurer {
    
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOrigins("*")
                .withSockJS();
    }
    
    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic", "/queue");
        registry.setApplicationDestinationPrefixes("/app");
    }
}
```

### 2. 安全性

```java
@Override
public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
    registry.addHandler(handler, "/ws/chat")
            .setAllowedOrigins("https://trusted-domain.com")
            .addInterceptors(new AuthHandshakeInterceptor());
}
```

### 3. 集群部署

使用Redis或RabbitMQ作为消息代理，实现跨服务器的消息广播。

### 4. 连接限制

```java
@Component
public class ConnectionLimiter extends TextWebSocketHandler {
    
    private final AtomicInteger connections = new AtomicInteger(0);
    private static final int MAX_CONNECTIONS = 10000;
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        if (connections.incrementAndGet() > MAX_CONNECTIONS) {
            session.close(CloseStatus.POLICY_VIOLATION);
            connections.decrementAndGet();
        }
    }
}
```

## WebSocket使用场景

- 实时聊天
- 在线游戏
- 股票行情
- 协同编辑
- 实时通知
- 物联网

## 浏览器兼容性

| 浏览器 | 版本 |
|--------|------|
| Chrome | 16+ |
| Firefox | 11+ |
| Safari | 7+ |
| Edge | 所有版本 |
| IE | 10+ |

## 学习要点

1. WebSocket协议和工作原理
2. 全双工通信的优势
3. Spring WebSocket的使用
4. 连接管理和会话存储
5. 消息广播和点对点发送
6. 心跳检测和重连机制
7. 生产环境的集群部署
