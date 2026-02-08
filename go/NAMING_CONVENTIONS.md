# Go 技术栈命名大全

本文件定义了Go语言技术栈中各类组件、变量、函数、包等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、包和模块命名规范

### 1.1 包命名
```go
// 标准库风格包名
package main        // 主程序包
package http        // HTTP相关功能
package json        // JSON处理
package ioutil      // IO工具
package filepath    // 文件路径处理

// 应用程序包名
package user        // 用户相关业务逻辑
package order       // 订单处理模块
package payment     // 支付处理模块
package auth        // 认证授权模块
package logger      // 日志处理模块

// 内部包命名
package internal    // 内部实现，不对外暴露
package utils       // 通用工具函数
package config      // 配置管理
package middleware  // 中间件组件
package repository  // 数据访问层
```

### 1.2 模块路径命名
```go
// 模块声明
module github.com/company/project-name

// 子模块命名
module github.com/company/project-name/api
module github.com/company/project-name/internal/user
module github.com/company/project-name/pkg/logger
module github.com/company/project-name/cmd/server

// 版本管理
require (
    github.com/gin-gonic/gin v1.9.1
    github.com/go-sql-driver/mysql v1.7.1
    github.com/spf13/viper v1.16.0
)
```

## 二、变量和常量命名规范

### 2.1 变量命名
```go
// 局部变量 - 简洁明了
func processUser() {
    userName := "john_doe"
    userAge := 25
    isActive := true
    retryCount := 0
    maxRetries := 3
}

// 全局变量 - 描述性强
var (
    DatabaseConnection *sql.DB
    Logger             *zap.Logger
    Config             *AppConfig
    ServerInstance     *http.Server
    CacheClient        *redis.Client
)

// 结构体字段命名
type User struct {
    ID        int64     `json:"id" db:"id"`
    Username  string    `json:"username" db:"username"`
    Email     string    `json:"email" db:"email"`
    CreatedAt time.Time `json:"created_at" db:"created_at"`
    UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

// 错误变量命名
var (
    ErrUserNotFound      = errors.New("user not found")
    ErrInvalidPassword   = errors.New("invalid password")
    ErrDatabaseConnFail  = errors.New("database connection failed")
    ErrTimeout           = errors.New("operation timeout")
)
```

### 2.2 常量命名
```go
// 枚举常量
const (
    StatusPending    = "pending"
    StatusProcessing = "processing"
    StatusCompleted  = "completed"
    StatusFailed     = "failed"
)

// 配置常量
const (
    DefaultPort          = "8080"
    DefaultTimeout       = 30 * time.Second
    MaxRequestSize       = 10 << 20 // 10MB
    DefaultPageSize      = 20
    MaxConcurrentWorkers = 100
)

// 环境相关常量
const (
    EnvDevelopment = "development"
    EnvStaging     = "staging"
    EnvProduction  = "production"
)

// 错误码常量
const (
    ErrorCodeInternal     = 500
    ErrorCodeBadRequest   = 400
    ErrorCodeUnauthorized = 401
    ErrorCodeNotFound     = 404
)
```

## 三、函数和方法命名规范

### 3.1 函数命名
```go
// 动词开头的函数名
func CreateUser(user *User) error {
    // 创建用户的业务逻辑
    return nil
}

func ValidateEmail(email string) bool {
    // 邮箱验证逻辑
    return true
}

func CalculateTotal(items []OrderItem) float64 {
    // 计算总金额
    return 0.0
}

func SendNotification(message string) error {
    // 发送通知
    return nil
}

// Getter/Setter函数
func (u *User) GetUsername() string {
    return u.Username
}

func (u *User) SetUsername(username string) {
    u.Username = username
}

// 布尔返回函数
func IsUserActive(userID int64) bool {
    // 检查用户是否活跃
    return true
}

func HasPermission(userID int64, permission string) bool {
    // 检查权限
    return true
}

// 工厂函数
func NewUserService(db *sql.DB, logger *zap.Logger) *UserService {
    return &UserService{
        db:     db,
        logger: logger,
    }
}

func NewHTTPClient(timeout time.Duration) *http.Client {
    return &http.Client{
        Timeout: timeout,
    }
}
```

