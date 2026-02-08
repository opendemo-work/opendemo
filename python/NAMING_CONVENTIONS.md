# Python 技术栈命名大全

本文件定义了Python技术栈中各类模块、类、函数、变量等的标准命名规范，特别针对生产环境中的问题排查和解决方案场景。

## 一、项目结构命名规范

### 1.1 目录结构命名
```python
# 标准项目结构
project_root/
├── src/                          # 源代码目录
│   ├── api/                     # API相关代码
│   │   ├── routers/            # 路由定义
│   │   ├── schemas/            # 数据模式定义
│   │   └── dependencies/       # 依赖注入
│   ├── core/                   # 核心业务逻辑
│   │   ├── services/           # 业务服务层
│   │   ├── models/             # 数据模型
│   │   ├── repositories/       # 数据访问层
│   │   └── exceptions/         # 自定义异常
│   ├── utils/                  # 工具函数
│   │   ├── helpers/            # 辅助函数
│   │   ├── validators/         # 验证器
│   │   └── formatters/         # 格式化工具
│   ├── config/                 # 配置管理
│   │   ├── settings.py         # 设置配置
│   │   └── environment.py      # 环境配置
│   └── main.py                 # 应用入口
├── tests/                      # 测试目录
│   ├── unit/                   # 单元测试
│   ├── integration/            # 集成测试
│   └── conftest.py             # 测试配置
├── docs/                       # 文档目录
├── scripts/                    # 脚本目录
├── requirements/               # 依赖管理
│   ├── base.txt               # 基础依赖
│   ├── dev.txt                # 开发依赖
│   └── prod.txt               # 生产依赖
└── pyproject.toml             # 项目配置文件
```

### 1.2 模块命名规范
```python
# 包命名 - 全小写，单词间用下划线分隔
user_management/                # 用户管理
order_processing/               # 订单处理
payment_gateway/                # 支付网关
data_validation/                # 数据验证
email_notification/             # 邮件通知

# 模块文件命名 - 全小写，单词间用下划线分隔
user_controller.py              # 用户控制器
order_service.py                # 订单服务
database_manager.py             # 数据库管理器
config_loader.py                # 配置加载器
logger_factory.py               # 日志工厂

# 私有模块命名 - 下划线前缀
_internal_utils.py              # 内部工具
_helpers.py                     # 辅助函数
_config_parser.py               # 配置解析器
```

## 二、类和对象命名规范

### 2.1 类命名
```python
# 类名 - 首字母大写的驼峰命名法
class UserManager:
    """用户管理类"""
    pass

class OrderProcessor:
    """订单处理器"""
    pass

class DatabaseConnection:
    """数据库连接类"""
    pass

class EmailService:
    """邮件服务类"""
    pass

class PaymentGateway:
    """支付网关类"""
    pass

# 异常类命名 - Exception后缀
class UserNotFoundException(Exception):
    """用户未找到异常"""
    pass

class InvalidCredentialsException(Exception):
    """无效凭证异常"""
    pass

class DatabaseConnectionError(Exception):
    """数据库连接错误"""
    pass

class ValidationError(Exception):
    """验证错误"""
    pass

# 数据类命名
from dataclasses import dataclass

@dataclass
class User:
    """用户数据类"""
    id: int
    username: str
    email: str
    created_at: datetime

@dataclass
class Order:
    """订单数据类"""
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
```

### 2.2 实例变量命名
```python
# 实例变量 - 全小写，单词间用下划线分隔
class UserService:
    def __init__(self):
        self.database_connection = None
        self.logger = get_logger(__name__)
        self.cache_client = RedisCache()
        self.config_settings = load_config()
        
    def create_user(self, user_data):
        user_id = self._generate_user_id()
        created_user = self._save_user_to_database(user_data)
        self._send_welcome_email(created_user)
        return created_user

# 私有变量 - 下划线前缀
class DatabaseManager:
    def __init__(self):
        self._connection_pool = None
        self._retry_count = 0
        self._max_retries = 3
        self._logger = logging.getLogger(__name__)
```

## 三、函数和方法命名规范

