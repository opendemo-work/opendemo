package main

import (
	"encoding/json"
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

// User 结构体表示用户数据模型
// json 标签用于控制JSON序列化时的字段名称
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// 模拟数据库：使用切片存储用户数据（实际项目应使用数据库）
var users []User = []User{
	{ID: "1", Name: "Alice", Email: "alice@example.com"},
}

// GetUsers 处理获取所有用户的请求
func GetUsers(w http.ResponseWriter, r *http.Request) {
	// 设置响应头为JSON格式
	w.Header().Set("Content-Type", "application/json")
	// 将用户列表编码为JSON并写入响应
	if err := json.NewEncoder(w).Encode(users); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

// GetUser 处理根据ID获取单个用户
func GetUser(w http.ResponseWriter, r *http.Request) {
	// 解析URL路径中的变量
	params := mux.Vars(r)
	id := params["id"]
	// 遍历查找用户
	for _, user := range users {
		if user.ID == id {
			w.Header().Set("Content-Type", "application/json")
			json.NewEncoder(w).Encode(user)
			return
		}
	}
	// 未找到用户，返回404
	http.Error(w, "User not found", http.StatusNotFound)
}

// CreateUser 处理创建新用户
func CreateUser(w http.ResponseWriter, r *http.Request) {
	// 设置响应头
	w.Header().Set("Content-Type", "application/json")
	// 创建空User实例用于接收请求体
	var newUser User
	// 解码请求体中的JSON数据
	if err := json.NewDecoder(r.Body).Decode(&newUser); err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}
	// 简单模拟生成ID（实际应使用UUID等）
	if len(users) > 0 {
		newUser.ID = "2"
	} else {
		newUser.ID = "1"
	}
	// 添加到用户列表
	users = append(users, newUser)
	// 返回201状态码和创建的用户
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(newUser)
}

// 主函数：启动HTTP服务器
func main() {
	// 创建新的路由器
	r := mux.NewRouter()

	// 定义RESTful路由
	r.HandleFunc("/api/users", GetUsers).Methods("GET")
	r.HandleFunc("/api/users/{id}", GetUser).Methods("GET")
	r.HandleFunc("/api/users", CreateUser).Methods("POST")

	// 启动服务器
	log.Println("Server is running on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", r))
}