### 3.2 方法命名
```go
// 接口方法
type UserRepository interface {
    Create(user *User) error
    FindByID(id int64) (*User, error)
    Update(user *User) error
    Delete(id int64) error
    List(filter UserFilter) ([]*User, error)
}

// 实现方法
func (r *mysqlUserRepository) Create(user *User) error {
    query := "INSERT INTO users (username, email) VALUES (?, ?)"
    result, err := r.db.Exec(query, user.Username, user.Email)
    if err != nil {
        return fmt.Errorf("failed to create user: %w", err)
    }
    
    id, err := result.LastInsertId()
    if err != nil {
        return fmt.Errorf("failed to get insert id: %w", err)
    }
    
    user.ID = id
    return nil
}

// 服务层方法
type OrderService struct {
    repo OrderRepository
    logger *zap.Logger
}

func (s *OrderService) ProcessPayment(orderID int64) error {
    order, err := s.repo.FindByID(orderID)
    if err != nil {
        return fmt.Errorf("failed to find order: %w", err)
    }
    
    if err := s.processPaymentLogic(order); err != nil {
        s.logger.Error("payment processing failed", 
            zap.Int64("order_id", orderID),
            zap.Error(err))
        return fmt.Errorf("payment processing failed: %w", err)
    }
    
    return nil
}
```

## 四、接口和类型命名规范

### 4.1 接口命名
```go
// 单方法接口 - er结尾
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// 多方法接口 - er结尾或描述性名称
type UserService interface {
    CreateUser(user *User) error
    GetUser(id int64) (*User, error)
    UpdateUser(user *User) error
    DeleteUser(id int64) error
    ListUsers(filter UserFilter) ([]*User, error)
}

type PaymentProcessor interface {
    ProcessPayment(amount float64, method string) error
    RefundPayment(transactionID string) error
    GetPaymentStatus(transactionID string) (string, error)
}

// 嵌套接口
type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}
```

### 4.2 结构体命名
```go
// 业务实体
type User struct {
    ID        int64     `json:"id" db:"id"`
    Username  string    `json:"username" db:"username"`
    Email     string    `json:"email" db:"email"`
    Password  string    `json:"-" db:"password"` // 敏感信息不序列化
    CreatedAt time.Time `json:"created_at" db:"created_at"`
    UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

type Order struct {
    ID         int64          `json:"id" db:"id"`
    UserID     int64          `json:"user_id" db:"user_id"`
    Items      []OrderItem    `json:"items"`
    Total      float64        `json:"total" db:"total"`
    Status     OrderStatus    `json:"status" db:"status"`
    CreatedAt  time.Time      `json:"created_at" db:"created_at"`
}

// 配置结构体
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Redis    RedisConfig    `mapstructure:"redis"`
    Logging  LogConfig      `mapstructure:"logging"`
}

type ServerConfig struct {
    Port         string        `mapstructure:"port"`
    ReadTimeout  time.Duration `mapstructure:"read_timeout"`
    WriteTimeout time.Duration `mapstructure:"write_timeout"`
    IdleTimeout  time.Duration `mapstructure:"idle_timeout"`
}

// 请求响应结构体
type CreateUserRequest struct {
    Username string `json:"username" binding:"required"`
    Email    string `json:"email" binding:"required,email"`
    Password string `json:"password" binding:"required,min=8"`
}

type APIResponse struct {
    Success bool        `json:"success"`
    Message string      `json:"message,omitempty"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
}
```

## 五、并发和上下文命名规范

### 5.1 Goroutine相关
```go
// Channel命名
var (
    userChan      chan *User
    orderChan     chan *Order
    resultChan    chan Result
    errorChan     chan error
    doneChan      chan struct{}
    notificationQ chan Notification
)

