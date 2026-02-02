package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// Lambda表达式和函数式接口使用示例
public class PaymentService {
    private static final Logger logger = LoggerFactory.getLogger(PaymentService.class);
    
    // 使用函数式接口
    public void processCreditCardPayment(double amount, PaymentProcessor processor) {
        logger.info("处理信用卡支付: ¥{}", amount);
        processor.validateAmount(amount);
        boolean success = processor.processPayment(amount);
        logger.info("支付{}: {}", success ? "成功" : "失败", processor.getProcessorName());
    }
    
    // 方法引用示例
    public void batchProcessPayments(double[] amounts, PaymentProcessor processor) {
        logger.info("批量处理 {} 笔支付", amounts.length);
        for (double amount : amounts) {
            processCreditCardPayment(amount, processor);
        }
    }
    
    // 内部类实现接口
    public PaymentProcessor createAlipayProcessor() {
        return new PaymentProcessor() {
            @Override
            public boolean processPayment(double amount) {
                logger.info("支付宝处理支付: ¥{}", amount);
                return Math.random() > 0.1; // 90%成功率模拟
            }
            
            @Override
            public String getProcessorName() {
                return "支付宝";
            }
        };
    }
    
    // 匿名内部类示例
    public PaymentProcessor createWeChatPayProcessor() {
        return new PaymentProcessor() {
            @Override
            public boolean processPayment(double amount) {
                logger.info("微信支付处理支付: ¥{}", amount);
                return Math.random() > 0.05; // 95%成功率模拟
            }
            
            @Override
            public String getProcessorName() {
                return "微信支付";
            }
        };
    }
    
    // Lambda表达式示例
    public PaymentProcessor createUnionPayProcessor() {
        return (double amount) -> {
            logger.info("银联支付处理支付: ¥{}", amount);
            return Math.random() > 0.15; // 85%成功率模拟
        };
    }
    
    // 静态工厂方法
    public static PaymentProcessor createMockProcessor(String name, double successRate) {
        return new PaymentProcessor() {
            @Override
            public boolean processPayment(double amount) {
                logger.info("{} 处理支付: ¥{}", name, amount);
                return Math.random() < successRate;
            }
            
            @Override
            public String getProcessorName() {
                return name;
            }
        };
    }
}