### 3.1 函数命名
```python
# 函数名 - 全小写，单词间用下划线分隔
def calculate_total_amount(items):
    """计算总金额"""
    return sum(item.price * item.quantity for item in items)

def validate_email_address(email):
    """验证邮箱地址"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_notification_email(recipient, subject, body):
    """发送通知邮件"""
    # 邮件发送逻辑
    pass

def process_payment_transaction(order_id, payment_data):
    """处理支付交易"""
    # 支付处理逻辑
    pass

# 私有函数 - 下划线前缀
def _generate_unique_id():
    """生成唯一ID"""
    return str(uuid.uuid4())

def _sanitize_input_data(data):
    """清洗输入数据"""
    if isinstance(data, str):
        return data.strip()
    return data

def _log_error_details(error, context):
    """记录错误详情"""
    logger.error(f"Error in {context}: {str(error)}")
```

### 3.2 方法命名
```python
class OrderService:
    def create_order(self, order_data):
        """创建订单"""
        validated_data = self._validate_order_data(order_data)
        order = self._save_order_to_database(validated_data)
        self._trigger_order_created_event(order)
        return order
    
    def get_order_by_id(self, order_id):
        """根据ID获取订单"""
        order = self.repository.find_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Order {order_id} not found")
        return order
    
    def update_order_status(self, order_id, new_status):
        """更新订单状态"""
        order = self.get_order_by_id(order_id)
        old_status = order.status
        order.status = new_status
        self._save_order(order)
        self._log_status_change(order_id, old_status, new_status)
        return order
    
    def cancel_order(self, order_id, reason):
        """取消订单"""
        order = self.get_order_by_id(order_id)
        if order.status in ['shipped', 'delivered']:
            raise OrderCannotBeCancelledException("Order cannot be cancelled")
        
        order.status = 'cancelled'
        order.cancellation_reason = reason
        self._save_order(order)
        self._refund_payment(order)
        self._release_inventory(order.items)
        return order
    
    # 私有方法
    def _validate_order_data(self, order_data):
        """验证订单数据"""
        # 验证逻辑
        pass
    
    def _save_order(self, order):
        """保存订单"""
        # 保存逻辑
        pass
    
    def _trigger_order_created_event(self, order):
        """触发订单创建事件"""
        # 事件触发逻辑
        pass
```

## 四、变量和常量命名规范

### 4.1 常量命名
```python
# 常量 - 全大写，单词间用下划线分隔
MAX_RETRY_ATTEMPTS = 3
DEFAULT_PAGE_SIZE = 20
API_BASE_URL = "https://api.example.com"
DATABASE_CONNECTION_TIMEOUT = 30
CACHE_TTL_SECONDS = 3600

# 配置常量
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 枚举常量
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
```

### 4.2 变量命名
```python
# 局部变量
def process_user_registration(user_data):
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')
    
    # 验证数据
    validation_errors = []
    if not username:
        validation_errors.append("Username is required")
    if not validate_email(email):
        validation_errors.append("Invalid email format")
    
    if validation_errors:
        raise ValidationError(validation_errors)
    
    # 处理注册
    hashed_password = hash_password(password)
    user_record = create_user_record(username, email, hashed_password)
    send_welcome_email(user_record.email)
    
    return user_record

# 全局变量 - 尽量避免，如需使用加注释说明
# 全局数据库连接池
_database_connection_pool = None

# 全局配置对象
_app_config = None

# 全局日志记录器
_logger = None
```

## 五、装饰器和上下文管理器命名

### 5.1 装饰器命名
```python
# 装饰器函数 - 全小写，单词间用下划线分隔
def retry_on_failure(max_retries=3, delay=1):
    """失败重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # 指数退避
                    else:
                        logger.warning(f"Function {func.__name__} failed after {max_retries} attempts")
            raise last_exception
        return wrapper
    return decorator

def rate_limit(calls_per_minute=60):
    """速率限制装饰器"""
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理过期的调用记录
            calls[:] = [call_time for call_time in calls if now - call_time < 60]
            
            if len(calls) >= calls_per_minute:
                raise RateLimitExceededException("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_execution_time(func):
    """执行时间记录装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {str(e)}")
            raise
    return wrapper

# 使用示例
@retry_on_failure(max_retries=3, delay=2)
@log_execution_time
def fetch_external_api_data(endpoint):
    """获取外部API数据"""
    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()
    return response.json()

@rate_limit(calls_per_minute=100)
def process_user_request(user_id, request_data):
    """处理用户请求"""
    # 处理逻辑
    pass
```

