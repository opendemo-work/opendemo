package com.example.demo.listener;

import com.example.demo.event.OrderCreatedEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

@Component
public class OrderEventListener {

    private static final Logger logger = LoggerFactory.getLogger(OrderEventListener.class);

    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        logger.info("[订单处理] 订单创建: orderId={}, user={}, amount={}",
                event.getOrderId(), event.getUsername(), event.getAmount());
    }

    @EventListener(condition = "#event.amount > 1000")
    public void handleHighValueOrder(OrderCreatedEvent event) {
        logger.info("[VIP订单] 高价值订单通知: orderId={}, amount={}",
                event.getOrderId(), event.getAmount());
    }
}
