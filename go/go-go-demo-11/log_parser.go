package main

import (
	"fmt"
	"regexp"
)

// logPattern 匹配日志行中的时间戳和请求路径
// 示例日志行："2023-04-05 14:23:01 | GET /api/users HTTP/1.1"
// 使用命名捕获组 (?P<name>...) 来标记感兴趣的部分
var logPattern = regexp.MustCompile(`(\d{2}:\d{2}:\d{2}) \| \w+ (/.*) HTTP/`)`

// parseLogLines 模拟解析多行日志数据
func parseLogLines() {
	logs := []string{
		"2023-04-05 14:23:01 | GET /api/users HTTP/1.1",
		"2023-04-05 14:23:05 | GET /static/image.png HTTP/1.1",
	}

	fmt.Println("\n解析日志条目:")
	for _, log := range logs {
		matches := logPattern.FindStringSubmatch(log)
		if len(matches) > 0 {
			// matches[0] 是完整匹配，后续为各捕获组
			time := matches[1]
			requestPath := matches[2]
			fmt.Printf("时间: %s, 请求路径: %s\n", time, requestPath)
		}
	}
}