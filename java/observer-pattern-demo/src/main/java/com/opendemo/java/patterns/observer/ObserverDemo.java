package com.opendemo.java.patterns.observer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ObserverDemo {

    private static final Logger logger = LoggerFactory.getLogger(ObserverDemo.class);

    public static void main(String[] args) {
        logger.info("=== 观察者模式演示 ===");

        logger.info("--- 1. 新闻发布系统 ---");
        NewsPublisher publisher = new NewsPublisher();
        NewsSubscriber subscriber1 = new NewsSubscriber("Alice");
        NewsSubscriber subscriber2 = new NewsSubscriber("Bob");
        NewsSubscriber subscriber3 = new NewsSubscriber("Charlie");

        publisher.attach(subscriber1);
        publisher.attach(subscriber2);
        publisher.publishNews("Java 21 正式发布！");

        System.out.println();
        publisher.attach(subscriber3);
        publisher.publishNews("Spring Boot 4.0 即将到来");

        System.out.println();
        publisher.detach(subscriber2);
        publisher.publishNews("设计模式教程更新");

        logger.info("--- 2. 气象站系统 ---");
        WeatherStation station = new WeatherStation();
        WeatherDisplay livingRoom = new WeatherDisplay("客厅");
        WeatherDisplay bedroom = new WeatherDisplay("卧室");

        station.attach(livingRoom);
        station.attach(bedroom);
        station.setMeasurements(25.5f, 65.0f, 1013.2f);

        System.out.println();
        station.setMeasurements(23.0f, 70.5f, 1010.8f);
    }
}