### 5.2 上下文管理器命名
```python
# 上下文管理器类
class DatabaseTransaction:
    """数据库事务上下文管理器"""
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.transaction = None
    
    def __enter__(self):
        self.transaction = self.db_connection.begin()
        return self.transaction
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.transaction.commit()
            logger.info("Database transaction committed successfully")
        else:
            self.transaction.rollback()
            logger.warning(f"Database transaction rolled back due to: {exc_val}")
        return False

class TimerContext:
    """计时上下文管理器"""
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time.time() - self.start_time
        if exc_type is None:
            logger.info(f"{self.operation_name} completed in {elapsed_time:.4f} seconds")
        else:
            logger.error(f"{self.operation_name} failed after {elapsed_time:.4f} seconds: {exc_val}")
        return False

class TemporaryDirectory:
    """临时目录上下文管理器"""
    
    def __init__(self, prefix="temp_"):
        self.prefix = prefix
        self.temp_dir = None
    
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(prefix=self.prefix)
        return self.temp_dir
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        return False

# 使用示例
def process_large_file(file_path):
    """处理大文件"""
    with TimerContext("File Processing") as timer:
        with TemporaryDirectory("file_processing_") as temp_dir:
            # 文件处理逻辑
            extracted_data = extract_file_contents(file_path, temp_dir)
            processed_data = process_extracted_data(extracted_data)
            return processed_data

def update_user_profile(user_id, profile_data):
    """更新用户档案"""
    with DatabaseTransaction(get_db_connection()) as transaction:
        # 更新用户信息
        update_user_query = "UPDATE users SET name = %s, email = %s WHERE id = %s"
        transaction.execute(update_user_query, (
            profile_data['name'], 
            profile_data['email'], 
            user_id
        ))
        
        # 记录变更历史
        history_query = """
            INSERT INTO user_profile_history 
            (user_id, changed_field, old_value, new_value, changed_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        for field, new_value in profile_data.items():
            transaction.execute(history_query, (
                user_id, field, None, new_value
            ))
```

## 六、类型提示和文档字符串

### 6.1 类型提示
```python
from typing import List, Dict, Optional, Union, Callable, Any
from datetime import datetime
from decimal import Decimal

# 函数类型提示
def calculate_discount(
    amount: Decimal, 
    discount_type: str, 
    user_level: Optional[str] = None
) -> Decimal:
    """计算折扣金额
    
    Args:
        amount: 原始金额
        discount_type: 折扣类型 ('percentage' 或 'fixed')
        user_level: 用户等级 (可选)
    
    Returns:
        折扣后的金额
    
    Raises:
        ValueError: 当折扣类型无效时
    """
    if discount_type == 'percentage':
        return amount * Decimal('0.9')  # 10% 折扣
    elif discount_type == 'fixed':
        return max(amount - Decimal('10'), Decimal('0'))  # 固定减免10元
    else:
        raise ValueError(f"Invalid discount type: {discount_type}")

# 类型别名
UserId = int
EmailAddress = str
OrderList = List[Dict[str, Any]]

class UserService:
    def get_user_orders(self, user_id: UserId) -> OrderList:
        """获取用户订单列表"""
        # 实现逻辑
        pass
    
    def send_email(self, email: EmailAddress, subject: str, body: str) -> bool:
        """发送邮件"""
        # 实现逻辑
        pass

# 泛型使用
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def find_by_id(self, id: int) -> Optional[T]:
        """根据ID查找实体"""
        pass
    
    def save(self, entity: T) -> T:
        """保存实体"""
        pass

class UserRepository(Repository[User]):
    """用户仓储实现"""
    pass
```

