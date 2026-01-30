package main

import (
	"log"
	"net/http"
	"time"

	// 导入pprof以自动注册调试路由
	_ "net/http/pprof"
)

// cpuHeavyFunction 模拟CPU密集型任务
func cpuHeavyFunction(n int) int64 {
	var result int64
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			result += int64(i * j)
		}
	}
	return result
}

// cpuHandler 处理/CPU路径的HTTP请求，触发CPU密集型计算
func cpuHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("开始CPU密集型任务...")
	start := time.Now()

	// 执行一个较大的计算
	result := cpuHeavyFunction(4000)

	duration := time.Since(start)
	log.Printf("计算完成，耗时: %v, 结果: %d\n", duration, result)

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("CPU任务完成，耗时: " + duration.String() + "\n"))
}

func main() {
	// 注册HTTP处理器
	http.HandleFunc("/cpu", cpuHandler)

	// pprof的路由由导入_ "net/http/pprof"自动注册
	log.Println("服务器启动在 :8080")
	log.Println("访问 /debug/pprof/ 查看pprof界面")

	// 在后台定期触发内存增长
	go func() {
		time.Sleep(5 * time.Second)
		for {
			growMemory()
			log.Println("模拟内存增长，请稍等...")
			time.Sleep(10 * time.Second)
		}
	}()

	// 启动HTTP服务器
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal("服务器启动失败:", err)
	}
}