// WaitGroup命名
var (
    wg          sync.WaitGroup
    workerWg    sync.WaitGroup
    processorWg sync.WaitGroup
)

// Mutex命名
var (
    mu           sync.Mutex
    userMu       sync.RWMutex
    cacheMu      sync.RWMutex
    configMu     sync.RWMutex
)

// Context命名
func ProcessUserData(ctx context.Context, userID int64) error {
    // 使用带超时的context
    timeoutCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    
    // 使用带取消的context
    processCtx, processCancel := context.WithCancel(ctx)
    defer processCancel()
    
    // 业务逻辑处理
    return nil
}

// Worker池相关
type WorkerPool struct {
    workers    int
    jobQueue   chan Job
    quitChan   chan struct{}
    wg         sync.WaitGroup
}

func (wp *WorkerPool) Start() {
    for i := 0; i < wp.workers; i++ {
        wp.wg.Add(1)
        go wp.worker(i)
    }
}

func (wp *WorkerPool) worker(workerID int) {
    defer wp.wg.Done()
    
    for {
        select {
        case job := <-wp.jobQueue:
            wp.processJob(job)
        case <-wp.quitChan:
            return
        }
    }
}
```

### 5.2 错误处理命名
```go
// 自定义错误类型
type ValidationError struct {
    Field   string `json:"field"`
    Message string `json:"message"`
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field '%s': %s", e.Field, e.Message)
}

type BusinessError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Details string `json:"details,omitempty"`
}

func (e *BusinessError) Error() string {
    return fmt.Sprintf("business error [%d]: %s", e.Code, e.Message)
}

// 错误包装
func ProcessOrder(orderID int64) error {
    order, err := getOrderFromDB(orderID)
    if err != nil {
        return fmt.Errorf("failed to get order %d: %w", orderID, err)
    }
    
    if err := validateOrder(order); err != nil {
        return fmt.Errorf("order validation failed: %w", err)
    }
    
    if err := chargePayment(order); err != nil {
        return &BusinessError{
            Code:    4001,
            Message: "payment processing failed",
            Details: err.Error(),
        }
    }
    
    return nil
}

// 错误检查辅助函数
func IsNotFoundError(err error) bool {
    var target *BusinessError
    if errors.As(err, &target) {
        return target.Code == 404
    }
    return false
}

func IsTimeoutError(err error) bool {
    return errors.Is(err, context.DeadlineExceeded)
}
```

## 六、测试相关命名规范

### 6.1 测试函数命名
```go
// 单元测试
func TestCreateUser(t *testing.T) {
    // 测试创建用户的基本功能
}

func TestValidateEmail_ValidEmail(t *testing.T) {
    // 测试有效邮箱验证
}

func TestValidateEmail_InvalidEmail(t *testing.T) {
    // 测试无效邮箱验证
}

func TestProcessPayment_Success(t *testing.T) {
    // 测试支付成功场景
}

func TestProcessPayment_InsufficientFunds(t *testing.T) {
    // 测试余额不足场景
}

// 表驱动测试
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        amount   float64
        userType string
        expected float64
    }{
        {"Regular user small amount", 100, "regular", 0},
        {"Premium user medium amount", 500, "premium", 50},
        {"VIP user large amount", 1000, "vip", 150},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := calculateDiscount(tt.amount, tt.userType)
            if result != tt.expected {
                t.Errorf("expected %.2f, got %.2f", tt.expected, result)
            }
        })
    }
}

// 基准测试
func BenchmarkProcessLargeDataset(b *testing.B) {
    data := generateTestData(10000)
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        processDataset(data)
    }
}

func BenchmarkDatabaseQuery(b *testing.B) {
    db := setupTestDatabase()
    defer db.Close()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        getUsers(db, 100)
    }
}

