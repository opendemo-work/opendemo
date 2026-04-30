package com.opendemo.java.patterns.decorator;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DecoratorDemo {

    private static final Logger logger = LoggerFactory.getLogger(DecoratorDemo.class);

    public static void main(String[] args) {
        logger.info("=== 装饰器模式演示 ===");

        logger.info("--- 1. 咖啡配料系统 ---");
        Coffee simpleCoffee = new SimpleCoffee();
        System.out.println(simpleCoffee.getDescription() + " -> ¥" + simpleCoffee.getCost());

        Coffee milkCoffee = new MilkDecorator(simpleCoffee);
        System.out.println(milkCoffee.getDescription() + " -> ¥" + milkCoffee.getCost());

        Coffee sugarMilkCoffee = new SugarDecorator(milkCoffee);
        System.out.println(sugarMilkCoffee.getDescription() + " -> ¥" + sugarMilkCoffee.getCost());

        Coffee fullCoffee = new WhipDecorator(sugarMilkCoffee);
        System.out.println(fullCoffee.getDescription() + " -> ¥" + fullCoffee.getCost());

        System.out.println();
        Coffee doubleMilk = new MilkDecorator(new MilkDecorator(new SimpleCoffee()));
        System.out.println(doubleMilk.getDescription() + " -> ¥" + doubleMilk.getCost());

        logger.info("--- 2. 通知系统 ---");
        Notifier emailNotifier = new EmailNotifier();
        emailNotifier.send("Welcome!");
        System.out.println("Channels: " + emailNotifier.getChannel());

        System.out.println();
        Notifier multiNotifier = new SMSNotifier(new EmailNotifier());
        multiNotifier.send("System Alert!");
        System.out.println("Channels: " + multiNotifier.getChannel());
    }
}
