package main

// EmailService 定义邮件服务的接口
// 通过接口抽象，可以轻松替换为真实发送、日志记录或mock实现
type EmailService interface {
	Send(email, message string) error
}

// RealEmailService 真实的邮件发送实现
type RealEmailService struct{}

// Send 模拟发送邮件
func (s *RealEmailService) Send(email, message string) error {
	println("邮件服务发送消息到:", email+", 内容:", message)
	return nil
}

// UserService 定义用户相关业务逻辑的接口
type UserService interface {
	Register(name string) error
}

// NotificationService 通知中心，依赖EmailService来发送通知
type NotificationService struct {
	Email EmailService // 依赖通过构造函数注入
}

// NewNotificationService 构造函数，接收一个EmailService实现
// 符合依赖注入原则：由外部提供依赖，而非自行创建
func NewNotificationService(emailSvc EmailService) *NotificationService {
	return &NotificationService{Email: emailSvc}
}

// Notify 发送注册成功通知
func (n *NotificationService) Notify(email, message string) {
	n.Email.Send(email, message)
	println("通知中心完成通知流程")
}

// UserRegistrationService 用户注册服务，包含业务逻辑
type UserRegistrationService struct {
	Notifier *NotificationService
}

// NewUserRegistrationService 创建用户注册服务，注入通知组件
func NewUserRegistrationService(notifier *NotificationService) *UserRegistrationService {
	return &UserRegistrationService{Notifier: notifier}
}

// Register 处理用户注册流程
func (u *UserRegistrationService) Register(name string) error {
	println("用户服务正在处理:", name)
	// 模拟注册后发送欢迎邮件
	u.Notifier.Notify(name+"@example.com", "欢迎注册！")
	return nil
}