// 示例测试
func ExampleUserService_CreateUser() {
    userService := NewUserService(mockDB, mockLogger)
    user := &User{Username: "testuser", Email: "test@example.com"}
    
    err := userService.CreateUser(user)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    fmt.Printf("Created user with ID: %d\n", user.ID)
    // Output: Created user with ID: 1
}
```

### 6.2 测试辅助结构
```go
// 测试数据构建器
type UserBuilder struct {
    user *User
}

func NewUserBuilder() *UserBuilder {
    return &UserBuilder{
        user: &User{
            Username: "testuser",
            Email:    "test@example.com",
        },
    }
}

func (ub *UserBuilder) WithUsername(username string) *UserBuilder {
    ub.user.Username = username
    return ub
}

func (ub *UserBuilder) WithEmail(email string) *UserBuilder {
    ub.user.Email = email
    return ub
}

func (ub *UserBuilder) Build() *User {
    return ub.user
}

// 测试Mock
type MockUserRepository struct {
    users map[int64]*User
    mu    sync.RWMutex
}

func (m *MockUserRepository) Create(user *User) error {
    m.mu.Lock()
    defer m.mu.Unlock()
    
    user.ID = int64(len(m.users) + 1)
    m.users[user.ID] = user
    return nil
}

func (m *MockUserRepository) FindByID(id int64) (*User, error) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    
    user, exists := m.users[id]
    if !exists {
        return nil, ErrUserNotFound
    }
    return user, nil
}
```

## 七、日志和监控命名规范

### 7.1 日志字段命名
```go
// 结构化日志
logger.Info("user login successful",
    zap.Int64("user_id", userID),
    zap.String("username", username),
    zap.String("ip_address", clientIP),
    zap.String("user_agent", userAgent),
    zap.Duration("processing_time", processingTime),
)

logger.Error("database operation failed",
    zap.String("operation", "insert_user"),
    zap.Int64("user_id", userID),
    zap.Error(err),
    zap.String("query", query),
    zap.Duration("duration", queryDuration),
)

logger.Warn("rate limit exceeded",
    zap.String("endpoint", endpoint),
    zap.String("client_ip", clientIP),
    zap.Int("request_count", requestCount),
    zap.Int("limit", rateLimit),
)

// 业务指标日志
logger.Info("order processed",
    zap.String("event_type", "order_processed"),
    zap.Int64("order_id", orderID),
    zap.Float64("amount", orderAmount),
    zap.String("payment_method", paymentMethod),
    zap.String("status", orderStatus),
)
```

### 7.2 监控指标命名
```go
// Prometheus指标
var (
    httpRequestTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status_code"},
    )
    
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
    
    activeUsers = prometheus.NewGauge(
        prometheus.GaugeOpts{
            Name: "active_users_count",
            Help: "Number of currently active users",
        },
    )
    
    databaseConnections = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "database_connections",
            Help: "Number of database connections",
        },
        []string{"state"},
    )
)

// 自定义指标收集
type MetricsCollector struct {
    requestCount      *prometheus.CounterVec
    errorCount        *prometheus.CounterVec
    processingTime    *prometheus.HistogramVec
    businessMetrics   *prometheus.GaugeVec
}

func NewMetricsCollector() *MetricsCollector {
    return &MetricsCollector{
        requestCount: prometheus.NewCounterVec(
            prometheus.CounterOpts{
                Name: "business_requests_total",
                Help: "Total number of business requests",
            },
            []string{"service", "operation"},
        ),
        errorCount: prometheus.NewCounterVec(
            prometheus.CounterOpts{
                Name: "business_errors_total",
                Help: "Total number of business errors",
            },
            []string{"service", "operation", "error_type"},
        ),
    }
}
```

## 八、配置和环境变量命名

### 8.1 配置结构体
```go
// 应用配置
type AppConfig struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Redis    RedisConfig    `mapstructure:"redis"`
    Logging  LogConfig      `mapstructure:"logging"`
    Security SecurityConfig `mapstructure:"security"`
}

