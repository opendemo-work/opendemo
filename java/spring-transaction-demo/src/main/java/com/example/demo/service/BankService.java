package com.example.demo.service;

import com.example.demo.entity.Account;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;
import java.math.BigDecimal;
import java.util.List;

/**
 * 银行服务类
 * 
 * 演示各种事务传播行为和隔离级别
 */
@Service
public class BankService {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    /**
     * 创建账户（无事务）
     */
    public Account createAccount(String accountNumber, String ownerName, BigDecimal initialBalance) {
        Account account = new Account(accountNumber, ownerName, initialBalance);
        entityManager.persist(account);
        System.out.println("  [创建账户] " + account);
        return account;
    }
    
    /**
     * 查询所有账户
     */
    public List<Account> findAllAccounts() {
        TypedQuery<Account> query = entityManager.createQuery("SELECT a FROM Account a", Account.class);
        return query.getResultList();
    }
    
    /**
     * 标准转账 - REQUIRED（默认）
     * 
     * 如果当前没有事务，就新建一个事务
     * 如果已经存在一个事务中，加入到这个事务中
     */
    @Transactional
    public void transfer(String fromAccountNumber, String toAccountNumber, BigDecimal amount) {
        System.out.println("  [转账开始] 从 " + fromAccountNumber + " 到 " + toAccountNumber + " 金额: " + amount);
        
        Account fromAccount = findAccountByNumber(fromAccountNumber);
        Account toAccount = findAccountByNumber(toAccountNumber);
        
        // 检查余额
        if (fromAccount.getBalance().compareTo(amount) < 0) {
            throw new RuntimeException("余额不足");
        }
        
        // 扣款
        fromAccount.setBalance(fromAccount.getBalance().subtract(amount));
        entityManager.merge(fromAccount);
        System.out.println("    扣款成功，新余额: " + fromAccount.getBalance());
        
        // 收款
        toAccount.setBalance(toAccount.getBalance().add(amount));
        entityManager.merge(toAccount);
        System.out.println("    收款成功，新余额: " + toAccount.getBalance());
        
        System.out.println("  [转账完成]");
    }
    
    /**
     * 演示事务回滚
     * 
     * 运行时异常会自动回滚
     */
    @Transactional
    public void transferWithException(String fromAccountNumber, String toAccountNumber, BigDecimal amount) {
        System.out.println("  [异常转账开始]");
        
        transfer(fromAccountNumber, toAccountNumber, amount);
        
        // 模拟异常
        throw new RuntimeException("模拟系统故障，事务应该回滚");
    }
    
    /**
     * REQUIRES_NEW - 新建事务
     * 
     * 不管是否存在事务，都创建新事务
     * 如果已存在事务，将当前事务挂起
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logTransaction(String message) {
        System.out.println("  [日志记录 - REQUIRES_NEW] " + message);
        // 这里可以保存到日志表，独立于主事务
    }
    
    /**
     * NESTED - 嵌套事务
     * 
     * 如果当前存在事务，则在嵌套事务内执行
     * 如果当前没有事务，则执行与REQUIRED类似的操作
     */
    @Transactional(propagation = Propagation.NESTED)
    public void nestedOperation() {
        System.out.println("  [嵌套操作 - NESTED]");
    }
    
    /**
     * 只读事务
     * 
     * 用于查询操作，可以优化性能
     */
    @Transactional(readOnly = true)
    public BigDecimal getTotalBalance() {
        System.out.println("  [只读查询 - 总余额]");
        List<Account> accounts = findAllAccounts();
        return accounts.stream()
                .map(Account::getBalance)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    /**
     * 指定隔离级别
     * 
     * READ_COMMITTED: 防止脏读，允许不可重复读和幻读
     */
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public void operationWithIsolation() {
        System.out.println("  [指定隔离级别 - READ_COMMITTED]");
    }
    
    private Account findAccountByNumber(String accountNumber) {
        TypedQuery<Account> query = entityManager.createQuery(
                "SELECT a FROM Account a WHERE a.accountNumber = :number", Account.class);
        query.setParameter("number", accountNumber);
        return query.getSingleResult();
    }
}
