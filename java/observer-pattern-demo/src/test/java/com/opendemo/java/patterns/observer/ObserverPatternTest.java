package com.opendemo.java.patterns.observer;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("观察者模式测试")
class ObserverPatternTest {

    private NewsPublisher newsPublisher;
    private WeatherStation weatherStation;

    @BeforeEach
    void setUp() {
        newsPublisher = new NewsPublisher();
        weatherStation = new WeatherStation();
    }

    @Test
    @DisplayName("新闻系统 - 订阅者接收通知")
    void testNewsSubscriberReceivesUpdate() {
        NewsSubscriber subscriber = new NewsSubscriber("TestUser");
        newsPublisher.attach(subscriber);
        newsPublisher.publishNews("Breaking News!");
        assertEquals("Breaking News!", subscriber.getLastReceivedNews());
    }

    @Test
    @DisplayName("新闻系统 - 多个订阅者接收通知")
    void testMultipleSubscribersReceiveUpdate() {
        NewsSubscriber sub1 = new NewsSubscriber("User1");
        NewsSubscriber sub2 = new NewsSubscriber("User2");
        newsPublisher.attach(sub1);
        newsPublisher.attach(sub2);
        newsPublisher.publishNews("Test News");
        assertEquals("Test News", sub1.getLastReceivedNews());
        assertEquals("Test News", sub2.getLastReceivedNews());
    }

    @Test
    @DisplayName("新闻系统 - 取消订阅后不再接收通知")
    void testDetachedSubscriberDoesNotReceiveUpdate() {
        NewsSubscriber sub1 = new NewsSubscriber("User1");
        NewsSubscriber sub2 = new NewsSubscriber("User2");
        newsPublisher.attach(sub1);
        newsPublisher.attach(sub2);
        newsPublisher.detach(sub1);
        newsPublisher.publishNews("Latest News");
        assertNull(sub1.getLastReceivedNews());
        assertEquals("Latest News", sub2.getLastReceivedNews());
    }

    @Test
    @DisplayName("新闻系统 - 订阅者计数")
    void testSubscriberCount() {
        assertEquals(0, newsPublisher.getSubscriberCount());
        NewsSubscriber sub1 = new NewsSubscriber("User1");
        newsPublisher.attach(sub1);
        assertEquals(1, newsPublisher.getSubscriberCount());
        NewsSubscriber sub2 = new NewsSubscriber("User2");
        newsPublisher.attach(sub2);
        assertEquals(2, newsPublisher.getSubscriberCount());
    }

    @Test
    @DisplayName("新闻系统 - 重复订阅不会重复添加")
    void testDuplicateAttach() {
        NewsSubscriber subscriber = new NewsSubscriber("User1");
        newsPublisher.attach(subscriber);
        newsPublisher.attach(subscriber);
        assertEquals(1, newsPublisher.getSubscriberCount());
    }

    @Test
    @DisplayName("气象站 - 显示器接收天气更新")
    void testWeatherDisplayReceivesUpdate() {
        WeatherDisplay display = new WeatherDisplay("客厅");
        weatherStation.attach(display);
        weatherStation.setMeasurements(25.5f, 65.0f, 1013.2f);
        assertEquals(25.5f, display.getTemperature(), 0.01);
        assertEquals(65.0f, display.getHumidity(), 0.01);
    }

    @Test
    @DisplayName("气象站 - 多次更新覆盖旧数据")
    void testWeatherDisplayMultipleUpdates() {
        WeatherDisplay display = new WeatherDisplay("客厅");
        weatherStation.attach(display);
        weatherStation.setMeasurements(25.0f, 60.0f, 1013.0f);
        weatherStation.setMeasurements(30.0f, 75.0f, 1010.0f);
        assertEquals(30.0f, display.getTemperature(), 0.01);
        assertEquals(75.0f, display.getHumidity(), 0.01);
    }

    @Test
    @DisplayName("气象站 - 取消订阅后不接收更新")
    void testWeatherDisplayDetach() {
        WeatherDisplay display = new WeatherDisplay("客厅");
        weatherStation.attach(display);
        weatherStation.setMeasurements(25.0f, 60.0f, 1013.0f);
        weatherStation.detach(display);
        weatherStation.setMeasurements(35.0f, 80.0f, 1005.0f);
        assertEquals(25.0f, display.getTemperature(), 0.01);
    }
}
