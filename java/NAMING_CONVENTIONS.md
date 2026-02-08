# Java 技术栈命名大全

本文件定义了Java技术栈中各类组件、类、方法、变量等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、包和模块命名规范

### 1.1 包命名规范
```java
// 域名反向包结构
package com.company.projectname;
package com.company.projectname.module;
package com.company.projectname.common.util;
package com.company.projectname.service.user;
package com.company.projectname.controller.api;

// 分层架构包命名
package com.company.projectname.controller;     // 控制层
package com.company.projectname.service;        // 服务层
package com.company.projectname.repository;     // 数据访问层
package com.company.projectname.model;          // 实体模型
package com.company.projectname.dto;            // 数据传输对象
package com.company.projectname.exception;      // 异常处理
package com.company.projectname.config;         // 配置类
package com.company.projectname.util;           // 工具类

// 业务领域包命名
package com.company.ecommerce.user;
package com.company.ecommerce.order;
package com.company.ecommerce.payment;
package com.company.ecommerce.inventory;
```

### 1.2 Maven模块命名
```xml
<!-- 父项目 -->
<groupId>com.company</groupId>
<artifactId>ecommerce-platform</artifactId>
<version>1.0.0</version>
<packaging>pom</packaging>

<!-- 子模块命名 -->
<modules>
    <module>ecommerce-user-service</module>
    <module>ecommerce-order-service</module>
    <module>ecommerce-payment-service</module>
    <module>ecommerce-common</module>
    <module>ecommerce-api</module>
</modules>

<!-- 依赖管理 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>2.7.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

## 二、类和接口命名规范

### 2.1 类命名
```java
// 实体类命名 - 名词形式
public class User {
    private Long id;
    private String username;
    private String email;
}

public class Order {
    private Long orderId;
    private Long userId;
    private BigDecimal totalAmount;
    private OrderStatus status;
}

public class Product {
    private Long productId;
    private String productName;
    private BigDecimal price;
    private Integer stockQuantity;
}

// 服务类命名 - Service结尾
@Service
public class UserService {
    // 业务逻辑实现
}

@Service
public class OrderProcessingService {
    // 订单处理逻辑
}

@Service
public class PaymentGatewayService {
    // 支付网关逻辑
}

// 控制器类命名 - Controller结尾
@RestController
@RequestMapping("/api/users")
public class UserController {
    // 用户相关API
}

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    // 订单相关API
}

// 配置类命名 - Config结尾
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    // 安全配置
}

@Configuration
@EnableSwagger2
public class SwaggerConfig {
    // API文档配置
}

// 异常类命名 - Exception结尾
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

public class InsufficientBalanceException extends BusinessException {
    public InsufficientBalanceException(String message) {
        super(message);
    }
}
```

### 2.2 接口命名
```java
// 服务接口 - Service结尾
public interface UserService {
    User createUser(UserDto userDto);
    User getUserById(Long userId);
    List<User> getAllUsers();
    void updateUser(UserDto userDto);
    void deleteUser(Long userId);
}

public interface OrderService {
    Order createOrder(OrderRequest request);
    Order getOrderById(Long orderId);
    List<Order> getUserOrders(Long userId);
    void cancelOrder(Long orderId);
}

// Repository接口 - Repository结尾
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    List<User> findByStatus(UserStatus status);
}

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUserIdOrderByCreatedAtDesc(Long userId);
    List<Order> findByStatus(OrderStatus status);
    @Query("SELECT o FROM Order o WHERE o.createdAt BETWEEN :startDate AND :endDate")
    List<Order> findOrdersByDateRange(@Param("startDate") LocalDateTime startDate,
                                    @Param("endDate") LocalDateTime endDate);
}

// DTO类命名
public class UserDto {
    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
}

public class OrderResponse {
    private Long orderId;
    private String orderNumber;
    private BigDecimal totalAmount;
    private OrderStatus status;
    private LocalDateTime createdAt;
}
```

## 三、方法和变量命名规范

### 3.1 方法命名
```java
// 动词开头的方法名
public class UserServiceImpl implements UserService {
    
    // CRUD操作方法
    @Override
    public User createUser(UserDto userDto) {
        // 创建用户逻辑
        return user;
    }
    
    @Override
    public User getUserById(Long userId) {
        // 获取用户逻辑
        return user;
    }
    
