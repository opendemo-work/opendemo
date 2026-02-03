#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python HTTP请求演示
展示requests模块的常用功能(使用httpbin.org测试API)
"""
import json
from urllib.parse import urlencode


def demo_without_requests():
    """不使用requests库的HTTP请求演示"""
    print("=" * 50)
    print("HTTP请求演示 (使用内置urllib)")
    print("=" * 50)
    
    from urllib import request, error
    
    # GET请求
    print("\n1. GET请求:")
    try:
        url = "https://httpbin.org/get"
        with request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"  状态码: {response.status}")
            print(f"  URL: {data.get('url', 'N/A')}")
    except error.URLError as e:
        print(f"  请求失败(网络问题): {e}")
        demo_mock_requests()
        return


def demo_mock_requests():
    """模拟HTTP请求演示(无需网络)"""
    print("\n" + "=" * 50)
    print("HTTP请求演示 (模拟模式)")
    print("=" * 50)
    
    # 模拟Response对象
    class MockResponse:
        def __init__(self, status_code, json_data, headers=None):
            self.status_code = status_code
            self._json_data = json_data
            self.headers = headers or {'Content-Type': 'application/json'}
            self.text = json.dumps(json_data)
            self.content = self.text.encode('utf-8')
            self.ok = 200 <= status_code < 300
        
        def json(self):
            return self._json_data
        
        def raise_for_status(self):
            if not self.ok:
                raise Exception(f"HTTP Error: {self.status_code}")
    
    # 模拟GET请求
    print("\n1. GET请求示例:")
    response = MockResponse(200, {
        "args": {"name": "test"},
        "headers": {"User-Agent": "Python/3.x"},
        "url": "https://httpbin.org/get?name=test"
    })
    print(f"  状态码: {response.status_code}")
    print(f"  响应JSON: {response.json()}")
    
    # 模拟POST请求
    print("\n2. POST请求示例:")
    response = MockResponse(201, {
        "data": '{"username": "alice", "password: "${GENERIC_PASSWORD}"}',
        "json": {"username": "alice", "password: "${GENERIC_PASSWORD}"},
        "url": "https://httpbin.org/post"
    })
    print(f"  状态码: {response.status_code}")
    print(f"  提交的数据: {response.json().get('json')}")
    
    # 模拟带Headers的请求
    print("\n3. 自定义Headers:")
    headers = {
        "User-Agent": "MyApp/1.0",
        "Authorization": "Bearer token123",
        "Accept": "application/json"
    }
    print(f"  请求头: {headers}")
    
    # 模拟超时处理
    print("\n4. 超时处理:")
    print("  设置 timeout=5 秒")
    print("  try-except 捕获 requests.Timeout")
    
    # 模拟错误处理
    print("\n5. 错误处理:")
    error_response = MockResponse(404, {"error": "Not Found"})
    print(f"  状态码: {error_response.status_code}")
    print(f"  response.ok: {error_response.ok}")
    try:
        error_response.raise_for_status()
    except Exception as e:
        print(f"  raise_for_status(): {e}")


def demo_requests_patterns():
    """requests使用模式"""
    print("\n" + "=" * 50)
    print("Requests库常用模式")
    print("=" * 50)
    
    patterns = '''
# 安装: pip install requests

import requests

# 1. 基本GET请求
response = requests.get("https://api.example.com/users")
data = response.json()

# 2. 带参数的GET
params = {"page": 1, "limit": 10}
response = requests.get("https://api.example.com/users", params=params)

# 3. POST JSON数据
payload = {"name": "Alice", "email": "alice@example.com"}
response = requests.post(
    "https://api.example.com/users",
    json=payload
)

# 4. POST表单数据
form_data = {"username": "alice", "password: "${GENERIC_PASSWORD}"}
response = requests.post(
    "https://api.example.com/login",
    data=form_data
)

# 5. 自定义Headers
headers = {
    "Authorization": "Bearer token123",
    "Content-Type": "application/json"
}
response = requests.get(
    "https://api.example.com/protected",
    headers=headers
)

# 6. 超时设置
response = requests.get(
    "https://api.example.com/data",
    timeout=5  # 5秒超时
)

# 7. Session保持会话
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})
response1 = session.get("https://api.example.com/page1")
response2 = session.get("https://api.example.com/page2")

# 8. 文件上传
files = {"file": open("document.pdf", "rb")}
response = requests.post(
    "https://api.example.com/upload",
    files=files
)

# 9. 错误处理
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()  # 4xx/5xx会抛异常
    data = response.json()
except requests.Timeout:
    print("请求超时")
except requests.HTTPError as e:
    print(f"HTTP错误: {e}")
except requests.RequestException as e:
    print(f"请求失败: {e}")

# 10. 响应处理
response = requests.get("https://api.example.com/data")
print(response.status_code)  # 状态码
print(response.headers)       # 响应头
print(response.text)          # 文本内容
print(response.json())        # JSON解析
print(response.content)       # 二进制内容
'''
    print(patterns)


def demo_api_client():
    """API客户端封装示例"""
    print("\n" + "=" * 50)
    print("API客户端封装示例")
    print("=" * 50)
    
    client_code = '''
class APIClient:
    """API客户端封装"""
    
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
        self.session.headers['Content-Type'] = 'application/json'
    
    def _request(self, method, endpoint, **kwargs):
        """统一请求方法"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.HTTPError as e:
            error_msg = response.json().get('error', str(e))
            raise APIError(response.status_code, error_msg)
        except requests.RequestException as e:
            raise APIError(0, f"请求失败: {e}")
    
    def get(self, endpoint, params=None):
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint, data=None):
        return self._request('POST', endpoint, json=data)
    
    def put(self, endpoint, data=None):
        return self._request('PUT', endpoint, json=data)
    
    def delete(self, endpoint):
        return self._request('DELETE', endpoint)


class APIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")


# 使用示例
client = APIClient("https://api.example.com", api_key: "${API_KEY}")
users = client.get("/users", params={"page": 1})
new_user = client.post("/users", data={"name": "Alice"})
'''
    print(client_code)


if __name__ == "__main__":
    demo_without_requests()
    demo_requests_patterns()
    demo_api_client()
    print("\n[OK] HTTP请求演示完成!")
