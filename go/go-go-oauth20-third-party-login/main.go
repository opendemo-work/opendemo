package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

// 主函数：设置路由并启动HTTP服务器
func main() {
	// 创建基于 Gorilla Mux 的路由器
	router := mux.NewRouter()

	// 注册处理函数
	router.HandleFunc("/login", loginHandler).Methods("GET")
	router.HandleFunc("/callback", callbackHandler).Methods("GET")

	// 提供静态资源（可选）
	router.PathPrefix("/").Handler(http.FileServer(http.Dir("./public/")))

	log.Println("服务器启动在 :8080...")
	log.Println("访问 http://localhost:8080/login 使用 GitHub 登录")

	// 启动服务器，监听8080端口
	if err := http.ListenAndServe(":8080", router); err != nil {
		log.Fatalf("服务器启动失败: %v", err)
	}
}
