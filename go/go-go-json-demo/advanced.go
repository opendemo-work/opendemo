package main

import (
	"encoding/json"
	"fmt"
	"log"
)

// Profile 用户资料
type Profile struct {
	Age  int    `json:"age"`
	City string `json:"city"`
}

// User 包含嵌套结构的用户对象
type User struct {
	User   struct {
		Name     string `json:"name"`
		Profile  `json:"profile"` // 嵌套结构
	} `json:"user"`
	Active bool `json:"active"` // 账户是否激活
}

func main() {
	// 构建嵌套结构体
	user := User{
		User: struct {
			Name    string `json:"name"`
			Profile `json:"profile"`
		}{
			Name: "李四",
			Profile: Profile{
				Age:  30,
				City: "北京",
			},
		},
		Active: true,
	}

	// 序列化为格式化的JSON
	jsonData, err := json.MarshalIndent(user, "", "\t")
	if err != nil {
		log.Fatalf("JSON编码失败: %v", err)
	}

	fmt.Printf("带嵌套的JSON: %s\n", jsonData)

	// 反序列化
	var decodedUser User
	err = json.Unmarshal(jsonData, &decodedUser)
	if err != nil {
		log.Fatalf("JSON解码失败: %v", err)
	}

	// 输出解析后的数据
	fmt.Printf("用户姓名: %s\n", decodedUser.User.Name)
	fmt.Printf("用户年龄: %d\n", decodedUser.User.Profile.Age)
	fmt.Printf("所在城市: %s\n", decodedUser.User.Profile.City)
	fmt.Printf("账户状态: %t\n", decodedUser.Active)
}