    @Override
    public List<User> getAllUsers() {
        // 获取所有用户逻辑
        return users;
    }
    
    @Override
    public void updateUser(UserDto userDto) {
        // 更新用户逻辑
    }
    
    @Override
    public void deleteUser(Long userId) {
        // 删除用户逻辑
    }
    
    // 业务逻辑方法
    public boolean authenticateUser(String username, String password) {
        // 用户认证逻辑
        return true;
    }
    
    public void sendWelcomeEmail(User user) {
        // 发送欢迎邮件
    }
    
    public List<User> findUsersByRole(String role) {
        // 根据角色查找用户
        return users;
    }
    
    // 布尔返回方法 - is/has/can开头
    public boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }
    
    public boolean hasPermission(Long userId, String permission) {
        // 检查权限
        return true;
    }
    
    public boolean canAccessResource(Long userId, String resourceId) {
        // 检查资源访问权限
        return true;
    }
    
    // 工厂方法 - create/build/make开头
    public static User createUser(String username, String email) {
        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        return user;
    }
    
    // 转换方法 - to/from开头
    public UserDto toDto(User user) {
        UserDto dto = new UserDto();
        dto.setId(user.getId());
        dto.setUsername(user.getUsername());
        return dto;
    }
    
    public User fromDto(UserDto dto) {
        User user = new User();
        user.setId(dto.getId());
        user.setUsername(dto.getUsername());
        return user;
    }
}
```

### 3.2 变量命名
```java
// 局部变量 - 驼峰命名法
public void processOrder(Order order) {
    BigDecimal totalAmount = order.getTotalAmount();
    LocalDateTime orderDate = order.getCreatedAt();
    String customerEmail = order.getCustomer().getEmail();
    boolean isPriorityOrder = order.getOrderType() == OrderType.PRIORITY;
    
    List<OrderItem> orderItems = order.getItems();
    int itemCount = orderItems.size();
    
    // 循环变量
    for (OrderItem item : orderItems) {
        String productName = item.getProduct().getName();
        BigDecimal itemPrice = item.getPrice();
        int quantity = item.getQuantity();
    }
}

// 成员变量 - 私有且有意义
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentService paymentService;
    private final EmailService emailService;
    private final Logger logger = LoggerFactory.getLogger(OrderService.class);
    
    private static final int MAX_RETRY_ATTEMPTS = 3;
    private static final long DEFAULT_TIMEOUT_MS = 5000L;
    private static final String ORDER_CONFIRMATION_TEMPLATE = "order_confirmation";
}

// 常量命名 - 全大写加下划线
public class Constants {
    public static final String API_VERSION = "v1";
    public static final String DEFAULT_ROLE = "USER";
    public static final int MAX_LOGIN_ATTEMPTS = 5;
    public static final long SESSION_TIMEOUT_MINUTES = 30;
    public static final String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";
    public static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";
}
```

## 四、注解和配置命名规范

### 4.1 Spring注解
```java
// 控制器注解
@RestController
@RequestMapping("/api/v1/users")
@Validated
@Slf4j
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    @ApiOperation("根据ID获取用户信息")
    public ResponseEntity<UserDto> getUserById(
            @ApiParam(value = "用户ID", required = true)
            @PathVariable Long id) {
        
        UserDto user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    @ApiOperation("创建新用户")
    public ResponseEntity<UserDto> createUser(
            @ApiParam(value = "用户信息", required = true)
            @Valid @RequestBody CreateUserRequest request) {
        
        UserDto user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
    
    @PutMapping("/{id}")
    @ApiOperation("更新用户信息")
    public ResponseEntity<UserDto> updateUser(
            @ApiParam(value = "用户ID", required = true)
            @PathVariable Long id,
            @ApiParam(value = "更新的用户信息", required = true)
            @Valid @RequestBody UpdateUserRequest request) {
        
        UserDto user = userService.updateUser(id, request);
        return ResponseEntity.ok(user);
    }
}

// 服务层注解
@Service
@Transactional(readOnly = true)
@Slf4j
public class UserServiceImpl implements UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Override
    @Transactional
    public UserDto createUser(CreateUserRequest request) {
        // 业务逻辑
        return userDto;
    }
    
    @Cacheable(value = "users", key = "#id")
    public UserDto getUserById(Long id) {
        // 获取用户逻辑
        return userDto;
    }
    
    @CacheEvict(value = "users", key = "#id")
    @Transactional
    public void updateUser(Long id, UpdateUserRequest request) {
        // 更新用户逻辑
    }
}

