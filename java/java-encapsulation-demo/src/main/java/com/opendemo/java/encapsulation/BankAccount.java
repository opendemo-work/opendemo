package com.opendemo.java.encapsulation;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * BankAccount银行账户类 - 演示封装基本原则
 * 展示数据隐藏、访问控制、数据验证等封装技术
 */
public class BankAccount {
    private static final Logger logger = LoggerFactory.getLogger(BankAccount.class);
    
    // 私有成员变量 - 实现数据隐藏
    private String accountNumber;     // 账户号码
    private String accountHolderName; // 账户持有人姓名
    private BigDecimal balance;       // 账户余额
    private AccountStatus status;     // 账户状态
    private LocalDateTime createdAt;  // 创建时间
    private int transactionCount;     // 交易次数
    
    // 常量定义
    private static final BigDecimal MIN_BALANCE = new BigDecimal("0.00");
    private static final BigDecimal MAX_WITHDRAWAL = new BigDecimal("50000.00");
    private static final int MAX_DAILY_TRANSACTIONS = 10;
    
    // 构造方法
    public BankAccount(String accountNumber, String accountHolderName, BigDecimal initialBalance) {
        // 参数验证
        if (accountNumber == null || accountNumber.trim().isEmpty()) {
            throw new IllegalArgumentException("账户号码不能为空");
        }
        if (accountHolderName == null || accountHolderName.trim().isEmpty()) {
            throw new IllegalArgumentException("账户持有人姓名不能为空");
        }
        if (initialBalance == null || initialBalance.compareTo(MIN_BALANCE) < 0) {
            throw new IllegalArgumentException("初始余额不能为负数");
        }
        
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        this.balance = initialBalance;
        this.status = AccountStatus.ACTIVE;
        this.createdAt = LocalDateTime.now();
        this.transactionCount = 0;
        
        logger.info("创建银行账户: {}, 持有人: {}, 初始余额: ¥{}", 
                   accountNumber, accountHolderName, initialBalance);
    }
    
    // Getter方法 - 受控访问
    public String getAccountNumber() {
        // 返回账户号码的部分隐藏版本
        if (accountNumber.length() > 4) {
            return "****" + accountNumber.substring(accountNumber.length() - 4);
        }
        return accountNumber;
    }
    
    public String getAccountHolderName() {
        return accountHolderName;
    }
    
    public BigDecimal getBalance() {
        return balance;
    }
    
    public AccountStatus getStatus() {
        return status;
    }
    
    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
    
    public int getTransactionCount() {
        return transactionCount;
    }
    
    // Setter方法 - 带验证的修改
    public void setAccountHolderName(String accountHolderName) {
        if (accountHolderName != null && !accountHolderName.trim().isEmpty()) {
            String oldName = this.accountHolderName;
            this.accountHolderName = accountHolderName.trim();
            logger.info("账户持有人姓名从 '{}' 更新为 '{}'", oldName, accountHolderName);
        } else {
            logger.warn("账户持有人姓名不能为空");
            throw new IllegalArgumentException("账户持有人姓名不能为空");
        }
    }
    
    // 业务方法 - 封装具体操作
    public synchronized boolean deposit(BigDecimal amount) {
        // 参数验证
        if (amount == null || amount.compareTo(MIN_BALANCE) <= 0) {
            logger.warn("存款金额必须大于0: {}", amount);
            return false;
        }
        
        // 状态检查
        if (status != AccountStatus.ACTIVE) {
            logger.warn("账户状态不正常，无法存款: {}", status);
            return false;
        }
        
        // 交易次数检查
        if (transactionCount >= MAX_DAILY_TRANSACTIONS) {
            logger.warn("已达到每日最大交易次数: {}", MAX_DAILY_TRANSACTIONS);
            return false;
        }
        
        // 执行存款操作
        BigDecimal oldBalance = balance;
        balance = balance.add(amount);
        transactionCount++;
        
        logger.info("存款成功: 账户 {}, 金额 ¥{}, 余额从 ¥{} 变为 ¥{}", 
                   accountNumber, amount, oldBalance, balance);
        return true;
    }
    
