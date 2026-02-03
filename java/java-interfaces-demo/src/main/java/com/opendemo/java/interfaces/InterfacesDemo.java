package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 主演示程序
public class InterfacesDemo {
    private static final Logger logger = LoggerFactory.getLogger(InterfacesDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java接口设计完整演示 ===");
        
        InterfacesDemo demo = new InterfacesDemo();
        
        demo.demonstrateBasicInterfaces();
        demo.demonstrateMultipleInterfaces();
        demo.demonstrateFunctionalInterfaces();
        demo.demonstrateCallbackMechanism();
        demo.demonstrateDefaultMethods();
        
        logger.info("=== 演示完成 ===");
    }
    
    public void demonstrateBasicInterfaces() {
        logger.info("--- 基础接口演示 ---");
        
        Car car = new Car("丰田", "卡罗拉");
        car.start();
        car.accelerate(50);
        car.honk();
        car.openTrunk();
        car.stop();
        
        logger.info("汽车运行状态: {}", car.isRunning());
        logger.info("");
    }
    
    public void demonstrateMultipleInterfaces() {
        logger.info("--- 多接口实现演示 ---");
        
        Airplane airplane = new Airplane("中国国际航空", "CA1234");
        airplane.start();
        airplane.takeOff();
        airplane.accelerate(2000);
        airplane.setAltitude(8000);
        airplane.honk();
        airplane.land();
        airplane.stop();
        
        logger.info("飞机飞行状态: {}", airplane.isFlying());
        logger.info("当前高度: {} 米", airplane.getAltitude());
        logger.info("");
    }
    
    public void demonstrateFunctionalInterfaces() {
        logger.info("--- 函数式接口演示 ---");
        
        PaymentService paymentService = new PaymentService();
        
        // Lambda表达式
        PaymentProcessor unionPay = paymentService.createUnionPayProcessor();
        paymentService.processCreditCardPayment(1000.0, unionPay);
        
        // 方法引用和匿名内部类
        PaymentProcessor alipay = paymentService.createAlipayProcessor();
        PaymentProcessor wechat = paymentService.createWeChatPayProcessor();
        
        double[] payments = {100.0, 200.0, 300.0};
        paymentService.batchProcessPayments(payments, alipay);
        
        // 静态工厂方法
        PaymentProcessor mockProcessor = PaymentService.createMockProcessor("测试支付", 0.95);
        paymentService.processCreditCardPayment(500.0, mockProcessor);
        
        logger.info("");
    }
    
    public void demonstrateCallbackMechanism() {
        logger.info("--- 回调机制演示 ---");
        
        EventManager eventManager = new EventManager();
        
        // Lambda回调
        eventManager.fireEvent("用户登录", event -> 
            logger.info("处理登录事件: {}", event));
        
        // 方法引用
        eventManager.fireEvent("数据更新", EventManager.createLoggingHandler());
        
        // 匿名内部类
        eventManager.fireEvent("系统错误", new EventManager.EventHandler() {
            @Override
            public void handleEvent(String event) {
                logger.error("紧急处理事件: {}", event);
                throw new RuntimeException("模拟异常");
            }
            
            @Override
            public void onError(Exception e) {
                logger.error("事件处理异常: {}", e.getMessage());
            }
        });
        
        // 异步处理
        eventManager.processAsync(new EventManager.AsyncProcessor<String>() {
            @Override
            public String process() {
                try {
                    Thread.sleep(1000);
                    return "异步任务完成";
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException(e);
                }
            }
        });
        
        logger.info("");
    }
    
    public void demonstrateDefaultMethods() {
        logger.info("--- 默认方法演示 ---");
        
        // 调用接口静态方法
        Vehicle.showVehicleInfo();
        
        // 使用默认实现
        Car car = new Car("本田", "雅阁");
        logger.info("默认运行状态: {}", car.isRunning());
        car.honk(); // 调用默认方法
        
        // 重写的默认方法
        Airplane airplane = new Airplane("南方航空", "CZ5678");
        airplane.honk(); // 调用重写的方法
        
        logger.info("");
    }
}