package com.opendemo.java.patterns.decorator;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("装饰器模式测试")
class DecoratorPatternTest {

    @Test
    @DisplayName("基础咖啡")
    void testSimpleCoffee() {
        Coffee coffee = new SimpleCoffee();
        assertEquals(10.0, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee", coffee.getDescription());
    }

    @Test
    @DisplayName("加牛奶的咖啡")
    void testMilkDecorator() {
        Coffee coffee = new MilkDecorator(new SimpleCoffee());
        assertEquals(12.0, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee, Milk", coffee.getDescription());
    }

    @Test
    @DisplayName("加糖的咖啡")
    void testSugarDecorator() {
        Coffee coffee = new SugarDecorator(new SimpleCoffee());
        assertEquals(11.0, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee, Sugar", coffee.getDescription());
    }

    @Test
    @DisplayName("加奶油的咖啡")
    void testWhipDecorator() {
        Coffee coffee = new WhipDecorator(new SimpleCoffee());
        assertEquals(13.5, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee, Whip", coffee.getDescription());
    }

    @Test
    @DisplayName("多重装饰 - 全配料")
    void testFullDecorator() {
        Coffee coffee = new WhipDecorator(
                new SugarDecorator(
                        new MilkDecorator(
                                new SimpleCoffee())));
        assertEquals(16.5, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee, Milk, Sugar, Whip", coffee.getDescription());
    }

    @Test
    @DisplayName("双重牛奶装饰")
    void testDoubleMilk() {
        Coffee coffee = new MilkDecorator(new MilkDecorator(new SimpleCoffee()));
        assertEquals(14.0, coffee.getCost(), 0.01);
        assertEquals("Simple Coffee, Milk, Milk", coffee.getDescription());
    }

    @Test
    @DisplayName("邮件通知")
    void testEmailNotifier() {
        Notifier notifier = new EmailNotifier();
        assertDoesNotThrow(() -> notifier.send("Test message"));
        assertEquals("Email", notifier.getChannel());
    }

    @Test
    @DisplayName("短信通知")
    void testSMSNotifier() {
        Notifier notifier = new SMSNotifier();
        assertDoesNotThrow(() -> notifier.send("Test message"));
        assertEquals("SMS", notifier.getChannel());
    }

    @Test
    @DisplayName("多层通知装饰")
    void testMultiNotifier() {
        Notifier notifier = new SMSNotifier(new EmailNotifier());
        assertDoesNotThrow(() -> notifier.send("Alert!"));
        assertEquals("Email, SMS", notifier.getChannel());
    }

    @Test
    @DisplayName("装饰器不改变接口类型")
    void testDecoratorPreservesType() {
        Coffee coffee = new SimpleCoffee();
        Coffee decorated = new MilkDecorator(coffee);
        assertInstanceOf(Coffee.class, decorated);
        assertInstanceOf(CoffeeDecorator.class, decorated);
    }
}
