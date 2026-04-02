# Socket Programming Demo

Socket编程实战演示，使用多种语言实现网络通信。

## 技术栈

- C/C++ Socket
- Python Socket
- Java Socket
- Go net package

## 案例结构

```
socket-programming/
├── c-socket/           # C语言Socket实现
├── python-socket/      # Python Socket实现
├── java-socket/        # Java Socket实现
└── go-socket/          # Go语言实现
```

## 快速开始

### Python Socket示例

```python
# server.py
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(5)

print("Server listening on port 8080...")
while True:
    client, addr = server.accept()
    print(f"Connection from {addr}")
    data = client.recv(1024)
    client.send(b"Hello, Client!")
    client.close()
```

```python
# client.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.send(b"Hello, Server!")
response = client.recv(1024)
print(f"Received: {response.decode()}")
client.close()
```

## 学习要点

1. Socket类型：TCP vs UDP
2. 阻塞与非阻塞IO
3. Select/Poll/Epoll多路复用
4. 并发服务器实现
5. 协议设计与序列化
