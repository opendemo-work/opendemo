package com.opendemo.java.encapsulation;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * Java封装原则演示程序
 * 展示数据隐藏、访问控制、不可变对象、配置管理等各种封装技术
 */
public class EncapsulationDemo {
    private static final Logger logger = LoggerFactory.getLogger(EncapsulationDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java封装原则完整演示 ===");
        
        EncapsulationDemo demo = new EncapsulationDemo();
        
        demo.demonstrateBasicEncapsulation();
        demo.demonstrateImmutableObjects();
        demo.demonstrateValidationUtils();
        demo.demonstrateConfigurationManagement();
        demo.demonstrateThreadSafety();
        
        logger.info("=== 演示完成 ===");
    }
    
    /**
     * 演示基本封装原则
     */
    public void demonstrateBasicEncapsulation() {
        logger.info("--- 基本封装原则演示 ---");
        
        // 创建银行账户
        BankAccount account = new BankAccount("ACC001", "张三", new BigDecimal("1000.00"));
        
        // 通过公共接口访问数据
        logger.info("账户信息:");
        logger.info("  账户号码: {}", account.getAccountNumber());
        logger.info("  持有人: {}", account.getAccountHolderName());
        logger.info("  余额: ¥{}", account.getBalance());
        logger.info("  状态: {}", account.getStatus());
        
        // 执行业务操作
        logger.info("\n执行银行业务操作:");
        account.deposit(new BigDecimal("500.00"));
        account.withdraw(new BigDecimal("200.00"));
        account.withdraw(new BigDecimal("2000.00")); // 余额不足
        
        // 修改账户信息
        logger.info("\n修改账户信息:");
        account.setAccountHolderName("张三丰");
        logger.info("  更新后的持有人: {}", account.getAccountHolderName());
        
        // 账户状态管理
        logger.info("\n账户状态管理:");
        account.freezeAccount();
        account.deposit(new BigDecimal("100.00")); // 冻结状态下无法操作
        account.unfreezeAccount();
        account.deposit(new BigDecimal("100.00")); // 解冻后可以操作
        
        logger.info("");
    }
    
    /**
     * 演示不可变对象
     */
    public void demonstrateImmutableObjects() {
        logger.info("--- 不可变对象演示 ---");
        
        // 使用构建器创建不可变对象
        ImmutablePerson.Address address = new ImmutablePerson.Address(
            "北京市朝阳区", "北京", "100000", "中国"
        );
        
        ImmutablePerson person = new ImmutablePerson.Builder()
            .setName("李四")
            .setAge(25)
            .setBirthDate(LocalDate.of(1998, 5, 15))
            .addHobby("阅读")
            .addHobby("游泳")
            .setAddress(address)
            .build();
        
        // 访问不可变对象属性
        logger.info("个人信息:");
        logger.info("  姓名: {}", person.getName());
        logger.info("  年龄: {}", person.getAge());
        logger.info("  生日: {}", person.getBirthDate());
        logger.info("  爱好: {}", person.getHobbies());
        logger.info("  地址: {}", person.getAddress());
        logger.info("  是否成年: {}", person.isAdult());
        logger.info("  距离下次生日还有: {} 天", person.getDaysUntilNextBirthday());
        
        // 尝试修改不可变对象（创建新对象）
        logger.info("\n创建修改后的对象:");
        ImmutablePerson updatedPerson = person.withName("李四改");
        logger.info("  原对象姓名: {}", person.getName());
        logger.info("  新对象姓名: {}", updatedPerson.getName());
        
        // 验证不可变性
        logger.info("\n验证不可变性:");
        try {
            // 这些操作不会影响原对象
            person.getHobbies().add("新爱好");
            logger.info("  原对象爱好: {}", person.getHobbies());
        } catch (UnsupportedOperationException e) {
            logger.info("  爱好列表是不可修改的");
        }
        
        logger.info("");
    }
    