type ServerConfig struct {
    Host            string        `mapstructure:"host"`
    Port            int           `mapstructure:"port"`
    ReadTimeout     time.Duration `mapstructure:"read_timeout"`
    WriteTimeout    time.Duration `mapstructure:"write_timeout"`
    IdleTimeout     time.Duration `mapstructure:"idle_timeout"`
    ShutdownTimeout time.Duration `mapstructure:"shutdown_timeout"`
}

type DatabaseConfig struct {
    Host     string `mapstructure:"host"`
    Port     int    `mapstructure:"port"`
    Username string `mapstructure:"username"`
    Password string `mapstructure:"password"`
    Database string `mapstructure:"database"`
    PoolSize int    `mapstructure:"pool_size"`
    SSLMode  string `mapstructure:"ssl_mode"`
}

// 环境变量配置
const (
    EnvServerHost     = "SERVER_HOST"
    EnvServerPort     = "SERVER_PORT"
    EnvDatabaseURL    = "DATABASE_URL"
    EnvRedisAddr      = "REDIS_ADDR"
    EnvLogLevel       = "LOG_LEVEL"
    EnvJWTSecret      = "JWT_SECRET"
    EnvEnableMetrics  = "ENABLE_METRICS"
)

// 配置加载
func LoadConfig() (*AppConfig, error) {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")
    viper.AddConfigPath("./config")
    
    // 环境变量前缀
    viper.SetEnvPrefix("APP")
    viper.AutomaticEnv()
    
    // 环境变量映射
    viper.BindEnv("server.host", EnvServerHost)
    viper.BindEnv("server.port", EnvServerPort)
    viper.BindEnv("database.url", EnvDatabaseURL)
    viper.BindEnv("redis.addr", EnvRedisAddr)
    
    if err := viper.ReadInConfig(); err != nil {
        return nil, fmt.Errorf("failed to read config: %w", err)
    }
    
    var config AppConfig
    if err := viper.Unmarshal(&config); err != nil {
        return nil, fmt.Errorf("failed to unmarshal config: %w", err)
    }
    
    return &config, nil
}
```

## 九、API和路由命名规范

### 9.1 RESTful API路由
```go
// 路由分组
func SetupRoutes(r *gin.Engine, handlers *Handlers) {
    // API版本前缀
    v1 := r.Group("/api/v1")
    {
        // 用户相关路由
        users := v1.Group("/users")
        {
            users.POST("", handlers.CreateUser)
            users.GET("/:id", handlers.GetUser)
            users.PUT("/:id", handlers.UpdateUser)
            users.DELETE("/:id", handlers.DeleteUser)
            users.GET("", handlers.ListUsers)
        }
        
        // 订单相关路由
        orders := v1.Group("/orders")
        {
            orders.POST("", handlers.CreateOrder)
            orders.GET("/:id", handlers.GetOrder)
            orders.PUT("/:id/status", handlers.UpdateOrderStatus)
            orders.GET("", handlers.ListOrders)
        }
        
        // 认证相关路由
        auth := v1.Group("/auth")
        {
            auth.POST("/login", handlers.Login)
            auth.POST("/logout", handlers.Logout)
            auth.POST("/refresh", handlers.RefreshToken)
        }
    }
}

// 中间件命名
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "missing token"})
            c.Abort()
            return
        }
        
        // 验证token逻辑
        userID, err := validateToken(token)
        if err != nil {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            c.Abort()
            return
        }
        
        c.Set("user_id", userID)
        c.Next()
    }
}

func RateLimitMiddleware() gin.HandlerFunc {
    limiter := rate.NewLimiter(rate.Every(time.Second), 100)
    
    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{
                "error": "rate limit exceeded",
            })
            c.Abort()
            return
        }
        c.Next()
    }
}
```

### 9.2 请求响应处理
```go
// 统一响应格式
type APIResponse struct {
    Success bool        `json:"success"`
    Message string      `json:"message,omitempty"`
    Data    interface{} `json:"data,omitempty"`
    Error   string      `json:"error,omitempty"`
    Meta    *MetaInfo   `json:"meta,omitempty"`
}

