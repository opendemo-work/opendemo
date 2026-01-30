package main

// main 是程序入口点
// 展示如何通过手动依赖注入组装组件
func main() {
	// 第一步：创建具体的邮件服务实现
	// 可替换为其他实现（如Mock、日志等）
	mailService := &RealEmailService{}

	// 第二步：创建通知服务，并注入邮件依赖
	notifier := NewNotificationService(mailService)

	// 第三步：创建用户注册服务，并注入通知依赖
	userService := NewUserRegistrationService(notifier)

	// 第四步：执行业务逻辑
	_ = userService.Register("Alice")

	// 输出将显示整个流程的调用链
}