    public synchronized boolean withdraw(BigDecimal amount) {
        // 参数验证
        if (amount == null || amount.compareTo(MIN_BALANCE) <= 0) {
            logger.warn("取款金额必须大于0: {}", amount);
            return false;
        }
        
        // 金额限制检查
        if (amount.compareTo(MAX_WITHDRAWAL) > 0) {
            logger.warn("单次取款金额不能超过 ¥{}: {}", MAX_WITHDRAWAL, amount);
            return false;
        }
        
        // 状态检查
        if (status != AccountStatus.ACTIVE) {
            logger.warn("账户状态不正常，无法取款: {}", status);
            return false;
        }
        
        // 余额检查
        if (balance.compareTo(amount) < 0) {
            logger.warn("余额不足，当前余额: ¥{}, 取款金额: ¥{}", balance, amount);
            return false;
        }
        
        // 交易次数检查
        if (transactionCount >= MAX_DAILY_TRANSACTIONS) {
            logger.warn("已达到每日最大交易次数: {}", MAX_DAILY_TRANSACTIONS);
            return false;
        }
        
        // 执行取款操作
        BigDecimal oldBalance = balance;
        balance = balance.subtract(amount);
        transactionCount++;
        
        logger.info("取款成功: 账户 {}, 金额 ¥{}, 余额从 ¥{} 变为 ¥{}", 
                   accountNumber, amount, oldBalance, balance);
        return true;
    }
    
    public void freezeAccount() {
        if (status == AccountStatus.ACTIVE) {
            status = AccountStatus.FROZEN;
            logger.info("账户 {} 已冻结", accountNumber);
        } else {
            logger.warn("账户状态不允许冻结: {}", status);
        }
    }
    
    public void unfreezeAccount() {
        if (status == AccountStatus.FROZEN) {
            status = AccountStatus.ACTIVE;
            logger.info("账户 {} 已解冻", accountNumber);
        } else {
            logger.warn("账户状态不允许解冻: {}", status);
        }
    }
    
    public void closeAccount() {
        if (status == AccountStatus.ACTIVE && balance.compareTo(MIN_BALANCE) == 0) {
            status = AccountStatus.CLOSED;
            logger.info("账户 {} 已关闭", accountNumber);
        } else if (balance.compareTo(MIN_BALANCE) > 0) {
            logger.warn("账户仍有余额 ¥{}，无法关闭", balance);
        } else {
            logger.warn("账户状态不允许关闭: {}", status);
        }
    }
    
    public void resetDailyTransactions() {
        transactionCount = 0;
        logger.info("账户 {} 的每日交易次数已重置", accountNumber);
    }
    
    // 查询方法
    public boolean isOverdrawn() {
        return balance.compareTo(MIN_BALANCE) < 0;
    }
    
    public boolean isActive() {
        return status == AccountStatus.ACTIVE;
    }
    
    public BigDecimal getAvailableBalance() {
        return balance.max(MIN_BALANCE);
    }
    
    // 重写Object方法
    @Override
    public String toString() {
        return String.format("BankAccount[number=%s, holder=%s, balance=¥%s, status=%s, created=%s]", 
                           getAccountNumber(), accountHolderName, balance, status, createdAt.toLocalDate());
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        BankAccount that = (BankAccount) obj;
        return accountNumber.equals(that.accountNumber);
    }
    
    @Override
    public int hashCode() {
        return accountNumber.hashCode();
    }
    
    // 账户状态枚举
    public enum AccountStatus {
        ACTIVE("活跃"),
        FROZEN("冻结"),
        CLOSED("已关闭");
        
        private final String description;
        
        AccountStatus(String description) {
            this.description = description;
        }
        
        public String getDescription() {
            return description;
        }
    }
}