package main

import (
	"encoding/json"
	"fmt"
	"log"
)

// Person 表示一个人的基本信息
// 使用 json tag 来定义JSON字段名
type Person struct {
	Name  string `json:"name"`
	Age   int    `json:"age"`
	Email string `json:"email"`
}

func main() {
	// 创建一个Person实例
	person := Person{
		Name:  "张三",
		Age:   25,
		Email: "zhangsan@example.com",
	}

	// 将结构体序列化为JSON
	jsonData, err := json.Marshal(person)
	if err != nil {
		log.Fatalf("JSON序列化失败: %v", err)
	}

	fmt.Printf("序列化后的JSON: %s\n\n", jsonData)

	// 将JSON反序列化回结构体
	var decodedPerson Person
	err = json.Unmarshal(jsonData, &decodedPerson)
	if err != nil {
		log.Fatalf("JSON反序列化失败: %v", err)
	}

	fmt.Println("反序列化成功:")
	fmt.Printf("姓名: %s\n", decodedPerson.Name)
	fmt.Printf("年龄: %d\n", decodedPerson.Age)
	fmt.Printf("邮箱: %s\n", decodedPerson.Email)
}