### 6.2 文档字符串规范
```python
class OrderProcessor:
    """
    订单处理器类
    
    负责处理订单的创建、验证、支付和发货等全流程操作。
    提供完整的订单生命周期管理功能。
    
    Attributes:
        payment_service: 支付服务实例
        inventory_service: 库存服务实例
        notification_service: 通知服务实例
    """
    
    def __init__(
        self, 
        payment_service: 'PaymentService',
        inventory_service: 'InventoryService',
        notification_service: 'NotificationService'
    ):
        """
        初始化订单处理器
        
        Args:
            payment_service: 支付服务实例
            inventory_service: 库存服务实例  
            notification_service: 通知服务实例
        """
        self.payment_service = payment_service
        self.inventory_service = inventory_service
        self.notification_service = notification_service
        self.logger = logging.getLogger(__name__)
    
    def process_new_order(self, order_data: Dict[str, Any]) -> 'Order':
        """
        处理新订单
        
        执行完整的订单处理流程，包括：
        1. 验证订单数据
        2. 检查库存可用性
        3. 处理支付
        4. 更新库存
        5. 发送确认通知
        
        Args:
            order_data: 订单数据字典，包含商品信息、用户信息等
            
        Returns:
            处理完成的订单对象
            
        Raises:
            ValidationError: 当订单数据验证失败时
            InsufficientInventoryError: 当库存不足时
            PaymentProcessingError: 当支付处理失败时
            
        Example:
            >>> processor = OrderProcessor(payment_svc, inventory_svc, notify_svc)
            >>> order = processor.process_new_order({
            ...     'user_id': 123,
            ...     'items': [{'product_id': 1, 'quantity': 2}],
            ...     'shipping_address': '北京市朝阳区xxx'
            ... })
            >>> print(order.status)
            'confirmed'
        """
        try:
            # 1. 验证订单数据
            validated_data = self._validate_order_data(order_data)
            
            # 2. 检查库存
            self._check_inventory_availability(validated_data['items'])
            
            # 3. 创建订单记录
            order = self._create_order_record(validated_data)
            
            # 4. 处理支付
            payment_result = self.payment_service.process_payment(
                order.id, 
                validated_data['payment_info']
            )
            
            # 5. 更新库存
            self.inventory_service.reserve_items(validated_data['items'])
            
            # 6. 更新订单状态
            order.status = 'confirmed'
            self._save_order(order)
            
            # 7. 发送确认通知
            self.notification_service.send_order_confirmation(order)
            
            self.logger.info(f"Order {order.id} processed successfully")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to process order: {str(e)}")
            raise
```

## 七、配置和环境管理

### 7.1 配置类设计
```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class DatabaseConfig:
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    database: str = "myapp"
    username: str = "postgres"
    password: str = ""
    pool_size: int = 10
    max_overflow: int = 20
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """从环境变量创建配置"""
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=os.getenv("DB_NAME", "myapp"),
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20"))
        )

@dataclass
class RedisConfig:
    """Redis配置"""
    host: str = "localhost"
    port: int = 6379
    database: int = 0
    password: Optional[str] = None
    ssl: bool = False
    
    @classmethod
    def from_env(cls) -> 'RedisConfig':
        """从环境变量创建配置"""
        return cls(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            database=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD"),
            ssl=os.getenv("REDIS_SSL", "false").lower() == "true"
        )

@dataclass
class AppConfig:
    """应用配置"""
    debug: bool = False
    secret_key: str = "dev-secret-key"
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"
    
    database: DatabaseConfig = None
    redis: RedisConfig = None
    
    def __post_init__(self):
        if self.database is None:
            self.database = DatabaseConfig.from_env()
        if self.redis is None:
            self.redis = RedisConfig.from_env()
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """从环境变量创建完整配置"""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            api_prefix=os.getenv("API_PREFIX", "/api/v1")
        )

# 配置使用示例
config = AppConfig.from_env()

# 数据库连接
engine = create_engine(
    f"postgresql://{config.database.username}:{config.database.password}@"
    f"{config.database.host}:{config.database.port}/{config.database.database}",
    pool_size=config.database.pool_size,
    max_overflow=config.database.max_overflow
)

# Redis连接
redis_client = redis.Redis(
    host=config.redis.host,
    port=config.redis.port,
    db=config.redis.database,
    password=config.redis.password,
    ssl=config.redis.ssl
)
```