// 配置类注解
@Configuration
@EnableTransactionManagement
@ComponentScan(basePackages = "com.company.project")
@PropertySource("classpath:application.properties")
public class ApplicationConfig {
    
    @Bean
    @Primary
    public DataSource dataSource() {
        // 数据源配置
        return dataSource;
    }
    
    @Bean
    public PlatformTransactionManager transactionManager() {
        return new DataSourceTransactionManager(dataSource());
    }
    
    @Bean
    @ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("users", "orders", "products");
    }
}
```

### 4.2 自定义注解
```java
// 权限检查注解
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RequirePermission {
    String value();
    String description() default "";
}

// 日志记录注解
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface LogExecutionTime {
    String value() default "";
}

// 参数验证注解
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = EmailValidator.class)
@Documented
public @interface ValidEmail {
    String message() default "Invalid email format";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// 切面实现
@Aspect
@Component
@Slf4j
public class LoggingAspect {
    
    @Around("@annotation(LogExecutionTime)")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        
        Object result = joinPoint.proceed();
        
        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;
        
        log.info("{} executed in {} ms", 
                joinPoint.getSignature().toShortString(), 
                executionTime);
        
        return result;
    }
    
    @Before("@annotation(requirePermission)")
    public void checkPermission(JoinPoint joinPoint, RequirePermission requirePermission) {
        // 权限检查逻辑
        String permission = requirePermission.value();
        // 检查当前用户是否有指定权限
    }
}
```

## 五、异常处理命名规范

### 5.1 异常类层次结构
```java
// 基础业务异常
public abstract class BusinessException extends RuntimeException {
    private final String errorCode;
    private final Object[] params;
    
    public BusinessException(String message) {
        super(message);
        this.errorCode = "BUSINESS_ERROR";
        this.params = new Object[0];
    }
    
    public BusinessException(String errorCode, String message, Object... params) {
        super(message);
        this.errorCode = errorCode;
        this.params = params;
    }
    
    public String getErrorCode() {
        return errorCode;
    }
    
    public Object[] getParams() {
        return params;
    }
}

// 具体业务异常
public class UserNotFoundException extends BusinessException {
    public UserNotFoundException(Long userId) {
        super("USER_NOT_FOUND", "User with ID {0} not found", userId);
    }
}

public class InsufficientBalanceException extends BusinessException {
    public InsufficientBalanceException(BigDecimal required, BigDecimal available) {
        super("INSUFFICIENT_BALANCE", 
              "Insufficient balance. Required: {0}, Available: {1}", 
              required, available);
    }
}

public class OrderProcessingException extends BusinessException {
    public OrderProcessingException(String orderId, String reason) {
        super("ORDER_PROCESSING_FAILED", 
              "Failed to process order {0}: {1}", 
              orderId, reason);
    }
}

// 系统异常
public class DatabaseException extends RuntimeException {
    public DatabaseException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class ExternalServiceException extends RuntimeException {
    private final String serviceName;
    
    public ExternalServiceException(String serviceName, String message, Throwable cause) {
        super(message, cause);
        this.serviceName = serviceName;
    }
    
    public String getServiceName() {
        return serviceName;
    }
}
```

### 5.2 全局异常处理器
```java
@ControllerAdvice
@RestController
@Slf4j
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
        log.warn("Business exception occurred: {}", ex.getMessage(), ex);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code(ex.getErrorCode())
                .message(ex.getMessage())
                .timestamp(LocalDateTime.now())
                .build();
                
        return ResponseEntity.badRequest().body(errorResponse);
    }
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFoundException(UserNotFoundException ex) {
        log.warn("User not found: {}", ex.getMessage());
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("USER_NOT_FOUND")
                .message(ex.getMessage())
                .timestamp(LocalDateTime.now())
                .build();
                
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(errorResponse);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex) {
        
        List<String> errors = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.toList());
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("VALIDATION_ERROR")
                .message("Validation failed")
                .details(errors)
                .timestamp(LocalDateTime.now())
                .build();
                
        return ResponseEntity.badRequest().body(errorResponse);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        log.error("Unexpected error occurred", ex);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
                .code("INTERNAL_SERVER_ERROR")
                .message("An unexpected error occurred")
                .timestamp(LocalDateTime.now())
                .build();
                
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
    }
}

