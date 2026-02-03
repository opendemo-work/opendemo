package main

import (
	"log"
	"math/rand"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"sync"
	"time"
)

// 后端服务器列表
var backends = []string{
	"http://localhost:8081",
	"http://localhost:8082",
}

// 轮询索引和互斥锁
var (
	mu        sync.Mutex
	curIndex  int
)

// getNextBackend 使用轮询策略获取下一个健康的后端
func getNextBackend() *url.URL {
	mu.Lock()
	defer mu.Unlock()

	// 简单轮询
	backend := backends[curIndex%len(backends)]
	curIndex++

	backendURL, err := url.Parse(backend)
	if err != nil {
		log.Fatalf("Failed to parse backend URL: %v", err)
	}

	log.Printf("Serving request via backend: %s", backend)
	return backendURL
}

// 负载均衡反向代理处理器
func proxyHandler(w http.ResponseWriter, r *http.Request) {
	// 获取目标后端
	target := getNextBackend()

	// 创建反向代理
	proxy := httputil.NewSingleHostReverseProxy(target)

	// 修改请求头，保留原始信息
	originalScheme := "http"
	if r.TLS != nil {
		originalScheme = "https"
	}
	r.Header.Set("X-Forwarded-Host", r.Host)
	r.Header.Set("X-Forwarded-For", getClientIP(r))
	r.Header.Set("X-Forwarded-Proto", originalScheme)

	// 执行代理
	proxy.ServeHTTP(w, r)
}

// 获取客户端真实IP
func getClientIP(r *http.Request) string {
	// 检查 X-Forwarded-For 头
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		return xff
	}
	// 检查 X-Real-IP
	if xrip := r.Header.Get("X-Real-IP"); xrip != "" {
		return xrip
	}
	// 默认从远程地址提取
	ip, _, _ := net.SplitHostPort(r.RemoteAddr)
	return ip
}

func main() {
	// 设置随机种子
	rand.Seed(time.Now().UnixNano())

	log.Println("Reverse proxy server starting on :8000")
	log.Println("Load balancing requests between :8081 and :8082")

	// 注册处理函数
	http.HandleFunc("/", proxyHandler)

	// 启动服务
	log.Fatal(http.ListenAndServe(":8000", nil))
}