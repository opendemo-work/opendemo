package com.opendemo.java.interfaces;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.jupiter.api.Assertions.*;

public class InterfacesDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(InterfacesDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化接口测试环境");
    }
    
    @Test
    void testBasicInterfaceImplementation() {
        logger.info("测试基础接口实现");
        
        Car car = new Car("测试品牌", "测试型号");
        assertEquals("测试品牌", car.getBrand());
        assertEquals("测试型号", car.getModel());
        assertFalse(car.isRunning());
        
        car.start();
        assertTrue(car.isRunning());
        
        car.accelerate(60);
        assertEquals(60, car.getCurrentSpeed());
        
        car.stop();
        assertFalse(car.isRunning());
        assertEquals(0, car.getCurrentSpeed());
    }
    
    @Test
    void testMultipleInterfaceImplementation() {
        logger.info("测试多接口实现");
        
        Airplane airplane = new Airplane("测试航空", "TEST001");
        assertFalse(airplane.isFlying());
        assertEquals(0, airplane.getAltitude());
        
        airplane.start();
        airplane.takeOff();
        assertTrue(airplane.isFlying());
        
        airplane.accelerate(1000);
        assertEquals(1000, airplane.getAltitude());
        
        airplane.land();
        assertFalse(airplane.isFlying());
        assertEquals(0, airplane.getAltitude());
    }
    
    @Test
    void testFunctionalInterface() {
        logger.info("测试函数式接口");
        
        PaymentService paymentService = new PaymentService();
        
        // 测试Lambda表达式
        PaymentProcessor processor = paymentService.createUnionPayProcessor();
        assertNotNull(processor.getProcessorName());
        assertDoesNotThrow(() -> processor.processPayment(100.0));
        
        // 测试匿名内部类
        PaymentProcessor alipay = paymentService.createAlipayProcessor();
        assertEquals("支付宝", alipay.getProcessorName());
        
        PaymentProcessor wechat = paymentService.createWeChatPayProcessor();
        assertEquals("微信支付", wechat.getProcessorName());
        
        // 测试静态工厂方法
        PaymentProcessor mock = PaymentService.createMockProcessor("测试", 1.0);
        assertEquals("测试", mock.getProcessorName());
        assertTrue(mock.processPayment(100.0));
    }
    
    @Test
    void testDefaultMethods() {
        logger.info("测试默认方法");
        
        Car car = new Car("品牌", "型号");
        
        // 测试继承的默认方法
        assertFalse(car.isRunning());
        assertDoesNotThrow(() -> car.honk());
        
        // 测试重写的默认方法
        Airplane airplane = new Airplane("航空", "航班");
        assertDoesNotThrow(() -> airplane.honk());
    }
    
    @Test
    void testCallbackMechanism() {
        logger.info("测试回调机制");
        
        EventManager eventManager = new EventManager();
        boolean[] callbackCalled = {false};
        
        // 测试Lambda回调
        eventManager.fireEvent("测试事件", event -> {
            assertEquals("测试事件", event);
            callbackCalled[0] = true;
        });
        assertTrue(callbackCalled[0]);
        
        // 测试方法引用
        assertDoesNotThrow(() -> 
            eventManager.fireEvent("测试", EventManager.createLoggingHandler()));
        
        // 测试错误处理
        assertDoesNotThrow(() -> 
            eventManager.fireEvent("测试", EventManager.createErrorHandlingHandler()));
    }
    
    @Test
    void testAsyncProcessing() {
        logger.info("测试异步处理");
        
        EventManager eventManager = new EventManager();
        boolean[] completed = {false};
        
        eventManager.processAsync(new EventManager.AsyncProcessor<String>() {
            @Override
            public String process() {
                try {
                    Thread.sleep(100);
                    return "完成";
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return "中断";
                }
            }
            
            @Override
            public void onComplete(String result) {
                assertEquals("完成", result);
                completed[0] = true;
            }
        });
        
        // 给异步操作一些时间
        try {
            Thread.sleep(200);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        assertTrue(completed[0]);
    }
    
    @Test
    void testInterfaceInheritance() {
        logger.info("测试接口继承");
        
        // 测试FlyingVehicle继承Vehicle
        Airplane airplane = new Airplane("航空", "航班");
        
        // 可以调用父接口方法
        airplane.start();
        airplane.stop();
        airplane.accelerate(100);
        
        // 可以调用子接口方法
        airplane.takeOff();
        airplane.land();
        
        // 可以调用默认方法
        airplane.fly();
    }
    
    @Test
    void testPaymentService() {
        logger.info("测试支付服务");
        
        PaymentService paymentService = new PaymentService();
        PaymentProcessor processor = paymentService.createUnionPayProcessor();
        
        // 测试单笔支付
        assertDoesNotThrow(() -> 
            paymentService.processCreditCardPayment(100.0, processor));
        
        // 测试批量支付
        double[] amounts = {50.0, 100.0, 150.0};
        assertDoesNotThrow(() -> 
            paymentService.batchProcessPayments(amounts, processor));
    }
    
    @Test
    void testStaticInterfaceMethods() {
        logger.info("测试接口静态方法");
        
        // 测试Vehicle接口的静态方法
        assertDoesNotThrow(() -> Vehicle.showVehicleInfo());
    }
    
    @Test
    void testMarkerInterface() {
        logger.info("测试标记接口");
        
        Car car = new Car("品牌", "型号");
        
        // 验证实现了SerializableMarker接口
        assertTrue(car instanceof SerializableMarker);
    }
}