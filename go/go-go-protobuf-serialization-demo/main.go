package main

import (
	"fmt"
	"log"

	"google.golang.org/protobuf/proto"
)

// 自动生成的代码需要先运行:
// protoc --go_out=. --go_opt=paths=source_relative person.proto
func main() {
	// 创建一个 Person 对象
	person := &Person{
		Name:  "Alice",
		Age:   30,
		Email: "alice@example.com",
	}

	// 打印原始对象
	fmt.Printf("原始对象: %v\n", person)

	// 序列化：将对象编码为二进制数据
	data, err := proto.Marshal(person)
	if err != nil {
		log.Fatalf("序列化失败: %v", err)
	}

	// 查看序列化后的字节长度
	fmt.Printf("序列化后的字节长度: %d\n", len(data))

	// 反序列化：从二进制数据恢复对象
	newPerson := &Person{}
	err = proto.Unmarshal(data, newPerson)
	if err != nil {
		log.Fatalf("反序列化失败: %v", err)
	}

	// 打印恢复后的对象
	fmt.Printf("反序列化后对象: %v\n", newPerson)
}