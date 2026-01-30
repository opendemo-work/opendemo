#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Socket 网络编程完整示例
演示 TCP/UDP Socket 编程基础
"""

import socket
import threading
import time
import json
from typing import Tuple, Optional


# ============ 1. Socket 基础 ============
print("=" * 50)
print("1. Socket 基础")
print("=" * 50)

print("""
Socket 类型:
- socket.SOCK_STREAM: TCP (可靠、面向连接)
- socket.SOCK_DGRAM: UDP (不可靠、无连接)

地址族:
- socket.AF_INET: IPv4
- socket.AF_INET6: IPv6
""")

# 获取主机信息
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"主机名: {hostname}")
print(f"IP地址: {ip_address}")


# ============ 2. 简单 TCP 服务器/客户端 ============
print("\n" + "=" * 50)
print("2. TCP 服务器/客户端示例")
print("=" * 50)

def tcp_server(host: str, port: int, stop_event: threading.Event):
    """简单TCP服务器"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(1.0)  # 设置超时以便检查停止事件
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"  [服务器] 监听 {host}:{port}")
        
        while not stop_event.is_set():
            try:
                client_socket, address = server_socket.accept()
                print(f"  [服务器] 接受连接: {address}")
                
                # 接收数据
                data = client_socket.recv(1024)
                print(f"  [服务器] 收到: {data.decode()}")
                
                # 发送响应
                response = f"Echo: {data.decode()}"
                client_socket.send(response.encode())
                
                client_socket.close()
            except socket.timeout:
                continue
    finally:
        server_socket.close()
        print("  [服务器] 已关闭")

def tcp_client(host: str, port: int, message: str) -> str:
    """简单TCP客户端"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"  [客户端] 连接到 {host}:{port}")
        
        # 发送数据
        client_socket.send(message.encode())
        print(f"  [客户端] 发送: {message}")
        
        # 接收响应
        response = client_socket.recv(1024)
        print(f"  [客户端] 收到: {response.decode()}")
        
        return response.decode()
    finally:
        client_socket.close()

# 运行示例
stop_event = threading.Event()
server_thread = threading.Thread(target=tcp_server, args=("127.0.0.1", 9999, stop_event))
server_thread.start()

time.sleep(0.5)  # 等待服务器启动

tcp_client("127.0.0.1", 9999, "Hello, Server!")

stop_event.set()
server_thread.join()


# ============ 3. UDP 示例 ============
print("\n" + "=" * 50)
print("3. UDP 服务器/客户端示例")
print("=" * 50)

def udp_server(host: str, port: int, stop_event: threading.Event):
    """UDP服务器"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.settimeout(1.0)
    server_socket.bind((host, port))
    print(f"  [UDP服务器] 监听 {host}:{port}")
    
    try:
        while not stop_event.is_set():
            try:
                data, address = server_socket.recvfrom(1024)
                print(f"  [UDP服务器] 收到来自 {address}: {data.decode()}")
                
                response = f"UDP Echo: {data.decode()}"
                server_socket.sendto(response.encode(), address)
            except socket.timeout:
                continue
    finally:
        server_socket.close()
        print("  [UDP服务器] 已关闭")

def udp_client(host: str, port: int, message: str) -> str:
    """UDP客户端"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5.0)
    
    try:
        client_socket.sendto(message.encode(), (host, port))
        print(f"  [UDP客户端] 发送: {message}")
        
        data, _ = client_socket.recvfrom(1024)
        print(f"  [UDP客户端] 收到: {data.decode()}")
        return data.decode()
    finally:
        client_socket.close()

stop_event = threading.Event()
server_thread = threading.Thread(target=udp_server, args=("127.0.0.1", 9998, stop_event))
server_thread.start()

time.sleep(0.5)
udp_client("127.0.0.1", 9998, "Hello, UDP!")

stop_event.set()
server_thread.join()


# ============ 4. 多客户端 TCP 服务器 ============
print("\n" + "=" * 50)
print("4. 多客户端 TCP 服务器")
print("=" * 50)

class MultiClientServer:
    """支持多客户端的TCP服务器"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
    
    def handle_client(self, client_socket: socket.socket, address: Tuple):
        """处理单个客户端"""
        print(f"  处理客户端: {address}")
        try:
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break
                response = f"[{address}] Echo: {data.decode()}"
                client_socket.send(response.encode())
        except Exception as e:
            print(f"  客户端错误: {e}")
        finally:
            client_socket.close()
            print(f"  客户端断开: {address}")
    
    def start(self):
        """启动服务器"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1.0)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"  多客户端服务器启动于 {self.host}:{self.port}")
    
    def accept_connections(self, duration: float = 2.0):
        """接受连接一段时间"""
        start = time.time()
        while time.time() - start < duration and self.running:
            try:
                client_socket, address = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.daemon = True
                thread.start()
                self.clients.append(thread)
            except socket.timeout:
                continue
    
    def stop(self):
        """停止服务器"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("  服务器已停止")

