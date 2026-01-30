package main

import (
	"html/template"
	"os"
)

// 用户信息结构体
type Profile struct {
	Name    string
	Age     int
	Hobbies []string
	Married bool
}

func main() {
	// 定义HTML模板（使用反引号支持多行）
	const htmlTemplate = `<html><body>
<h1>用户资料 - {{.Name}}</h1>
<p>年龄: {{.Age}}</p>
<ul>
{{range .Hobbies}}
<li>{{.}}</li>
{{end}}
</ul>
<p>状态: {{if .Married}}已婚{{else}}未婚{{end}}</p>
</body></html>`

	// 解析HTML模板
	tmpl, err := template.New("profile").Parse(htmlTemplate)
	if err != nil {
		panic(err)
	}

	// 模拟用户数据
	profile := Profile{
		Name:    "张三",
		Age:     30,
		Hobbies: []string{"编程", "阅读", "跑步"},
		Married: true,
	}

	// 渲染模板并输出到控制台
	err = tmpl.Execute(os.Stdout, profile)
	if err != nil {
		panic(err)
	}
}