### 7.2 环境变量验证
```python
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EnvironmentValidator:
    """环境变量验证器"""
    
    REQUIRED_VARIABLES = [
        'DATABASE_URL',
        'SECRET_KEY',
        'REDIS_URL'
    ]
    
    OPTIONAL_VARIABLES = {
        'DEBUG': 'false',
        'LOG_LEVEL': 'INFO',
        'API_PORT': '8000',
        'WORKER_COUNT': '4'
    }
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """验证环境变量并返回配置字典"""
        config = {}
        
        # 检查必需变量
        missing_vars = []
        for var in cls.REQUIRED_VARIABLES:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                config[var] = value
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # 设置可选变量默认值
        for var, default in cls.OPTIONAL_VARIABLES.items():
            config[var] = os.getenv(var, default)
        
        # 验证特定变量格式
        cls._validate_database_url(config['DATABASE_URL'])
        cls._validate_secret_key(config['SECRET_KEY'])
        cls._validate_port(config['API_PORT'])
        
        logger.info("Environment validation completed successfully")
        return config
    
    @staticmethod
    def _validate_database_url(url: str) -> None:
        """验证数据库URL格式"""
        if not url.startswith(('postgresql://', 'mysql://', 'sqlite:///')):
            raise ValueError(f"Invalid database URL format: {url}")
    
    @staticmethod
    def _validate_secret_key(key: str) -> None:
        """验证密钥强度"""
        if len(key) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
    
    @staticmethod
    def _validate_port(port: str) -> None:
        """验证端口号"""
        try:
            port_num = int(port)
            if not (1 <= port_num <= 65535):
                raise ValueError("Port must be between 1 and 65535")
        except ValueError:
            raise ValueError(f"Invalid port number: {port}")

# 使用示例
try:
    app_config = EnvironmentValidator.validate()
    print("Configuration loaded successfully:")
    for key, value in app_config.items():
        # 不打印敏感信息
        if 'KEY' in key or 'PASSWORD' in key:
            print(f"{key}: {'*' * len(str(value))}")
        else:
            print(f"{key}: {value}")
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)
```

## 八、测试相关命名规范

### 8.1 测试文件命名
```python
# 测试文件命名 - test_前缀
test_user_service.py            # 用户服务测试
test_order_processor.py         # 订单处理器测试
test_database_manager.py        # 数据库管理器测试
test_api_endpoints.py           # API端点测试

# 测试目录结构
tests/
├── unit/
│   ├── test_models/
│   │   ├── test_user_model.py
│   │   └── test_order_model.py
│   ├── test_services/
│   │   ├── test_user_service.py
│   │   └── test_order_service.py
│   └── test_utils/
│       ├── test_validators.py
│       └── test_helpers.py
├── integration/
│   ├── test_database_integration.py
│   ├── test_api_integration.py
│   └── test_external_services.py
└── conftest.py                 # 测试配置和fixture
```