# 演示
server = MultiClientServer("127.0.0.1", 9997)
server.start()

# 模拟多个客户端连接
def simulate_client(client_id: int):
    time.sleep(0.2)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9997))
        s.send(f"Client {client_id}".encode())
        response = s.recv(1024)
        print(f"  客户端{client_id} 收到: {response.decode()}")
        s.close()
    except Exception as e:
        print(f"  客户端{client_id} 错误: {e}")

threads = [threading.Thread(target=simulate_client, args=(i,)) for i in range(3)]
for t in threads:
    t.start()

server.accept_connections(1.5)
server.stop()


# ============ 5. JSON 协议通信 ============
print("\n" + "=" * 50)
print("5. JSON 协议通信")
print("=" * 50)

def send_json(sock: socket.socket, data: dict):
    """发送JSON数据"""
    json_str = json.dumps(data)
    message = json_str.encode()
    # 先发送长度
    length = len(message)
    sock.send(length.to_bytes(4, 'big'))
    sock.send(message)

def recv_json(sock: socket.socket) -> Optional[dict]:
    """接收JSON数据"""
    # 先接收长度
    length_bytes = sock.recv(4)
    if not length_bytes:
        return None
    length = int.from_bytes(length_bytes, 'big')
    # 接收数据
    data = sock.recv(length)
    return json.loads(data.decode())

def json_server(host: str, port: int, stop_event: threading.Event):
    """JSON协议服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.settimeout(1.0)
    server.bind((host, port))
    server.listen(1)
    
    try:
        while not stop_event.is_set():
            try:
                client, addr = server.accept()
                request = recv_json(client)
                print(f"  [JSON服务器] 收到: {request}")
                
                response = {
                    "status": "success",
                    "echo": request,
                    "timestamp": time.time()
                }
                send_json(client, response)
                client.close()
            except socket.timeout:
                continue
    finally:
        server.close()

stop_event = threading.Event()
server_thread = threading.Thread(target=json_server, args=("127.0.0.1", 9996, stop_event))
server_thread.start()

time.sleep(0.5)

# 客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9996))
send_json(client, {"action": "greet", "name": "Alice"})
response = recv_json(client)
print(f"  [JSON客户端] 收到: {response}")
client.close()

stop_event.set()
server_thread.join()


# ============ 6. Socket 选项 ============
print("\n" + "=" * 50)
print("6. Socket 选项")
print("=" * 50)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置选项
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.settimeout(30.0)

# 获取选项
reuse = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
keepalive = s.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
print(f"SO_REUSEADDR: {reuse}")
print(f"SO_KEEPALIVE: {keepalive}")
print(f"Timeout: {s.gettimeout()}")

s.close()


# ============ 7. 非阻塞 Socket ============
print("\n" + "=" * 50)
print("7. 非阻塞 Socket")
print("=" * 50)

print("""
非阻塞模式:
- socket.setblocking(False)
- 操作不等待,立即返回
- 需要处理 BlockingIOError

I/O 多路复用:
- select.select(): 跨平台
- selectors: 高级封装
- asyncio: 异步框架
""")


# ============ 8. 上下文管理器 ============
print("\n" + "=" * 50)
print("8. Socket 上下文管理器")
print("=" * 50)

# 使用with自动管理socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(2.0)
    try:
        s.connect(("httpbin.org", 80))
        request = "GET /ip HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n"
        s.send(request.encode())
        response = s.recv(4096)
        print(f"HTTP响应(前200字符):\n{response.decode()[:200]}")
    except socket.timeout:
        print("连接超时")
    except Exception as e:
        print(f"连接失败: {e}")


# ============ 总结 ============
print("\n" + "=" * 50)
print("Socket 编程总结")
print("=" * 50)
print("""
TCP vs UDP:
- TCP: 可靠、有序、面向连接
- UDP: 快速、简单、无连接

常用模式:
1. 阻塞 I/O: 简单,适合少量连接
2. 多线程: 每连接一线程
3. 非阻塞 + select: 单线程多连接
4. asyncio: 异步协程

最佳实践:
- 使用 with 管理 socket
- 设置合理的超时
- 处理网络异常
- 使用 SO_REUSEADDR
- 正确关闭连接
""")
