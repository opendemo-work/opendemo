package main

import (
	"errors"
	"fmt"
	"time"

	"github.com/sony/gobreaker"
)

var cb = gobreaker.NewCircuitBreaker(gobreaker.Settings{
	Name:        "example",
	MaxRequests: 1,                // 半开状态下允许的请求数
	Timeout:     5 * time.Second,  // 熔断持续时间
	ReadyToTrip: func(counts gobreaker.Counts) bool {
		// 连续失败超过2次则触发熔断
		return counts.ConsecutiveFailures > 2
	},
})

// 模拟一个可能失败的服务调用
func callService(success bool) (string, error) {
	returnValue, errValue := "调用正常服务", error(nil)
	if !success {
		errValue = errors.New("服务异常")
	}
	// 使用熔断器包装调用
	result, err := cb.Execute(func() (interface{}, error) {
		return returnValue, errValue
	})

	if err != nil {
		fmt.Printf("调用失败: %s\n", err)
		return "", err
	}

	fmt.Printf("调用成功: %s\n", result)
	return result.(string), nil
}

func main() {
	// 成功调用
	callService(true)

	// 连续失败3次触发熔断
	callService(false)
	callService(false)
	callService(false)

	// 熔断期间拒绝请求
	for i := 0; i < 3; i++ {
		callService(true)
		time.Sleep(1 * time.Second)
	}

	// 5秒后熔断器进入半开状态，尝试一次
	callService(true)
	time.Sleep(1 * time.Second)

	// 恢复成功，后续请求正常
	callService(true)
}