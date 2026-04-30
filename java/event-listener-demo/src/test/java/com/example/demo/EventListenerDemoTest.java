package com.example.demo;

import com.example.demo.event.OrderCreatedEvent;
import com.example.demo.event.UserRegisteredEvent;
import com.example.demo.service.EventPublisherService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EventListenerDemoTest {

    @Test
    void testUserRegisteredEventCreation() {
        UserRegisteredEvent event = new UserRegisteredEvent(this, "张三", "zhangsan@test.com");
        assertEquals("张三", event.getUsername());
        assertEquals("zhangsan@test.com", event.getEmail());
        assertEquals(this, event.getSource());
    }

    @Test
    void testOrderCreatedEventCreation() {
        OrderCreatedEvent event = new OrderCreatedEvent(this, "ORD001", "张三", 999.99);
        assertEquals("ORD001", event.getOrderId());
        assertEquals("张三", event.getUsername());
        assertEquals(999.99, event.getAmount());
    }

    @Test
    void testHighValueOrder() {
        OrderCreatedEvent event = new OrderCreatedEvent(this, "ORD002", "李四", 2000.0);
        assertTrue(event.getAmount() > 1000);
    }

    @Test
    void testLowValueOrder() {
        OrderCreatedEvent event = new OrderCreatedEvent(this, "ORD003", "王五", 50.0);
        assertFalse(event.getAmount() > 1000);
    }

    @Test
    void testUserRegisteredEventWithNullEmail() {
        UserRegisteredEvent event = new UserRegisteredEvent(this, "user1", null);
        assertEquals("user1", event.getUsername());
        assertNull(event.getEmail());
    }

    @Test
    void testOrderCreatedEventAmountZero() {
        OrderCreatedEvent event = new OrderCreatedEvent(this, "ORD004", "赵六", 0.0);
        assertEquals(0.0, event.getAmount());
    }

    @Test
    void testMultipleEvents() {
        UserRegisteredEvent userEvent = new UserRegisteredEvent(this, "test", "test@test.com");
        OrderCreatedEvent orderEvent = new OrderCreatedEvent(this, "ORD005", "test", 100.0);
        assertNotEquals(userEvent.getSource(), "different");
        assertEquals(orderEvent.getOrderId(), "ORD005");
    }
}