@Data
@Builder
public class ErrorResponse {
    private String code;
    private String message;
    private List<String> details;
    private LocalDateTime timestamp;
}
```

## 六、测试相关命名规范

### 6.1 单元测试命名
```java
// 测试类命名 - Test结尾
public class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }
    
    // 测试方法命名 - should_期望行为_when_测试条件
    @Test
    void shouldReturnUserWhenValidIdProvided() {
        // Given
        Long userId = 1L;
        User expectedUser = User.builder().id(userId).username("testuser").build();
        when(userRepository.findById(userId)).thenReturn(Optional.of(expectedUser));
        
        // When
        User actualUser = userService.getUserById(userId);
        
        // Then
        assertThat(actualUser).isEqualTo(expectedUser);
        verify(userRepository).findById(userId);
    }
    
    @Test
    void shouldThrowExceptionWhenUserNotFound() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());
        
        // When & Then
        assertThatThrownBy(() -> userService.getUserById(userId))
                .isInstanceOf(UserNotFoundException.class)
                .hasMessageContaining("not found");
        
        verify(userRepository).findById(userId);
    }
    
    @Test
    void shouldCreateUserSuccessfully() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
                .username("newuser")
                .email("newuser@example.com")
                .password("password123")
                .build();
                
        User savedUser = User.builder()
                .id(1L)
                .username("newuser")
                .email("newuser@example.com")
                .build();
                
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        // When
        UserDto result = userService.createUser(request);
        
        // Then
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getUsername()).isEqualTo("newuser");
        verify(userRepository).save(any(User.class));
    }
}

// 集成测试命名
@SpringBootTest
@Testcontainers
class UserServiceIntegrationTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private UserRepository userRepository;
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Test
    @Transactional
    void shouldPersistUserInDatabase() {
        // Given
        CreateUserRequest request = CreateUserRequest.builder()
                .username("integrationtest")
                .email("integration@test.com")
                .password("password123")
                .build();
        
        // When
        UserDto userDto = userService.createUser(request);
        
        // Then
        assertThat(userDto.getId()).isNotNull();
        assertThat(userRepository.findById(userDto.getId())).isPresent();
    }
}
```

### 6.2 测试数据构建
```java
// 测试数据工厂类
public class TestDataFactory {
    
    public static User createUser() {
        return User.builder()
                .username("testuser")
                .email("test@example.com")
                .password("encodedPassword")
                .status(UserStatus.ACTIVE)
                .createdAt(LocalDateTime.now())
                .build();
    }
    
    public static User createUserWithId(Long id) {
        User user = createUser();
        user.setId(id);
        return user;
    }
    
    public static CreateUserRequest createCreateUserRequest() {
        return CreateUserRequest.builder()
                .username("newuser")
                .email("newuser@example.com")
                .password("password123")
                .firstName("John")
                .lastName("Doe")
                .build();
    }
    
    public static List<User> createMultipleUsers(int count) {
        List<User> users = new ArrayList<>();
        for (int i = 1; i <= count; i++) {
            users.add(createUserWithId((long) i));
        }
        return users;
    }
}

// 测试配置
@TestConfiguration
public class TestConfig {
    
    @Bean
    @Primary
    public PasswordEncoder testPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    @Primary
    public Clock testClock() {
        return Clock.fixed(Instant.parse("2023-01-01T10:00:00Z"), ZoneId.of("UTC"));
    }
}
```

## 七、日志和监控命名规范

### 7.1 日志记录规范
```java
// 服务层日志
@Service
@Slf4j
public class OrderServiceImpl implements OrderService {
    
    @Override
    @Transactional
    public OrderDto createOrder(CreateOrderRequest request) {
        log.info("Creating order for user: {}, items count: {}", 
                request.getUserId(), request.getItems().size());
        
        try {
            // 业务逻辑
            Order order = processOrderCreation(request);
            
            log.info("Order created successfully, order ID: {}", order.getId());
            return convertToDto(order);
            
        } catch (InsufficientInventoryException e) {
            log.warn("Insufficient inventory for order, user: {}, error: {}", 
                    request.getUserId(), e.getMessage());
            throw e;
        } catch (Exception e) {
            log.error("Failed to create order for user: {}", request.getUserId(), e);
            throw new OrderProcessingException("Failed to process order", e);
        }
    }
    