    /**
     * 演示验证工具类
     */
    public void demonstrateValidationUtils() {
        logger.info("--- 验证工具类演示 ---");
        
        // 数据验证演示
        logger.info("数据验证测试:");
        
        // 邮箱验证
        String[] emails = {"valid@example.com", "invalid.email", "test@domain.co.uk"};
        for (String email : emails) {
            boolean valid = ValidationUtils.isValidEmail(email);
            logger.info("  邮箱 '{}' 验证结果: {}", email, valid ? "✓ 有效" : "✗ 无效");
        }
        
        // 手机号验证
        String[] phones = {"13812345678", "12812345678", "1381234567"};
        for (String phone : phones) {
            boolean valid = ValidationUtils.isValidPhoneNumber(phone);
            logger.info("  手机号 '{}' 验证结果: {}", phone, valid ? "✓ 有效" : "✗ 无效");
        }
        
        // 密码验证
        String[] passwords = {"weakpass", "StrongPass123!", "STRONGPASS123!"};
        for (String pwd : passwords) {
            boolean valid = ValidationUtils.isValidPassword(pwd);
            logger.info("  密码 '{}' 验证结果: {}", pwd, valid ? "✓ 符合要求" : "✗ 不符合要求");
        }
        
        // 综合验证
        logger.info("\n综合信息验证:");
        ValidationUtils.ValidationResult result = ValidationUtils.validatePersonInfo(
            "张三", "zhangsan@example.com", "13812345678", 25
        );
        logger.info("  验证结果: {}", result);
        
        ValidationUtils.ValidationResult invalidResult = ValidationUtils.validatePersonInfo(
            "", "invalid-email", "12345", -5
        );
        logger.info("  无效信息验证结果: {}", invalidResult);
        logger.info("  错误信息: {}", invalidResult.getErrorMessage());
        
        logger.info("");
    }
    
    /**
     * 演示配置管理
     */
    public void demonstrateConfigurationManagement() {
        logger.info("--- 配置管理演示 ---");
        
        // 创建配置实例
        Configuration config = Configuration.getInstance();
        
        // 设置一些配置项
        config.setProperty("database.url", "jdbc:mysql://localhost:3306/test");
        config.setProperty("database.username", "root");
        config.setProperty("database.password", "password123");
        config.setProperty("app.timeout", "30000");
        config.setProperty("app.debug", "true");
        
        // 获取配置项
        logger.info("配置项获取:");
        logger.info("  数据库URL: {}", config.getProperty("database.url"));
        logger.info("  用户名: {}", config.getProperty("database.username"));
        logger.info("  超时时间: {} ms", config.getIntProperty("app.timeout", 5000));
        logger.info("  调试模式: {}", config.getBooleanProperty("app.debug", false));
        logger.info("  不存在的配置: {}", config.getProperty("non.existent", "默认值"));
        
        // 配置验证
        logger.info("\n配置验证:");
        boolean hasRequired = config.validateRequiredProperties("database.url", "database.username");
        logger.info("  必需配置项验证: {}", hasRequired ? "✓ 通过" : "✗ 失败");
        
        boolean missingRequired = config.validateRequiredProperties("missing.property");
        logger.info("  缺失配置项验证: {}", missingRequired ? "✓ 通过" : "✗ 失败");
        
        // 配置信息
        logger.info("\n配置统计:");
        logger.info("  配置项总数: {}", config.getPropertyCount());
        logger.info("  是否为空: {}", config.isEmpty());
        logger.info("  包含数据库URL: {}", config.containsProperty("database.url"));
        
        logger.info("");
    }
    
    /**
     * 演示线程安全性
     */
    public void demonstrateThreadSafety() {
        logger.info("--- 线程安全性演示 ---");
        
        // 创建共享的银行账户
        BankAccount sharedAccount = new BankAccount("SHARED001", "共享账户", new BigDecimal("1000.00"));
        
        // 创建多个线程同时操作账户
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 3; j++) {
                    // 随机执行存款或取款
                    if (Math.random() > 0.5) {
                        sharedAccount.deposit(new BigDecimal("100.00"));
                    } else {
                        sharedAccount.withdraw(new BigDecimal("50.00"));
                    }
                    
                    try {
                        Thread.sleep(100); // 模拟处理时间
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
                logger.info("线程 {} 完成操作，最终余额: ¥{}", 
                           threadId, sharedAccount.getBalance());
            });
        }
        
        // 启动所有线程
        logger.info("启动多线程并发操作测试:");
        for (Thread thread : threads) {
            thread.start();
        }
        
        // 等待所有线程完成
        try {
            for (Thread thread : threads) {
                thread.join();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        logger.info("最终账户余额: ¥{}", sharedAccount.getBalance());
        logger.info("总交易次数: {}", sharedAccount.getTransactionCount());
        logger.info("");
    }
}