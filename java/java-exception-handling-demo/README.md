# Java异常处理机制演示

## 🎯 学习目标

通过本案例你将掌握：
- Java异常体系结构和分类
- try-catch-finally语句的使用
- throws和throw关键字的应用
- 自定义异常类的设计
- 异常链和包装异常的处理
- 最佳异常处理实践

## 🛠️ 环境准备

### 系统要求
- JDK 11或更高版本
- 支持Java的IDE或文本编辑器
- Java基础语法知识

### 依赖检查
```bash
# 验证Java环境
java -version
javac -version
```

## 📁 项目结构

```
java-exception-handling-demo/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   ├── ExceptionBasicsDemo.java
│                   ├── CustomExceptionDemo.java
│                   ├── ExceptionBestPracticesDemo.java
│                   └── BankAccount.java
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：创建项目结构
```bash
mkdir java-exception-handling-demo
cd java-exception-handling-demo
mkdir -p src/main/java/com/example
```

### 步骤2：创建异常基础演示类
创建 `src/main/java/com/example/ExceptionBasicsDemo.java` 文件：

```java
package com.example;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.sql.SQLException;
import java.util.InputMismatchException;
import java.util.Scanner;

/**
 * Java异常处理基础演示类
 * 展示异常的基本概念、分类和处理方式
 */
