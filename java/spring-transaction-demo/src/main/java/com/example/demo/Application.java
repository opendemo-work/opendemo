package com.example.demo;

import com.example.demo.config.TransactionConfig;
import com.example.demo.entity.Account;
import com.example.demo.service.BankService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.math.BigDecimal;
import java.util.List;

/**
 * Spring事务演示应用
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║       Spring 声明式事务管理演示                           ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(TransactionConfig.class);
        
        BankService bankService = context.getBean(BankService.class);
        
        // 创建测试账户
        System.out.println("📦 创建测试账户\n");
        bankService.createAccount("ACC001", "张三", new BigDecimal("1000.00"));
        bankService.createAccount("ACC002", "李四", new BigDecimal("500.00"));
        
        // 显示初始状态
        showAllAccounts(bankService);
        
        System.out.println("📦 示例1: 标准转账（事务成功）\n");
        bankService.transfer("ACC001", "ACC002", new BigDecimal("200.00"));
        showAllAccounts(bankService);
        
        System.out.println("📦 示例2: 事务回滚演示\n");
        try {
            bankService.transferWithException("ACC001", "ACC002", new BigDecimal("100.00"));
        } catch (RuntimeException e) {
            System.out.println("  [捕获异常] " + e.getMessage());
            System.out.println("  [预期结果] 事务已回滚，余额不变\n");
        }
        showAllAccounts(bankService);
        
        System.out.println("📦 示例3: 只读查询\n");
        BigDecimal total = bankService.getTotalBalance();
        System.out.println("  所有账户总余额: " + total + "\n");
        
        System.out.println("═══════════════════════════════════════════════════════════");
        System.out.println("事务传播行为总结:");
        System.out.println("  REQUIRED      - 默认，加入当前事务或新建");
        System.out.println("  REQUIRES_NEW  - 新建独立事务");
        System.out.println("  NESTED        - 嵌套事务");
        System.out.println("  SUPPORTS      - 支持当前事务，无事务则非事务执行");
        System.out.println("  MANDATORY     - 必须在事务中执行");
        System.out.println("  NOT_SUPPORTED - 非事务执行");
        System.out.println("  NEVER         - 禁止在事务中执行");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
    
    private static void showAllAccounts(BankService bankService) {
        System.out.println("  当前账户状态:");
        List<Account> accounts = bankService.findAllAccounts();
        accounts.forEach(acc -> System.out.println("    " + acc));
        System.out.println();
    }
}
