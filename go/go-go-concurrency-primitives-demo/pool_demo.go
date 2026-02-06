package main

import (
	"fmt"
	"sync"
)

type Data struct {
	Content string
}

var dataPool = sync.Pool{
	New: func() interface{} {
		return &Data{Content: "默认数据"}
	},
}

func main() {
	// 从池中获取一个对象
	objA := dataPool.Get().(*Data)
	objA.Content = "数据 A"
	fmt.Printf("获取对象: %s\n", objA.Content)

	// 归还对象
	dataPool.Put(objA)
	fmt.Printf("归还对象: %s\n", objA.Content)

	// 再次获取，可能会复用之前的对象
	objB := dataPool.Get().(*Data)
	objB.Content = "数据 B"
	fmt.Printf("获取对象: %s\n", objB.Content)

	// 尝试获取，可能复用
	objC := dataPool.Get().(*Data)
	if objC.Content == "数据 A" {
		fmt.Printf("从池中重用对象: %s\n", objC.Content)
	} else {
		fmt.Printf("新建对象: %s\n", objC.Content)
	}

	// 归还最后一个
	dataPool.Put(objC)
}