type MetaInfo struct {
    Page       int `json:"page,omitempty"`
    PageSize   int `json:"page_size,omitempty"`
    Total      int `json:"total,omitempty"`
    TotalPages int `json:"total_pages,omitempty"`
}

// 响应辅助函数
func SuccessResponse(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, APIResponse{
        Success: true,
        Data:    data,
    })
}

func ErrorResponse(c *gin.Context, statusCode int, message string, err error) {
    response := APIResponse{
        Success: false,
        Message: message,
    }
    
    if err != nil {
        response.Error = err.Error()
        // 记录错误日志
        logger.Error("API error",
            zap.String("path", c.Request.URL.Path),
            zap.Int("status", statusCode),
            zap.Error(err))
    }
    
    c.JSON(statusCode, response)
}

func PaginatedResponse(c *gin.Context, data interface{}, meta *MetaInfo) {
    c.JSON(http.StatusOK, APIResponse{
        Success: true,
        Data:    data,
        Meta:    meta,
    })
}
```

## 十、最佳实践示例

### 10.1 生产环境服务启动模板
```go
package main

import (
    "context"
    "fmt"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
    
    "github.com/gin-gonic/gin"
    "go.uber.org/zap"
    "gorm.io/gorm"
)

type Application struct {
    config   *Config
    logger   *zap.Logger
    db       *gorm.DB
    server   *http.Server
    services *Services
}

func NewApplication(cfg *Config) (*Application, error) {
    // 初始化日志
    logger, err := initLogger(cfg.Logging)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize logger: %w", err)
    }
    
    // 初始化数据库
    db, err := initDatabase(cfg.Database)
    if err != nil {
        logger.Error("failed to initialize database", zap.Error(err))
        return nil, fmt.Errorf("failed to initialize database: %w", err)
    }
    
    // 初始化服务
    services := initServices(db, logger)
    
    // 创建Gin引擎
    router := setupRouter(services, logger)
    
    server := &http.Server{
        Addr:         fmt.Sprintf(":%d", cfg.Server.Port),
        Handler:      router,
        ReadTimeout:  cfg.Server.ReadTimeout,
        WriteTimeout: cfg.Server.WriteTimeout,
        IdleTimeout:  cfg.Server.IdleTimeout,
    }
    
    return &Application{
        config:   cfg,
        logger:   logger,
        db:       db,
        server:   server,
        services: services,
    }, nil
}

func (app *Application) Run() error {
    // 启动服务器
    app.logger.Info("starting server", 
        zap.String("address", app.server.Addr))
    
    go func() {
        if err := app.server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            app.logger.Fatal("server failed to start", zap.Error(err))
        }
    }()
    
    // 等待中断信号
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    
    <-quit
    app.logger.Info("shutting down server...")
    
    // 优雅关闭
    ctx, cancel := context.WithTimeout(context.Background(), app.config.Server.ShutdownTimeout)
    defer cancel()
    
    if err := app.server.Shutdown(ctx); err != nil {
        app.logger.Error("server forced to shutdown", zap.Error(err))
        return err
    }
    
    app.logger.Info("server exited gracefully")
    return nil
}

func main() {
    // 加载配置
    cfg, err := LoadConfig()
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to load config: %v\n", err)
        os.Exit(1)
    }
    
    // 创建应用实例
    app, err := NewApplication(cfg)
    if err != nil {
        fmt.Fprintf(os.Stderr, "failed to create application: %v\n", err)
        os.Exit(1)
    }
    
    // 运行应用
    if err := app.Run(); err != nil {
        fmt.Fprintf(os.Stderr, "application error: %v\n", err)
        os.Exit(1)
    }
}
```

### 10.2 错误处理和恢复机制
```go
// 全局错误处理中间件
func ErrorHandlingMiddleware(logger *zap.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        defer func() {
            if err := recover(); err != nil {
                // 记录panic信息
                logger.Error("panic recovered",
                    zap.Any("error", err),
                    zap.String("path", c.Request.URL.Path),
                    zap.String("method", c.Request.Method),
                )
                
                // 返回500错误
                c.JSON(http.StatusInternalServerError, gin.H{
                    "error": "internal server error",
                })
                c.Abort()
            }
        }()
        
        c.Next()
    }
}

