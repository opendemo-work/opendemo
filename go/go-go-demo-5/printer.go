package main

// Printable 定义了一个可以被打印的对象的接口
// 任何实现了 Print 方法的类型都自动满足此接口
type Printable interface {
	Print()
}

// Text 表示纯文本内容
type Text struct {
	Content string
}

// Print 实现 Printable 接口的方法
// 输出文本内容
func (t *Text) Print() {
	fmt.Println(t.Content)
}

// Document 表示文档类型，包含标题和内容
type Document struct {
	Title   string
	Content string
}

// Print 实现 Printable 接口
// 输出文档内容（可根据需要扩展格式化逻辑）
func (d *Document) Print() {
	fmt.Printf("Document content: %s\n", d.Content)
}