### 8.2 测试函数命名
```python
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

class TestUserService:
    """用户服务测试类"""
    
    def test_create_user_success(self, user_service, valid_user_data):
        """测试成功创建用户"""
        # Arrange
        mock_repo = Mock()
        user_service.user_repository = mock_repo
        mock_repo.create.return_value = {"id": 1, **valid_user_data}
        
        # Act
        result = user_service.create_user(valid_user_data)
        
        # Assert
        assert result["id"] == 1
        assert result["username"] == valid_user_data["username"]
        mock_repo.create.assert_called_once_with(valid_user_data)
    
    def test_create_user_invalid_data(self, user_service, invalid_user_data):
        """测试创建用户时数据验证失败"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(invalid_user_data)
        
        assert "username" in str(exc_info.value)
    
    def test_get_user_by_id_found(self, user_service):
        """测试根据ID找到用户"""
        # Arrange
        user_id = 123
        expected_user = {"id": user_id, "username": "testuser"}
        mock_repo = Mock()
        user_service.user_repository = mock_repo
        mock_repo.find_by_id.return_value = expected_user
        
        # Act
        result = user_service.get_user_by_id(user_id)
        
        # Assert
        assert result == expected_user
        mock_repo.find_by_id.assert_called_once_with(user_id)
    
    def test_get_user_by_id_not_found(self, user_service):
        """测试根据ID未找到用户"""
        # Arrange
        user_id = 999
        mock_repo = Mock()
        user_service.user_repository = mock_repo
        mock_repo.find_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UserNotFoundException):
            user_service.get_user_by_id(user_id)

class TestOrderProcessor:
    """订单处理器测试类"""
    
    @pytest.mark.parametrize("payment_method,expected_status", [
        ("credit_card", "confirmed"),
        ("paypal", "confirmed"),
        ("bank_transfer", "pending"),
    ])
    def test_process_payment_different_methods(
        self, order_processor, order_data, payment_method, expected_status
    ):
        """测试不同支付方式的处理"""
        # Arrange
        order_data["payment_method"] = payment_method
        mock_payment_service = Mock()
        order_processor.payment_service = mock_payment_service
        mock_payment_service.process_payment.return_value = {"status": "success"}
        
        # Act
        result = order_processor.process_new_order(order_data)
        
        # Assert
        assert result.status == expected_status
        mock_payment_service.process_payment.assert_called_once()
    
    @patch('src.services.order_service.datetime')
    def test_order_creation_timestamp(self, mock_datetime, order_processor, order_data):
        """测试订单创建时间戳"""
        # Arrange
        fixed_time = datetime(2023, 12, 1, 10, 30, 0)
        mock_datetime.now.return_value = fixed_time
        
        # Act
        result = order_processor.process_new_order(order_data)
        
        # Assert
        assert result.created_at == fixed_time
```

## 九、日志和监控命名规范

### 9.1 日志记录
```python
import logging
import logging.config
from typing import Dict, Any
import json

class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.extra_fields = {}
    
    def add_context(self, **fields):
        """添加上下文字段"""
        self.extra_fields.update(fields)
    
    def info(self, message: str, **extra):
        """记录信息级别日志"""
        self._log(logging.INFO, message, extra)
    
    def warning(self, message: str, **extra):
        """记录警告级别日志"""
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, **extra):
        """记录错误级别日志"""
        self._log(logging.ERROR, message, extra)
    
    def debug(self, message: str, **extra):
        """记录调试级别日志"""
        self._log(logging.DEBUG, message, extra)
    
    def _log(self, level: int, message: str, extra: Dict[str, Any]):
        """记录结构化日志"""
        log_data = {
            "message": message,
            "timestamp": self._get_timestamp(),
            **self.extra_fields,
            **extra
        }
        
        # 生产环境使用JSON格式
        if self.logger.level <= logging.DEBUG:
            self.logger.log(level, message, extra=log_data)
        else:
            self.logger.log(level, json.dumps(log_data))

# 配置日志
def setup_logging():
    """设置日志配置"""
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json'
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'src': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(config)

# 使用示例
setup_logging()
logger = StructuredLogger(__name__)

def process_user_order(user_id: int, order_data: Dict):
    """处理用户订单"""
    # 添加上下文
    logger.add_context(
        user_id=user_id,
        request_id=get_request_id(),
        correlation_id=get_correlation_id()
    )
    
    try:
        logger.info("Starting order processing", 
                   order_items=len(order_data.get('items', [])),
                   total_amount=order_data.get('total_amount'))
        
        # 订单处理逻辑
        order = create_order(user_id, order_data)
        
        logger.info("Order created successfully",
                   order_id=order.id,
                   status=order.status)
        
        return order
        
    except ValidationError as e:
        logger.warning("Order validation failed",
                      error=str(e),
                      invalid_fields=e.fields)
        raise
        
    except Exception as e:
        logger.error("Order processing failed",
                    error=str(e),
                    stack_trace=traceback.format_exc())
        raise
```