// 业务错误处理
type ErrorHandler struct {
    logger *zap.Logger
}

func NewErrorHandler(logger *zap.Logger) *ErrorHandler {
    return &ErrorHandler{logger: logger}
}

func (h *ErrorHandler) HandleError(c *gin.Context, err error) {
    // 根据错误类型返回不同的HTTP状态码
    switch {
    case errors.Is(err, ErrNotFound):
        h.logger.Warn("resource not found",
            zap.String("path", c.Request.URL.Path),
            zap.Error(err))
        c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
        
    case errors.Is(err, ErrValidation):
        h.logger.Warn("validation error",
            zap.String("path", c.Request.URL.Path),
            zap.Error(err))
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        
    case errors.Is(err, ErrUnauthorized):
        h.logger.Warn("unauthorized access",
            zap.String("path", c.Request.URL.Path),
            zap.String("client_ip", c.ClientIP()),
            zap.Error(err))
        c.JSON(http.StatusUnauthorized, gin.H{"error": err.Error()})
        
    default:
        h.logger.Error("internal error",
            zap.String("path", c.Request.URL.Path),
            zap.Error(err))
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal server error"})
    }
}
```

### 10.3 健康检查和监控
```go
// 健康检查处理器
type HealthChecker struct {
    db     *gorm.DB
    logger *zap.Logger
}

func NewHealthChecker(db *gorm.DB, logger *zap.Logger) *HealthChecker {
    return &HealthChecker{db: db, logger: logger}
}

func (hc *HealthChecker) HealthCheck(c *gin.Context) {
    health := HealthResponse{
        Status:    "healthy",
        Timestamp: time.Now().UTC(),
        Services:  make(map[string]string),
    }
    
    // 检查数据库连接
    ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
    defer cancel()
    
    if err := hc.db.WithContext(ctx).Exec("SELECT 1").Error; err != nil {
        health.Services["database"] = "unhealthy"
        health.Status = "degraded"
        hc.logger.Error("database health check failed", zap.Error(err))
    } else {
        health.Services["database"] = "healthy"
    }
    
    // 检查缓存连接
    if err := checkRedisConnection(); err != nil {
        health.Services["redis"] = "unhealthy"
        health.Status = "degraded"
        hc.logger.Error("redis health check failed", zap.Error(err))
    } else {
        health.Services["redis"] = "healthy"
    }
    
    statusCode := http.StatusOK
    if health.Status == "degraded" {
        statusCode = http.StatusServiceUnavailable
    }
    
    c.JSON(statusCode, health)
}

type HealthResponse struct {
    Status    string            `json:"status"`
    Timestamp time.Time         `json:"timestamp"`
    Services  map[string]string `json:"services"`
}

// 指标收集中间件
func MetricsMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        c.Next()
        
        duration := time.Since(start)
        statusCode := c.Writer.Status()
        
        // 记录指标
        httpRequestTotal.WithLabelValues(
            c.Request.Method,
            c.FullPath(),
            fmt.Sprintf("%d", statusCode),
        ).Inc()
        
        httpRequestDuration.WithLabelValues(
            c.Request.Method,
            c.FullPath(),
        ).Observe(duration.Seconds())
    }
}
```

---

**注意事项：**
1. 遵循Go官方命名约定和社区最佳实践
2. 错误处理应该具体且有意义，避免使用通用错误
3. 生产环境中必须包含完善的日志记录和监控
4. API设计应该遵循RESTful原则和一致性
5. 并发安全是Go程序的重要考虑因素