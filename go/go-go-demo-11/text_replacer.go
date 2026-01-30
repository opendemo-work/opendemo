package main

import (
	"fmt"
	"regexp"
)

// censorWords 定义需要屏蔽的敏感词汇列表
var censorWords = []string{"屏蔽词", "机密", "禁止"}

// createCensorRegex 构建一个匹配所有敏感词的正则表达式
// 使用 `|` 表示“或”，并将每个词转义以防特殊字符
func createCensorRegex() *regexp.Regexp {
	var pattern string
	for i, word := range censorWords {
		if i > 0 {
			pattern += `|`
		}
		pattern += regexp.QuoteMeta(word) // 自动转义特殊字符
	}
	return regexp.MustCompile(pattern)
}

// performTextReplacement 对文本执行敏感词替换
func performTextReplacement() {
	censorRegex := createCensorRegex()

	texts := []string{
		"用户提交了包含屏蔽词的内容",
		"这份文档含有机密信息，请勿传播",
	}

	fmt.Println("\n文本替换示例:")
	for _, text := range texts {
		cleaned := censorRegex.ReplaceAllString(text, "***")
		fmt.Printf("原始文本: %s\n", text)
		fmt.Printf("替换后: %s\n", cleaned)
	}
}