    @Cacheable(value = "orders", key = "#orderId")
    public OrderDto getOrderById(Long orderId) {
        log.debug("Fetching order by ID: {}", orderId);
        
        Optional<Order> orderOpt = orderRepository.findById(orderId);
        if (orderOpt.isEmpty()) {
            log.warn("Order not found, ID: {}", orderId);
            throw new OrderNotFoundException(orderId);
        }
        
        Order order = orderOpt.get();
        log.debug("Order found: ID={}, Status={}", order.getId(), order.getStatus());
        
        return convertToDto(order);
    }
}

// 控制器层日志
@RestController
@RequestMapping("/api/orders")
@Slf4j
public class OrderController {
    
    @PostMapping
    public ResponseEntity<OrderDto> createOrder(
            @AuthenticationPrincipal UserDetails userDetails,
            @Valid @RequestBody CreateOrderRequest request) {
        
        String username = userDetails.getUsername();
        log.info("Received order creation request from user: {}", username);
        
        try {
            OrderDto order = orderService.createOrder(request);
            log.info("Order created successfully for user: {}, order ID: {}", 
                    username, order.getId());
            
            return ResponseEntity.status(HttpStatus.CREATED).body(order);
            
        } catch (BusinessException e) {
            log.warn("Business exception for user {}: {}", username, e.getMessage());
            return ResponseEntity.badRequest().build();
        } catch (Exception e) {
            log.error("Unexpected error creating order for user: {}", username, e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
```

### 7.2 监控指标
```java
// Micrometer指标收集
@Component
public class OrderMetrics {
    
    private final Counter orderCreatedCounter;
    private final Counter orderFailedCounter;
    private final Timer orderProcessingTimer;
    private final Gauge activeOrdersGauge;
    
    public OrderMetrics(MeterRegistry meterRegistry, OrderService orderService) {
        this.orderCreatedCounter = Counter.builder("orders.created")
                .description("Number of orders created")
                .register(meterRegistry);
                
        this.orderFailedCounter = Counter.builder("orders.failed")
                .description("Number of failed orders")
                .register(meterRegistry);
                
        this.orderProcessingTimer = Timer.builder("orders.processing.time")
                .description("Order processing time")
                .register(meterRegistry);
                
        this.activeOrdersGauge = Gauge.builder("orders.active")
                .description("Number of active orders")
                .register(meterRegistry);
    }
    
    public void recordOrderCreated() {
        orderCreatedCounter.increment();
    }
    
    public void recordOrderFailed() {
        orderFailedCounter.increment();
    }
    
    public Timer.Sample startOrderProcessingTimer() {
        return Timer.start();
    }
    
    public void stopOrderProcessingTimer(Timer.Sample sample) {
        sample.stop(orderProcessingTimer);
    }
}

// 使用监控指标
@Service
public class OrderServiceImpl implements OrderService {
    
    @Autowired
    private OrderMetrics orderMetrics;
    
    @Override
    @Transactional
    public OrderDto createOrder(CreateOrderRequest request) {
        Timer.Sample sample = orderMetrics.startOrderProcessingTimer();
        
        try {
            Order order = processOrderCreation(request);
            orderMetrics.recordOrderCreated();
            return convertToDto(order);
            
        } catch (Exception e) {
            orderMetrics.recordOrderFailed();
            throw e;
        } finally {
            orderMetrics.stopOrderProcessingTimer(sample);
        }
    }
}
```

## 八、配置和环境变量命名

### 8.1 配置属性类
```java
// 配置属性绑定
@ConfigurationProperties(prefix = "app")
@Data
public class AppProperties {
    private Server server = new Server();
    private Database database = new Database();
    private Cache cache = new Cache();
    private Security security = new Security();
    
    @Data
    public static class Server {
        private String host = "localhost";
        private int port = 8080;
        private long timeoutMs = 30000;
        private boolean sslEnabled = false;
    }
    
    @Data
    public static class Database {
        private String url;
        private String username;
        private String password;
        private int maxPoolSize = 10;
        private long connectionTimeoutMs = 30000;
    }
    
    @Data
    public static class Cache {
        private boolean enabled = true;
        private String type = "redis";
        private long ttlSeconds = 3600;
        private int maxSize = 1000;
    }
    
    @Data
    public static class Security {
        private Jwt jwt = new Jwt();
        private Cors cors = new Cors();
        
        @Data
        public static class Jwt {
            private String secret;
            private long expirationMs = 86400000;
            private String issuer = "myapp";
        }
        
        @Data
        public static class Cors {
            private List<String> allowedOrigins = Arrays.asList("*");
            private List<String> allowedMethods = Arrays.asList("GET", "POST", "PUT", "DELETE");
            private boolean allowCredentials = true;
        }
    }
}

// 环境变量配置
@Configuration
@EnableConfigurationProperties(AppProperties.class)
public class AppConfig {
    
    @Value("${spring.profiles.active:dev}")
    private String activeProfile;
    
    @Value("${app.version:1.0.0}")
    private String appVersion;
    
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    @Profile("production")
    public RestTemplate productionRestTemplate() {
        // 生产环境专用配置
        return new RestTemplate();
    }
}
```

### 8.2 环境特定配置
```yaml
# application.yml
spring:
  application:
    name: ecommerce-platform
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

app:
  version: @project.version@
  server:
    host: ${SERVER_HOST:localhost}
    port: ${SERVER_PORT:8080}
    timeout-ms: 30000
  database:
    url: ${DATABASE_URL:jdbc:mysql://localhost:3306/ecommerce}
    username: ${DATABASE_USERNAME:root}
    password: ${DATABASE_PASSWORD:password}
    max-pool-size: 20
  cache:
    enabled: true
    type: redis
    ttl-seconds: 3600
  security:
    jwt:
      secret: ${JWT_SECRET:mySecretKey}
      expiration-ms: 86400000

# application-dev.yml
spring:
  datasource:
    hikari:
      maximum-pool-size: 5
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: update

logging:
  level:
    com.company: DEBUG
    org.springframework: INFO

# application-prod.yml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      connection-timeout: 30000
  jpa:
    show-sql: false
    hibernate:
      ddl-auto: validate

logging:
  level:
    com.company: WARN
    org.springframework: WARN
  pattern:
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: /var/log/ecommerce/application.log
```

## 九、API和DTO命名规范

### 9.1 RESTful API设计
```java
// API版本控制
@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "User Management", description = "User management operations")
public class UserController {
    
    @GetMapping
    @Operation(summary = "Get all users", description = "Retrieve a paginated list of users")
    public ResponseEntity<PagedResponse<UserDto>> getAllUsers(
            @Parameter(description = "Page number (0-based)") 
            @RequestParam(defaultValue = "0") int page,
            
            @Parameter(description = "Page size") 
            @RequestParam(defaultValue = "20") int size,
            
            @Parameter(description = "Sort field") 
            @RequestParam(defaultValue = "createdAt") String sortBy,
            
            @Parameter(description = "Sort direction") 
            @RequestParam(defaultValue = "desc") String sortDir) {
        
        Pageable pageable = PageRequest.of(page, size, 
                Sort.by(Sort.Direction.fromString(sortDir), sortBy));
        
        Page<UserDto> users = userService.getAllUsers(pageable);
        
        PagedResponse<UserDto> response = PagedResponse.<UserDto>builder()
                .content(users.getContent())
                .page(users.getNumber())
                .size(users.getSize())
                .totalElements(users.getTotalElements())
                .totalPages(users.getTotalPages())
                .build();
                
        return ResponseEntity.ok(response);
    }
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "Create user", description = "Create a new user account")
    public ResponseEntity<UserDto> createUser(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                description = "User creation request",
                required = true
            )
            @Valid @RequestBody CreateUserRequest request) {
        
        UserDto user = userService.createUser(request);
        return new ResponseEntity<>(user, HttpStatus.CREATED);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID", description = "Retrieve user details by ID")
    public ResponseEntity<UserDto> getUserById(
            @Parameter(description = "User ID", required = true)
            @PathVariable Long id) {
        
        UserDto user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }
}

// DTO类设计
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CreateUserRequest {
    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 50, message = "Username must be between 3 and 50 characters")
    private String username;
    
    @NotBlank(message = "Email is required")
    @Email(message = "Email should be valid")
    private String email;
    
    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;
    
    private String firstName;
    private String lastName;
    private String phoneNumber;
}

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDto {
    private Long id;
    private String username;
    private String email;
    private String firstName;
    private String lastName;
    private String phoneNumber;
    private UserStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    // 不包含敏感信息
    private String password; // 不序列化
}
```

## 十、最佳实践示例

### 10.1 生产环境启动类模板
```java
@SpringBootApplication
@EnableCaching
@EnableScheduling
@EnableAsync
public class EcommerceApplication {
    
    private static final Logger logger = LoggerFactory.getLogger(EcommerceApplication.class);
    
    public static void main(String[] args) {
        // 设置默认profile
        System.setProperty("spring.profiles.default", "dev");
        
        // 启动应用
        ConfigurableApplicationContext context = SpringApplication.run(EcommerceApplication.class, args);
        
        // 记录启动信息
        String appName = context.getEnvironment().getProperty("spring.application.name");
        String profile = Arrays.toString(context.getEnvironment().getActiveProfiles());
        
        logger.info("=========================================");
        logger.info("Application '{}' started successfully!", appName);
        logger.info("Active profiles: {}", profile);
        logger.info("=========================================");
    }
    
    @EventListener(ApplicationReadyEvent.class)
    public void onApplicationReady() {
        logger.info("Application is ready to serve requests");
    }
    
    @EventListener
    public void onApplicationFailed(ApplicationFailedEvent event) {
        logger.error("Application failed to start", event.getException());
    }
}
```

### 10.2 健康检查和监控
```java
@Component
public class CustomHealthIndicator implements HealthIndicator {
    
    @Autowired
    private DataSource dataSource;
    
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    @Override
    public Health health() {
        Map<String, Object> details = new HashMap<>();
        
        // 检查数据库连接
        boolean databaseHealthy = checkDatabaseConnection();
        details.put("database", databaseHealthy ? "healthy" : "unhealthy");
        
        // 检查Redis连接
        boolean redisHealthy = checkRedisConnection();
        details.put("redis", redisHealthy ? "healthy" : "unhealthy");
        
        // 检查外部服务
        boolean externalServicesHealthy = checkExternalServices();
        details.put("externalServices", externalServicesHealthy ? "healthy" : "degraded");
        
        if (databaseHealthy && redisHealthy && externalServicesHealthy) {
            return Health.up().withDetails(details).build();
        } else if (databaseHealthy && redisHealthy) {
            return Health.outOfService().withDetails(details).build();
        } else {
            return Health.down().withDetails(details).build();
        }
    }
    
    private boolean checkDatabaseConnection() {
        try {
            Connection conn = dataSource.getConnection();
            boolean isValid = conn.isValid(5);
            conn.close();
            return isValid;
        } catch (Exception e) {
            return false;
        }
    }
    
    private boolean checkRedisConnection() {
        try {
            redisTemplate.getConnectionFactory().getConnection().ping();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
    
    private boolean checkExternalServices() {
        // 检查第三方服务连通性
        return true;
    }
}

@RestController
@RequestMapping("/actuator")
public class HealthController {
    
    @Autowired
    private HealthEndpoint healthEndpoint;
    
    @GetMapping("/health")
    public ResponseEntity<Health> getHealth() {
        Health health = healthEndpoint.health();
        HttpStatus status = getStatusFromHealth(health);
        return ResponseEntity.status(status).body(health);
    }
    
    private HttpStatus getStatusFromHealth(Health health) {
        switch (health.getStatus().getCode()) {
            case "UP":
                return HttpStatus.OK;
            case "DOWN":
                return HttpStatus.SERVICE_UNAVAILABLE;
            case "OUT_OF_SERVICE":
                return HttpStatus.SERVICE_UNAVAILABLE;
            default:
                return HttpStatus.INTERNAL_SERVER_ERROR;
        }
    }
}
```

---

**注意事项：**
1. 遵循Java命名约定和Spring Boot最佳实践
2. 异常处理应该分层且具体，提供有意义的错误信息
3. 生产环境中必须包含完善的日志记录和监控指标
4. API设计应该遵循RESTful原则和OpenAPI规范
5. 配置管理应该支持多环境和外部化配置