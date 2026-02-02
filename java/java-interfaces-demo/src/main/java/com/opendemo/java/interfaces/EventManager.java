package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 接口回调和事件处理示例
public class EventManager {
    private static final Logger logger = LoggerFactory.getLogger(EventManager.class);
    
    // 回调接口定义
    public interface EventHandler {
        void handleEvent(String event);
        
        default void onError(Exception e) {
            logger.error("事件处理出错", e);
        }
    }
    
    // 异步处理接口
    public interface AsyncProcessor<T> {
        T process();
        
        default void onComplete(T result) {
            logger.info("异步处理完成，结果: {}", result);
        }
        
        default void onFailure(Exception e) {
            logger.error("异步处理失败", e);
        }
    }
    
    // 事件发布方法
    public void fireEvent(String eventName, EventHandler handler) {
        logger.info("发布事件: {}", eventName);
        try {
            handler.handleEvent(eventName);
        } catch (Exception e) {
            handler.onError(e);
        }
    }
    
    // 异步处理方法
    public <T> void processAsync(AsyncProcessor<T> processor) {
        new Thread(() -> {
            try {
                T result = processor.process();
                processor.onComplete(result);
            } catch (Exception e) {
                processor.onFailure(e);
            }
        }).start();
    }
    
    // 工具方法
    public static EventHandler createLoggingHandler() {
        return event -> LoggerFactory.getLogger(EventManager.class).info("处理事件: {}", event);
    }
    
    public static EventHandler createErrorHandlingHandler() {
        return new EventHandler() {
            @Override
            public void handleEvent(String event) {
                if (event == null || event.isEmpty()) {
                    throw new IllegalArgumentException("事件名称不能为空");
                }
                LoggerFactory.getLogger(EventManager.class).info("安全处理事件: {}", event);
            }
            
            @Override
            public void onError(Exception e) {
                LoggerFactory.getLogger(EventManager.class).warn("事件处理警告: {}", e.getMessage());
            }
        };
    }
}