### 9.2 监控指标收集
```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from typing import Callable
from functools import wraps

class MetricsCollector:
    """监控指标收集器"""
    
    # HTTP请求指标
    http_requests_total = Counter(
        'http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status_code']
    )
    
    http_request_duration = Histogram(
        'http_request_duration_seconds',
        'HTTP request duration in seconds',
        ['method', 'endpoint'],
        buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float('inf'))
    )
    
    # 业务指标
    user_registrations_total = Counter(
        'user_registrations_total',
        'Total user registrations',
        ['source']
    )
    
    order_processing_time = Summary(
        'order_processing_seconds',
        'Time spent processing orders',
        ['order_type']
    )
    
    active_users = Gauge(
        'active_users_count',
        'Number of currently active users'
    )
    
    database_connections = Gauge(
        'database_connections_count',
        'Number of active database connections',
        ['state']
    )

# 装饰器用于自动收集指标
def monitor_http_endpoint(func: Callable):
    """HTTP端点监控装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 获取请求信息
        request = kwargs.get('request') or (args[0] if args else None)
        if hasattr(request, 'method') and hasattr(request, 'url'):
            method = request.method
            endpoint = str(request.url.path)
        else:
            method = 'UNKNOWN'
            endpoint = func.__name__
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 记录成功指标
            status_code = getattr(result, 'status_code', 200)
            MetricsCollector.http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status_code=status_code
            ).inc()
            
            return result
            
        except Exception as e:
            # 记录错误指标
            MetricsCollector.http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status_code=500
            ).inc()
            raise
            
        finally:
            # 记录耗时
            duration = time.time() - start_time
            MetricsCollector.http_request_duration.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    return wrapper

def monitor_business_operation(operation_name: str, **labels):
    """业务操作监控装饰器"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # 记录成功操作
                if operation_name == 'user_registration':
                    MetricsCollector.user_registrations_total.labels(
                        source=labels.get('source', 'unknown')
                    ).inc()
                
                return result
                
            except Exception as e:
                # 记录失败操作
                logger.error(f"Business operation failed: {operation_name}", 
                           error=str(e))
                raise
                
            finally:
                # 记录操作耗时
                duration = time.time() - start_time
                if operation_name == 'order_processing':
                    MetricsCollector.order_processing_time.labels(
                        order_type=labels.get('order_type', 'standard')
                    ).observe(duration)
        
        return wrapper
    return decorator

# 使用示例
@monitor_http_endpoint
async def create_user_endpoint(request):
    """创建用户端点"""
    user_data = await request.json()
    user = await user_service.create_user(user_data)
    return JSONResponse({"id": user.id, "username": user.username})

@monitor_business_operation('order_processing', order_type='premium')
def process_premium_order(order_data):
    """处理高级订单"""
    # 订单处理逻辑
    pass
```

## 十、最佳实践示例

### 10.1 生产环境应用模板
```python
# main.py - 生产环境应用入口
import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.config.settings import settings
from src.core.exceptions import (
    setup_exception_handlers,
    ValidationError,
    DatabaseError
)
from src.utils.logging import setup_logging, get_logger
from src.utils.metrics import setup_metrics
from src.api.routers import user_router, order_router, auth_router

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    # 启动时执行
    logger.info("Starting application...")
    
    try:
        # 初始化数据库连接
        from src.core.database import database
        await database.connect()
        logger.info("Database connected successfully")
        
        # 初始化缓存
        from src.core.cache import cache
        await cache.initialize()
        logger.info("Cache initialized successfully")
        
        # 启动后台任务
        from src.core.background import start_background_tasks
        start_background_tasks()
        logger.info("Background tasks started")
        
        yield
        
    finally:
        # 关闭时执行
        logger.info("Shutting down application...")
        
        # 关闭数据库连接
        await database.disconnect()
        logger.info("Database disconnected")
        
        # 关闭缓存连接
        await cache.close()
        logger.info("Cache connection closed")

def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Production-ready Python API",
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )
    
    # 中间件配置
    setup_middleware(app)
    
    # 异常处理
    setup_exception_handlers(app)
    
    # 路由注册
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(order_router, prefix="/api/v1/orders", tags=["Orders"])
    
    # 健康检查端点
    @app.get("/health")
    async def health_check():
        """健康检查端点"""
        return {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "version": settings.VERSION
        }
    
    return app

def setup_middleware(app: FastAPI) -> None:
    """设置中间件"""
    # CORS配置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 可信主机配置
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    
    # 请求日志中间件
    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        start_time = asyncio.get_event_loop().time()
        
        try:
            response = await call_next(request)
            process_time = asyncio.get_event_loop().time() - start_time
            
            logger.info(
                "Request processed",
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                process_time=f"{process_time:.4f}s",
                client_host=request.client.host if request.client else "unknown"
            )
            
            return response
            
        except Exception as e:
            process_time = asyncio.get_event_loop().time() - start_time
            logger.error(
                "Request processing failed",
                method=request.method,
                url=str(request.url),
                error=str(e),
                process_time=f"{process_time:.4f}s"
            )
            raise

def setup_signal_handlers() -> None:
    """设置信号处理器"""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    # 设置日志
    setup_logging()
    
    # 设置信号处理
    setup_signal_handlers()
    
    # 设置监控
    setup_metrics()
    
    # 创建应用
    app = create_app()
    
    # 运行应用
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKER_COUNT,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=False,  # 使用自定义日志
    )
```

