package main

import (
	"strings"
	"text/template"
	"os"
)

// 定义用户数据结构
type User struct {
	Name     string
	Age      int
	Hobbies  []string
	Married  bool
}

// 自定义函数映射
var funcMap = template.FuncMap{
	// join 函数用于将切片元素用指定分隔符合并
	"join": strings.Join,
}

func main() {
	// 创建包含自定义函数的模板
	tmpl := template.New("userText").Funcs(funcMap)
	// 解析模板内容
	tmpl, err := tmpl.Parse(`
姓名: {{.Name}}
年龄: {{.Age}}
兴趣: {{join .Hobbies ", "}}
是否已婚: {{if .Married}}是{{else}}否{{end}}
`)
	if err != nil {
		panic(err)
	}

	// 示例数据
	user := User{
		Name:    "张三",
		Age:     30,
		Hobbies: []string{"编程", "阅读", "跑步"},
		Married: true,
	}

	// 执行模板并将结果输出到标准输出
	err = tmpl.Execute(os.Stdout, user)
	if err != nil {
		panic(err)
	}
}