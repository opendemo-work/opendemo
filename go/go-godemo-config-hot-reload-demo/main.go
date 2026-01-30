package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/fsnotify/fsnotify"
)

// 配置文件路径
const configPath = "config.json"

func main() {
	// 创建文件监听器
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal("创建监听器失败：", err)
	}
	defer watcher.Close()

	// 添加要监听的文件
	err = watcher.Add(configPath)
	if err != nil {
		log.Fatal("添加监听文件失败：", err)
	}

	fmt.Printf("监听 %s 中...\n", configPath)

	// 用于接收系统中断信号
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	// 监听文件事件
	for {
		select {
		case <-quit:
			fmt.Println("收到中断信号，正在退出...")
			return

		case event, ok := <-watcher.Events:
			if !ok {
				return
			}

			// 过滤写入和创建事件
			if event.Op&fsnotify.Write == fsnotify.Write ||
				 event.Op&fsnotify.Create == fsnotify.Create {
				fmt.Println("检测到配置文件变更，正在重载...")
				// 模拟配置重载操作
				reloadConfig()
			}

		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			log.Println("监听器错误：", err)
		}
	}
}

// reloadConfig 模拟重新加载配置
// 实际项目中可解析JSON/YAML并更新全局配置变量
func reloadConfig() {
	time.Sleep(100 * time.Millisecond) // 模拟I/O延迟
	// 在这里可以加入 json.Unmarshal 或 viper.ReadInConfig()
	fmt.Println("配置已重载")
}