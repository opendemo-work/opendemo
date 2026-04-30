package com.opendemo.java.patterns.strategy;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class StrategyDemo {

    private static final Logger logger = LoggerFactory.getLogger(StrategyDemo.class);

    public static void main(String[] args) {
        logger.info("=== 策略模式演示 ===");

        logger.info("--- 1. 支付策略 ---");
        PaymentContext paymentContext = new PaymentContext();

        paymentContext.setPaymentStrategy(new CreditCardPayment("1234567890123456", "Zhang San", "12/28"));
        paymentContext.executePayment(199.99);

        System.out.println();
        paymentContext.setPaymentStrategy(new AlipayPayment("zhangsan@alipay.com"));
        paymentContext.executePayment(88.88);

        System.out.println();
        paymentContext.setPaymentStrategy(new WeChatPayment("wx_openid_12345"));
        paymentContext.executePayment(50.00);

        logger.info("--- 2. 排序策略 ---");
        Sorter sorter = new Sorter();
        int[] data = {64, 34, 25, 12, 22, 11, 90};

        sorter.setSortingStrategy(new BubbleSort());
        sorter.sort(data.clone());

        System.out.println();
        sorter.setSortingStrategy(new QuickSort());
        sorter.sort(data.clone());

        System.out.println();
        sorter.setSortingStrategy(new MergeSort());
        sorter.sort(data.clone());
    }
}