public class ExceptionBasicsDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java异常处理基础演示 ===\n");
        
        // 1. 异常体系结构演示
        demonstrateExceptionHierarchy();
        
        // 2. try-catch-finally基础用法
        demonstrateTryCatchFinally();
        
        // 3. 多重catch块演示
        demonstrateMultipleCatchBlocks();
        
        // 4. throws关键字演示
        demonstrateThrowsKeyword();
        
        // 5. throw关键字演示
        demonstrateThrowKeyword();
    }
    
    /**
     * 演示Java异常体系结构
     */
    private static void demonstrateExceptionHierarchy() {
        System.out.println("1. Java异常体系结构:");
        System.out.println("Throwable");
        System.out.println("├── Error (系统级错误)");
        System.out.println("│   ├── OutOfMemoryError");
        System.out.println("│   ├── StackOverflowError");
        System.out.println("│   └── ...");
        System.out.println("└── Exception (程序异常)");
        System.out.println("    ├── RuntimeException (运行时异常)");
        System.out.println("    │   ├── NullPointerException");
        System.out.println("    │   ├── ArrayIndexOutOfBoundsException");
        System.out.println("    │   ├── IllegalArgumentException");
        System.out.println("    │   └── ...");
        System.out.println("    └── CheckedException (检查异常)");
        System.out.println("        ├── IOException");
        System.out.println("        ├── SQLException");
        System.out.println("        ├── ClassNotFoundException");
        System.out.println("        └── ...");
        System.out.println();
    }
    
    /**
     * 演示try-catch-finally的基本用法
     */
    private static void demonstrateTryCatchFinally() {
        System.out.println("2. try-catch-finally基本用法:");
        
        // 基本的异常捕获
        try {
            int result = 10 / 0; // 会产生ArithmeticException
            System.out.println("结果: " + result);
        } catch (ArithmeticException e) {
            System.out.println("捕获到算术异常: " + e.getMessage());
            System.out.println("异常类型: " + e.getClass().getSimpleName());
        } finally {
            System.out.println("finally块总是执行");
        }
        
        // 数组越界异常
        try {
            int[] numbers = {1, 2, 3};
            System.out.println("访问数组元素: " + numbers[5]); // ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组越界异常: " + e.getMessage());
        }
        
        // 空指针异常
        try {
            String str = null;
            System.out.println("字符串长度: " + str.length()); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("空指针异常: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    /**
     * 演示多重catch块的使用
     */
    private static void demonstrateMultipleCatchBlocks() {
        System.out.println("3. 多重catch块演示:");
        
        Scanner scanner = new Scanner(System.in);
        
        try {
            System.out.print("请输入一个数字: ");
            int number = scanner.nextInt();
            
            System.out.print("请输入除数: ");
            int divisor = scanner.nextInt();
            
            int result = number / divisor;
            System.out.println("结果: " + result);
            
            // 模拟数组访问
            int[] array = {1, 2, 3};
            System.out.println("数组元素: " + array[number]); // 可能越界
            
        } catch (InputMismatchException e) {
            System.out.println("输入格式错误: 请输入有效的整数");
        } catch (ArithmeticException e) {
            System.out.println("算术错误: " + e.getMessage());
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组越界: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("其他异常: " + e.getMessage());
        } finally {
            scanner.close();
            System.out.println("资源已关闭");
        }
        
        System.out.println();
    }
    
    /**
     * 演示throws关键字的使用
     */
    private static void demonstrateThrowsKeyword() {
        System.out.println("4. throws关键字演示:");
        
        try {
            readFile("nonexistent.txt");
        } catch (FileNotFoundException e) {
            System.out.println("文件未找到: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }
        
        try {
            connectToDatabase();
        } catch (SQLException e) {
            System.out.println("数据库连接失败: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    /**
     * 演示throw关键字的使用
     */
    private static void demonstrateThrowKeyword() {
        System.out.println("5. throw关键字演示:");
        
        // 抛出自定义异常
        try {
            validateAge(15);
        } catch (IllegalArgumentException e) {
            System.out.println("年龄验证失败: " + e.getMessage());
        }
        
        // 抛出运行时异常
        try {
            processUserData(null);
        } catch (NullPointerException e) {
            System.out.println("用户数据处理异常: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    // 模拟文件读取方法
    private static void readFile(String filename) throws FileNotFoundException, IOException {
        FileInputStream fis = new FileInputStream(filename);
        // 实际的文件处理逻辑...
        fis.close();
        System.out.println("文件读取成功: " + filename);
    }
    
    // 模拟数据库连接方法
    private static void connectToDatabase() throws SQLException {
        // 模拟数据库连接失败
        throw new SQLException("无法连接到数据库服务器");
    }
    
    // 年龄验证方法
    private static void validateAge(int age) {
        if (age < 18) {
            throw new IllegalArgumentException("年龄必须大于等于18岁，当前年龄: " + age);
        }
        System.out.println("年龄验证通过: " + age);
    }
    
    // 用户数据处理方法
    private static void processUserData(String userData) {
        if (userData == null) {
            throw new NullPointerException("用户数据不能为空");
        }
        System.out.println("处理用户数据: " + userData);
    }
}
```

### 步骤3：创建自定义异常演示类
创建 `src/main/java/com/example/CustomExceptionDemo.java` 文件：

```java
package com.example;

/**
 * 自定义异常演示类
 * 展示如何创建和使用自定义异常类
 */
public class CustomExceptionDemo {
    
    public static void main(String[] args) {
        System.out.println("=== 自定义异常演示 ===\n");
        
        BankAccount account = new BankAccount("123456", 1000.0);
        
        // 正常操作
        try {
            account.deposit(500.0);
            System.out.println("存款成功，余额: $" + account.getBalance());
        } catch (BankOperationException e) {
            System.out.println("操作失败: " + e.getMessage());
        }
        
        // 异常操作演示
        demonstrateCustomExceptions(account);
        
        // 异常链演示
        demonstrateExceptionChaining();
    }
    
    /**
     * 演示自定义异常的使用
     */
    private static void demonstrateCustomExceptions(BankAccount account) {
        System.out.println("\n1. 自定义异常使用演示:");
        
        // 余额不足异常
        try {
            account.withdraw(2000.0);
        } catch (InsufficientFundsException e) {
            System.out.println("取款失败 - " + e.getMessage());
            System.out.println("账户余额: $" + e.getCurrentBalance());
            System.out.println("尝试取款: $" + e.getWithdrawAmount());
        }
        
        // 无效金额异常
        try {
            account.deposit(-100.0);
        } catch (InvalidAmountException e) {
            System.out.println("存款失败 - " + e.getMessage());
            System.out.println("无效金额: $" + e.getAmount());
        }
        
        // 账户冻结异常
        try {
            account.freezeAccount();
            account.withdraw(100.0);
        } catch (AccountFrozenException e) {
            System.out.println("操作受限 - " + e.getMessage());
        }
    }
    
    /**
     * 演示异常链的使用
     */
    private static void demonstrateExceptionChaining() {
        System.out.println("\n2. 异常链示例:");
        
        try {
            processDataFromFile("config.txt");
        } catch (DataProcessingException e) {
            System.out.println("数据处理失败: " + e.getMessage());
            System.out.println("根本原因: " + e.getCause().getMessage());
            
            // 打印完整的异常链
            System.out.println("\n异常堆栈跟踪:");
            e.printStackTrace();
        }
    }
    
    /**
     * 模拟从文件读取数据并处理
     */
    private static void processDataFromFile(String filename) throws DataProcessingException {
        try {
            // 模拟文件读取
            if (!filename.equals("config.txt")) {
                throw new FileReadException("文件不存在: " + filename);
            }
            
            // 模拟数据解析
            String data = "invalid_data_format";
            if (data.startsWith("invalid")) {
                throw new DataFormatException("数据格式错误: " + data);
            }
            
            // 模拟业务处理
            processBusinessLogic(data);
            
        } catch (FileReadException | DataFormatException e) {
            // 将底层异常包装为业务异常
            throw new DataProcessingException("处理文件数据时发生错误", e);
        }
    }
    
    /**
     * 模拟业务逻辑处理
     */
    private static void processBusinessLogic(String data) throws BusinessLogicException {
        if (data == null || data.isEmpty()) {
            throw new BusinessLogicException("业务数据为空");
        }
        System.out.println("业务处理成功: " + data);
    }
}

// 自定义异常类定义
class BankOperationException extends Exception {
    public BankOperationException(String message) {
        super(message);
    }
    
    public BankOperationException(String message, Throwable cause) {
        super(message, cause);
    }
}

class InsufficientFundsException extends BankOperationException {
    private double currentBalance;
    private double withdrawAmount;
    
    public InsufficientFundsException(double currentBalance, double withdrawAmount) {
        super(String.format("余额不足。当前余额: $%.2f, 尝试取款: $%.2f", 
                          currentBalance, withdrawAmount));
        this.currentBalance = currentBalance;
        this.withdrawAmount = withdrawAmount;
    }
    
    public double getCurrentBalance() {
        return currentBalance;
    }
    
    public double getWithdrawAmount() {
        return withdrawAmount;
    }
}

class InvalidAmountException extends BankOperationException {
    private double amount;
    
    public InvalidAmountException(double amount) {
        super("无效的金额: $" + amount);
        this.amount = amount;
    }
    
    public double getAmount() {
        return amount;
    }
}

class AccountFrozenException extends BankOperationException {
    public AccountFrozenException() {
        super("账户已被冻结，无法进行操作");
    }
}

// 数据处理相关自定义异常
class DataProcessingException extends Exception {
    public DataProcessingException(String message) {
        super(message);
    }
    
    public DataProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}

class FileReadException extends Exception {
    public FileReadException(String message) {
        super(message);
    }
}

class DataFormatException extends Exception {
    public DataFormatException(String message) {
        super(message);
    }
}

class BusinessLogicException extends Exception {
    public BusinessLogicException(String message) {
        super(message);
    }
}
```

### 步骤4：创建银行账户类
创建 `src/main/java/com/example/BankAccount.java` 文件：

```java
package com.example;

/**
 * 银行账户类
 * 用于演示异常处理在实际业务中的应用
 */
public class BankAccount {
    private String accountNumber;
    private double balance;
    private boolean frozen;
    
    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.frozen = false;
    }
    
    /**
     * 存款操作
     */
    public void deposit(double amount) throws InvalidAmountException {
        if (amount <= 0) {
            throw new InvalidAmountException(amount);
        }
        
        if (frozen) {
            throw new AccountFrozenException();
        }
        
        balance += amount;
        System.out.println("存款成功: $" + amount + ", 当前余额: $" + balance);
    }
    
    /**
     * 取款操作
     */
    public void withdraw(double amount) throws InsufficientFundsException, InvalidAmountException {
        if (amount <= 0) {
            throw new InvalidAmountException(amount);
        }
        
        if (frozen) {
            throw new AccountFrozenException();
        }
        
        if (amount > balance) {
            throw new InsufficientFundsException(balance, amount);
        }
        
        balance -= amount;
        System.out.println("取款成功: $" + amount + ", 当前余额: $" + balance);
    }
    
    /**
     * 冻结账户
     */
    public void freezeAccount() {
        this.frozen = true;
        System.out.println("账户已冻结");
    }
    
    /**
     * 解冻账户
     */
    public void unfreezeAccount() {
        this.frozen = false;
        System.out.println("账户已解冻");
    }
    
    /**
     * 获取账户余额
     */
    public double getBalance() {
        return balance;
    }
    
    /**
     * 获取账户号码
     */
    public String getAccountNumber() {
        return accountNumber;
    }
    
    /**
     * 检查账户是否冻结
     */
    public boolean isFrozen() {
        return frozen;
    }
}
```

### 步骤5：创建异常最佳实践演示类
创建 `src/main/java/com/example/ExceptionBestPracticesDemo.java` 文件：

```java
package com.example;

import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * 异常处理最佳实践演示类
 * 展示正确的异常处理方式和常见陷阱
 */
public class ExceptionBestPracticesDemo {
    private static final Logger logger = Logger.getLogger(ExceptionBestPracticesDemo.class.getName());
    
    public static void main(String[] args) {
        System.out.println("=== 异常处理最佳实践演示 ===\n");
        
        // 1. 早期验证和快速失败
        demonstrateEarlyValidation();
        
        // 2. 具体异常优于通用异常
        demonstrateSpecificExceptions();
        
        // 3. 异常信息要具体明确
        demonstrateMeaningfulMessages();
        
        // 4. 资源清理和try-with-resources
        demonstrateResourceManagement();
        
        // 5. 异常处理中的日志记录
        demonstrateLogging();
        
        // 6. 避免常见的异常处理错误
        demonstrateCommonMistakes();
    }
    
    /**
     * 演示早期验证和快速失败
     */
    private static void demonstrateEarlyValidation() {
        System.out.println("1. 早期验证和快速失败:");
        
        try {
            processData("valid_data", 5);
            System.out.println("数据处理成功");
        } catch (IllegalArgumentException e) {
            System.out.println("参数验证失败: " + e.getMessage());
        }
        
        try {
            processData(null, -1);
        } catch (IllegalArgumentException e) {
            System.out.println("参数验证失败: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    /**
     * 演示具体异常优于通用异常
     */
    private static void demonstrateSpecificExceptions() {
        System.out.println("2. 具体异常优于通用异常:");
        
        UserService userService = new UserService();
        
        // 好的做法：捕获具体异常
        try {
            userService.findUserById(123);
        } catch (UserNotFoundException e) {
            System.out.println("用户未找到: " + e.getMessage());
        } catch (DatabaseConnectionException e) {
            System.out.println("数据库连接失败: " + e.getMessage());
        }
        
        // 不好的做法：捕获过于宽泛的异常
        try {
            userService.findUserById(456);
        } catch (Exception e) { // 应该避免这样做
            System.out.println("发生了某种异常: " + e.getMessage());
        }
        
        System.out.println();
    }
    
    /**
     * 演示有意义的异常信息
     */
    private static void demonstrateMeaningfulMessages() {
        System.out.println("3. 有意义的异常信息:");
        
        OrderService orderService = new OrderService();
        
        try {
            orderService.processOrder(null);
        } catch (InvalidOrderException e) {
            System.out.println("订单处理失败: " + e.getMessage());
            // 好的消息包含了上下文信息
        }
        
        System.out.println();
    }
    
    /**
     * 演示资源管理和try-with-resources
     */
    private static void demonstrateResourceManagement() {
        System.out.println("4. 资源管理和try-with-resources:");
        
        // 传统方式（容易忘记关闭资源）
        traditionalResourceHandling();
        
        // 现代方式（自动资源管理）
        modernResourceHandling();
        
        System.out.println();
    }
    
    /**
     * 演示异常处理中的日志记录
     */
    private static void demonstrateLogging() {
        System.out.println("5. 异常处理中的日志记录:");
        
        FileProcessor processor = new FileProcessor();
        
        try {
            processor.processFile("important_data.txt");
        } catch (FileProcessingException e) {
            // 记录详细日志
            logger.log(Level.SEVERE, "文件处理失败", e);
            System.out.println("已记录错误日志");
        }
        
        System.out.println();
    }
    
    /**
     * 演示常见的异常处理错误
     */
    private static void demonstrateCommonMistakes() {
        System.out.println("6. 常见的异常处理错误:");
        
        // 错误1：忽略异常
        System.out.println("错误示例1 - 忽略异常:");
        try {
            riskyOperation();
        } catch (Exception e) {
            // 空的catch块 - 这很危险！
        }
        
        // 错误2：过于宽泛的异常捕获
        System.out.println("错误示例2 - 过于宽泛的异常捕获:");
        try {
            anotherRiskyOperation();
        } catch (Exception e) { // 捕获了不应该捕获的异常
            System.out.println("捕获了所有异常: " + e.getMessage());
        }
        
        // 错误3：在finally中改变返回值
        System.out.println("错误示例3 - finally中改变返回值:");
        System.out.println("getResult(): " + getResult());
        
        System.out.println();
    }
    
    // 辅助方法和类
    private static void processData(String data, int count) {
        // 早期验证
        if (data == null) {
            throw new IllegalArgumentException("数据不能为空");
        }
        if (count <= 0) {
            throw new IllegalArgumentException("计数必须大于0，当前值: " + count);
        }
        
        // 实际处理逻辑
        for (int i = 0; i < count; i++) {
            System.out.println("处理数据: " + data + " #" + (i + 1));
        }
    }
    
    private static void riskyOperation() throws Exception {
        throw new Exception("这是一个风险操作的异常");
    }
    
    private static void anotherRiskyOperation() throws RuntimeException {
        throw new RuntimeException("运行时异常");
    }
    
    private static int getResult() {
        try {
            return 10;
        } finally {
            return 20; // 这会覆盖try中的返回值
        }
    }
    
    private static void traditionalResourceHandling() {
        java.io.FileInputStream fis = null;
        try {
            fis = new java.io.FileInputStream("test.txt");
            // 使用资源...
            System.out.println("传统方式处理文件");
        } catch (java.io.FileNotFoundException e) {
            System.out.println("文件未找到: " + e.getMessage());
        } finally {
            if (fis != null) {
                try {
                    fis.close(); // 必须手动关闭
                } catch (java.io.IOException e) {
                    System.out.println("关闭文件时出错: " + e.getMessage());
                }
            }
        }
    }
    
    private static void modernResourceHandling() {
        try (java.io.FileInputStream fis = new java.io.FileInputStream("test.txt")) {
            // 使用资源...
            System.out.println("现代方式处理文件（自动关闭）");
        } catch (java.io.FileNotFoundException e) {
            System.out.println("文件未找到: " + e.getMessage());
        } catch (java.io.IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }
        // 资源自动关闭，无需手动处理
    }
}

// 业务服务类
class UserService {
    public User findUserById(long userId) throws UserNotFoundException, DatabaseConnectionException {
        // 模拟数据库查询
        if (userId == 123) {
            return new User(userId, "张三");
        } else if (userId == 789) {
            throw new DatabaseConnectionException("数据库连接超时");
        } else {
            throw new UserNotFoundException("用户ID " + userId + " 不存在");
        }
    }
}

class OrderService {
    public void processOrder(Order order) throws InvalidOrderException {
        if (order == null) {
            throw new InvalidOrderException("订单对象不能为空");
        }
        if (order.getItems().isEmpty()) {
            throw new InvalidOrderException("订单必须包含至少一个商品项");
        }
        if (order.getTotalAmount() <= 0) {
            throw new InvalidOrderException("订单总金额必须大于0，当前金额: " + order.getTotalAmount());
        }
        System.out.println("订单处理成功: " + order);
    }
}

class FileProcessor {
    public void processFile(String filename) throws FileProcessingException {
        try {
            // 模拟文件处理
            if (filename == null || filename.isEmpty()) {
                throw new IllegalArgumentException("文件名不能为空");
            }
            if (!filename.endsWith(".txt")) {
                throw new FileProcessingException("不支持的文件格式: " + filename);
            }
            // 实际处理逻辑...
            System.out.println("文件处理完成: " + filename);
        } catch (IllegalArgumentException e) {
            throw new FileProcessingException("文件参数无效", e);
        }
    }
}

// 数据类
class User {
    private long id;
    private String name;
    
    public User(long id, String name) {
        this.id = id;
        this.name = name;
    }
    
    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "'}";
    }
}

class Order {
    private java.util.List<OrderItem> items = new java.util.ArrayList<>();
    private double totalAmount;
    
    public void addItem(OrderItem item) {
        items.add(item);
        totalAmount += item.getPrice() * item.getQuantity();
    }
    
    public java.util.List<OrderItem> getItems() {
        return items;
    }
    
    public double getTotalAmount() {
        return totalAmount;
    }
    
    @Override
    public String toString() {
        return "Order{items=" + items.size() + ", totalAmount=" + totalAmount + "}";
    }
}

class OrderItem {
    private String name;
    private double price;
    private int quantity;
    
    public OrderItem(String name, double price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }
    
    public double getPrice() {
        return price;
    }
    
    public int getQuantity() {
        return quantity;
    }
    
    @Override
    public String toString() {
        return name + "(¥" + price + " x " + quantity + ")";
    }
}

// 自定义业务异常
class UserNotFoundException extends Exception {
    public UserNotFoundException(String message) {
        super(message);
    }
}

class DatabaseConnectionException extends Exception {
    public DatabaseConnectionException(String message) {
        super(message);
    }
}

class InvalidOrderException extends Exception {
    public InvalidOrderException(String message) {
        super(message);
    }
}

class FileProcessingException extends Exception {
    public FileProcessingException(String message) {
        super(message);
    }
    
    public FileProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### 步骤6：编译和运行
```bash
# 编译所有Java文件
javac src/main/java/com/example/*.java

# 分别运行各个演示程序
java com.example.ExceptionBasicsDemo
java com.example.CustomExceptionDemo
java com.example.ExceptionBestPracticesDemo
```

## 🔍 代码详解

### 1. 异常分类体系
- **Checked Exception**：编译时检查的异常，必须处理或声明
- **Runtime Exception**：运行时异常，可选择性处理
- **Error**：系统级错误，通常不应被捕获

### 2. 异常处理原则
- **早发现早处理**：在方法入口处进行参数验证
- **具体优于通用**：捕获具体的异常类型而非Exception
- **信息要明确**：异常消息应包含足够的上下文信息
- **资源要释放**：使用try-with-resources确保资源正确关闭

### 3. 自定义异常设计
- 继承合适的异常基类
- 提供有意义的构造方法
- 包含相关的业务信息
- 支持异常链传递

## 🧪 验证测试

### 功能验证清单
- [ ] 基本异常捕获和处理
- [ ] 多重catch块的正确使用
- [ ] throws和throw关键字的应用
- [ ] 自定义异常类的设计和使用
- [ ] 异常链和包装异常处理
- [ ] try-with-resources资源管理
- [ ] 异常处理最佳实践的应用

### 边界条件测试
- 空值和无效参数处理
- 资源获取失败的情况
- 嵌套异常的传递和处理

## ❓ 常见问题

### Q1: Checked Exception和Runtime Exception有什么区别？
**答**：Checked Exception必须在编译时处理（try-catch或throws），Runtime Exception可以选择性处理。

### Q2: 什么时候应该使用自定义异常？
**答**：当标准异常不能准确表达业务含义时，或者需要传递特定的业务信息时。

### Q3: finally块一定会执行吗？
**答**：几乎总是执行，除非在try或catch块中调用了System.exit()或JVM崩溃。

### Q4: 为什么要避免捕获Exception这样的通用异常？
**答**：会导致代码难以维护，隐藏真正的问题，不利于调试和问题定位。

## 📚 扩展学习

### 相关技术
- [Java日志框架](../java-logging-demo/)
- [Java输入输出](../java-input-output-demo/)
- [Java多线程异常处理](../java-multithreading-demo/)

### 进阶主题
- 异常性能影响分析
- 全局异常处理器设计
- 异常处理框架集成
- 微服务中的异常传播

### 企业级应用
- REST API异常响应设计
- 数据库操作异常处理
- 分布式系统异常传播
- 监控告警中的异常分析

---
> **💡 提示**: 良好的异常处理是高质量代码的重要特征，合理的异常设计能让系统更加健壮和易于维护。