### 10.2 错误处理和恢复机制
```python
# core/exceptions.py - 错误处理模块
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger(__name__)

class AppException(Exception):
    """应用基础异常类"""
    def __init__(
        self, 
        message: str, 
        error_code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AppException):
    """验证错误"""
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details={"field": field} if field else {}
        )

class AuthenticationError(AppException):
    """认证错误"""
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )

class AuthorizationError(AppException):
    """授权错误"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403
        )

class NotFoundError(AppException):
    """资源未找到错误"""
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            error_code="NOT_FOUND_ERROR",
            status_code=404
        )

class DatabaseError(AppException):
    """数据库错误"""
    def __init__(self, message: str, query: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details={"query": query} if query else {}
        )

def setup_exception_handlers(app) -> None:
    """设置全局异常处理器"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """处理应用自定义异常"""
        logger.warning(
            "Application error occurred",
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            url=str(request.url),
            method=request.method,
            details=exc.details
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """处理HTTP异常"""
        logger.info(
            "HTTP exception occurred",
            status_code=exc.status_code,
            detail=exc.detail,
            url=str(request.url),
            method=request.method
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail,
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """处理未预期的异常"""
        logger.error(
            "Unexpected error occurred",
            error=str(exc),
            stack_trace=traceback.format_exc(),
            url=str(request.url),
            method=request.method
        )
        
        # 生产环境不暴露详细错误信息
        error_message = "Internal server error" if not app.debug else str(exc)
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": error_message,
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
        )

# 使用示例
async def create_user_service(user_data: Dict) -> User:
    """创建用户服务"""
    try:
        # 验证输入数据
        if not user_data.get('email'):
            raise ValidationError("Email is required", field="email")
        
        if not validate_email_format(user_data['email']):
            raise ValidationError("Invalid email format", field="email")
        
        # 检查用户是否已存在
        existing_user = await user_repository.find_by_email(user_data['email'])
        if existing_user:
            raise ValidationError("User with this email already exists", field="email")
        
        # 创建用户
        user = await user_repository.create(user_data)
        
        # 发送欢迎邮件
        try:
            await email_service.send_welcome_email(user.email)
        except Exception as e:
            logger.warning(f"Failed to send welcome email: {e}")
            # 不中断主流程
        
        logger.info("User created successfully", user_id=user.id)
        return user
        
    except DatabaseError as e:
        logger.error("Database error during user creation", error=str(e))
        raise AppException("Failed to create user due to database error")
    
    except Exception as e:
        logger.error("Unexpected error during user creation", error=str(e))
        raise AppException("Failed to create user")
```

---

**注意事项：**
1. 遵循PEP 8 Python编码规范和命名约定
2. 使用类型提示提高代码可读性和IDE支持
3. 编写完整的文档字符串，便于团队协作和维护
4. 合理使用装饰器和上下文管理器简化代码
5. 生产环境中必须包含完善的错误处理和日志记录