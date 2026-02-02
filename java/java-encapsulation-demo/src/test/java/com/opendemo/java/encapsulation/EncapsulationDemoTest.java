package com.opendemo.java.encapsulation;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java封装原则示例测试类
 * 测试各种封装技术和设计模式的正确性
 */
public class EncapsulationDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(EncapsulationDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化封装测试环境");
    }
    
    @Test
    void testBankAccountEncapsulation() {
        logger.info("测试银行账户封装");
        
        // 测试正常创建
        BankAccount account = new BankAccount("TEST001", "测试用户", new BigDecimal("1000.00"));
        
        assertEquals("TEST001", account.getAccountNumber());
        assertEquals("测试用户", account.getAccountHolderName());
        assertEquals(new BigDecimal("1000.00"), account.getBalance());
        assertEquals(BankAccount.AccountStatus.ACTIVE, account.getStatus());
        
        // 测试存款功能
        assertTrue(account.deposit(new BigDecimal("500.00")));
        assertEquals(new BigDecimal("1500.00"), account.getBalance());
        
        // 测试取款功能
        assertTrue(account.withdraw(new BigDecimal("200.00")));
        assertEquals(new BigDecimal("1300.00"), account.getBalance());
        
        // 测试余额不足
        assertFalse(account.withdraw(new BigDecimal("2000.00")));
        assertEquals(new BigDecimal("1300.00"), account.getBalance()); // 余额不变
        
        // 测试无效金额
        assertFalse(account.deposit(new BigDecimal("-100.00")));
        assertFalse(account.withdraw(new BigDecimal("-50.00")));
        assertFalse(account.deposit(new BigDecimal("0.00")));
        
        // 测试账户状态管理
        account.freezeAccount();
        assertEquals(BankAccount.AccountStatus.FROZEN, account.getStatus());
        assertFalse(account.deposit(new BigDecimal("100.00"))); // 冻结状态下无法操作
        
        account.unfreezeAccount();
        assertEquals(BankAccount.AccountStatus.ACTIVE, account.getStatus());
        assertTrue(account.deposit(new BigDecimal("100.00"))); // 解冻后可以操作
    }
    
    @Test
    void testBankAccountValidation() {
        logger.info("测试银行账户验证");
        
        // 测试无效参数
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("", "用户", new BigDecimal("100.00"));
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC001", "", new BigDecimal("100.00"));
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC001", "用户", new BigDecimal("-100.00"));
        });
        
        // 测试姓名修改验证
        BankAccount account = new BankAccount("TEST001", "原姓名", new BigDecimal("1000.00"));
        assertThrows(IllegalArgumentException.class, () -> {
            account.setAccountHolderName("");
        });
        
        assertThrows(IllegalArgumentException.class, () -> {
            account.setAccountHolderName(null);
        });
    }
    
    @Test
    void testImmutablePerson() {
        logger.info("测试不可变对象");
        
        // 测试构建器模式
        ImmutablePerson.Address address = new ImmutablePerson.Address("街道", "城市", "邮编", "国家");
        List<String> hobbies = Arrays.asList("阅读", "游泳");
        
        ImmutablePerson person = ImmutablePerson.createWithDetails(
            "测试用户", 25, LocalDate.of(1998, 1, 1), hobbies, address
        );
        
        assertEquals("测试用户", person.getName());
        assertEquals(25, person.getAge());
        assertEquals(LocalDate.of(1998, 1, 1), person.getBirthDate());
        assertEquals(hobbies, person.getHobbies());
        assertEquals(address, person.getAddress());
        
        // 测试不可变性
        List<String> originalHobbies = person.getHobbies();
        originalHobbies.add("新爱好");
        // 原始对象不应该被修改
        assertFalse(person.getHobbies().contains("新爱好"));
        
        // 测试with方法创建新对象
        ImmutablePerson updatedPerson = person.withName("新姓名");
        assertEquals("测试用户", person.getName()); // 原对象不变
        assertEquals("新姓名", updatedPerson.getName()); // 新对象改变
        
        // 测试equals和hashCode
        ImmutablePerson samePerson = ImmutablePerson.createWithDetails(
            "测试用户", 25, LocalDate.of(1998, 1, 1), hobbies, address
        );
        assertEquals(person, samePerson);
        assertEquals(person.hashCode(), samePerson.hashCode());
    }
    
    @Test
    void testValidationUtils() {
        logger.info("测试验证工具类");
        
        // 邮箱验证
        assertTrue(ValidationUtils.isValidEmail("test@example.com"));
        assertTrue(ValidationUtils.isValidEmail("user.name@domain.co.uk"));
        assertFalse(ValidationUtils.isValidEmail("invalid.email"));
        assertFalse(ValidationUtils.isValidEmail("@domain.com"));
        assertFalse(ValidationUtils.isValidEmail(null));
        assertFalse(ValidationUtils.isValidEmail(""));
        
        // 手机号验证
        assertTrue(ValidationUtils.isValidPhoneNumber("13812345678"));
        assertTrue(ValidationUtils.isValidPhoneNumber("15900123456"));
        assertFalse(ValidationUtils.isValidPhoneNumber("12812345678"));
        assertFalse(ValidationUtils.isValidPhoneNumber("1381234567"));
        assertFalse(ValidationUtils.isValidPhoneNumber(null));
        
        // 密码验证
        assertTrue(ValidationUtils.isValidPassword("StrongPass123!"));
        assertFalse(ValidationUtils.isValidPassword("weakpass"));
        assertFalse(ValidationUtils.isValidPassword("STRONGPASS123!"));
        assertFalse(ValidationUtils.isValidPassword("StrongPass!"));
        assertFalse(ValidationUtils.isValidPassword(null));
        
        // 金额验证
        assertTrue(ValidationUtils.isValidAmount(new BigDecimal("100.00")));
        assertTrue(ValidationUtils.isValidAmount(new BigDecimal("0.00")));
        assertFalse(ValidationUtils.isValidAmount(new BigDecimal("-100.00")));
        assertFalse(ValidationUtils.isValidAmount(null));
        
        // 年龄验证
        assertTrue(ValidationUtils.isValidAge(25));
        assertTrue(ValidationUtils.isValidAge(0));
        assertTrue(ValidationUtils.isValidAge(150));
        assertFalse(ValidationUtils.isValidAge(-1));
        assertFalse(ValidationUtils.isValidAge(151));
        
        // 综合验证
        ValidationUtils.ValidationResult result = ValidationUtils.validatePersonInfo(
            "张三", "zhangsan@example.com", "13812345678", 25
        );
        assertTrue(result.isValid());
        
        ValidationUtils.ValidationResult invalidResult = ValidationUtils.validatePersonInfo(
            "", "invalid-email", "12345", -5
        );
        assertFalse(invalidResult.isValid());
        assertEquals(4, invalidResult.getErrors().size());
    }
    
    @Test
    void testConfiguration() {
        logger.info("测试配置管理");
        
        Configuration config = Configuration.getInstance();
        
        // 测试配置设置和获取
        config.setProperty("test.key", "test.value");
        config.setProperty("test.number", "123");
        config.setProperty("test.boolean", "true");
        
        assertEquals("test.value", config.getProperty("test.key"));
        assertEquals("default", config.getProperty("non.existent", "default"));
        assertEquals(123, config.getIntProperty("test.number", 0));
        assertEquals(456, config.getIntProperty("non.existent", 456));
        assertTrue(config.getBooleanProperty("test.boolean", false));
        assertFalse(config.getBooleanProperty("non.existent", false));
        
        // 测试配置验证
        assertTrue(config.validateRequiredProperties("test.key"));
        assertFalse(config.validateRequiredProperties("missing.property"));
        assertTrue(config.validateRequiredProperties()); // 空数组应该返回true
        
        // 测试配置信息
        assertTrue(config.containsProperty("test.key"));
        assertFalse(config.containsProperty("non.existent"));
        assertFalse(config.isEmpty());
        assertTrue(config.getPropertyCount() > 0);
    }
    
    @Test
    void testThreadSafety() {
        logger.info("测试线程安全性");
        
        BankAccount account = new BankAccount("THREAD001", "线程测试", new BigDecimal("1000.00"));
        BigDecimal initialBalance = account.getBalance();
        int threadCount = 10;
        int operationsPerThread = 100;
        
        // 创建多个线程并发操作
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    if (Math.random() > 0.5) {
                        account.deposit(new BigDecimal("10.00"));
                    } else {
                        account.withdraw(new BigDecimal("5.00"));
                    }
                }
            });
        }
        
        // 启动所有线程
        for (Thread thread : threads) {
            thread.start();
        }
        
        // 等待所有线程完成
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        // 验证最终状态的合理性
        BigDecimal expectedChange = new BigDecimal(threadCount * operationsPerThread * 5); // 每次净增加5元
        BigDecimal finalBalance = account.getBalance();
        
        logger.info("初始余额: {}, 最终余额: {}, 理论变化: {}", 
                   initialBalance, finalBalance, expectedChange);
        
        // 余额应该是合理的（考虑到可能的失败操作）
        assertTrue(finalBalance.compareTo(BigDecimal.ZERO) >= 0);
        assertTrue(account.getTransactionCount() <= threadCount * operationsPerThread);
    }
    
    @Test
    void testUtilityClassInstantiation() {
        logger.info("测试工具类实例化防护");
        
        // 验证ValidationUtils不能被实例化
        assertThrows(AssertionError.class, () -> {
            ValidationUtils validationUtils = new ValidationUtils();
        });
    }
    
    @Test
    void testAddressImmutability() {
        logger.info("测试Address不可变性");
        
        ImmutablePerson.Address address1 = new ImmutablePerson.Address("街道1", "城市1", "邮编1", "国家1");
        ImmutablePerson.Address address2 = new ImmutablePerson.Address("街道1", "城市1", "邮编1", "国家1");
        ImmutablePerson.Address address3 = new ImmutablePerson.Address("街道2", "城市2", "邮编2", "国家2");
        
        // 测试equals和hashCode
        assertEquals(address1, address2);
        assertEquals(address1.hashCode(), address2.hashCode());
        assertNotEquals(address1, address3);
        
        // 测试copy方法
        ImmutablePerson.Address copy = address1.copy();
        assertEquals(address1, copy);
        assertNotSame(address1, copy); // 应该是不同的对象实例
    }
}