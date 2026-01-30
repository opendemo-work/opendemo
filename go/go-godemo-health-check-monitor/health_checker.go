// Package main 提供健康检查服务的核心逻辑
// 本文件定义了可扩展的健康检查机制，支持多组件状态聚合
package main

// 说明：为了简化项目结构，实际业务中可将此拆分为独立包
// 当前作为演示合并到 main 包中，但仍保持职责分离

// HealthChecker 接口允许未来插入不同的健康检查实现
// 例如：DatabaseHealthChecker、CacheHealthChecker 等
// type HealthChecker interface {
// 	Check() (map[string]string, string)
// }

// CompositeHealthChecker 可组合多个健康检查器
// type CompositeHealthChecker struct {
// 	checkers []HealthChecker
// }

// NewCompositeHealthChecker 创建一个新的组合检查器
// func NewCompositeHealthChecker(checkers ...HealthChecker) *CompositeHealthChecker {
// 	return &CompositeHealthChecker{checkers: checkers}
// }

// Check 执行所有子检查并聚合结果
// func (c *CompositeHealthChecker) Check() (map[string]string, string) {
// 	details := make(map[string]string)
// 	allHealthy := true

// 	for _, checker := range c.checkers {
// 		result, status := checker.Check()
// 		for k, v := range result {
// 			details[k] = v
// 		}
// 		if status != "healthy" {
// 			allHealthy = false
// 		}
// 	}

// 	if allHealthy {
// 		return details, "healthy"
// 	}
// 	return details, "degraded"
// }

// 注意：上述代码被注释，以便在单个demo中聚焦核心概念
// 实际扩展时可取消注释并重构