package main

// Person 表示一个人的基本信息
// 字段首字母大写表示可被外部包访问
type Person struct {
	Name string // 姓名
	Age  int    // 年龄
}

// IsAdult 判断此人是否为成年人
// 使用值接收者，因为Person结构体较小
// 返回布尔值表示是否年满18岁
func (p Person) IsAdult() bool {
	return p.Age >= 18
}

// 注意：若要修改结构体内容，应使用指针接收者：
// func (p *Person) SetAge(age int) { p.Age = age }