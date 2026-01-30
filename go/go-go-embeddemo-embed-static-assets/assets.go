package assets

import (
	"embed"
	"io/fs"
	"log"
)

//go:embed templates/*
var templateFS embed.FS

//go:embed config/app.json
var configFS embed.FS

// ReadTemplate 读取嵌入的HTML模板文件
func ReadTemplate() (string, error) {
	// 从虚拟文件系统读取文件
	data, err := fs.ReadFile(templateFS, "templates/index.html")
	if err != nil {
		return "", err
	}
	return string(data), nil
}

// ReadConfig 读取嵌入的JSON配置文件
func ReadConfig() (string, error) {
	data, err := fs.ReadFile(configFS, "config/app.json")
	if err != nil {
		return "", err
	}
	// 格式化输出JSON
	return string(data), nil
}