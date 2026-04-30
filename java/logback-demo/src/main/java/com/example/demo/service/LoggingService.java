package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
public class LoggingService {

    private static final Logger logger = LoggerFactory.getLogger(LoggingService.class);
    private static final Logger auditLogger = LoggerFactory.getLogger("AUDIT_LOGGER");
    private static final Logger errorLogger = LoggerFactory.getLogger("ERROR_LOGGER");

    public void logWithMdc(String userId, String action) {
        MDC.put("requestId", UUID.randomUUID().toString());
        MDC.put("userId", userId);
        MDC.put("action", action);

        try {
            logger.info("用户操作开始: {}", action);
            logger.debug("调试信息: userId={}, timestamp={}", userId, LocalDateTime.now());
            logger.info("用户操作完成: {}", action);
        } finally {
            MDC.clear();
        }
    }

    public void logAudit(String userId, String operation, String detail) {
        MDC.put("userId", userId);
        MDC.put("operation", operation);
        try {
            auditLogger.info(detail);
        } finally {
            MDC.clear();
        }
    }

    public void logError(String errorCode, String message, Throwable throwable) {
        MDC.put("errorCode", errorCode);
        try {
            errorLogger.error(message, throwable);
        } finally {
            MDC.remove("errorCode");
        }
    }

    public void demonstrateAllLevels() {
        logger.trace("TRACE级别 - 最详细的调试信息");
        logger.debug("DEBUG级别 - 调试信息");
        logger.info("INFO级别 - 一般信息");
        logger.warn("WARN级别 - 警告信息");
        logger.error("ERROR级别 - 错误信息");
    }

    public void demonstrateParameterizedLogging() {
        String user = "张三";
        int age = 25;
        logger.info("用户: {}, 年龄: {}", user, age);
        logger.info("计算结果: {} + {} = {}", 1, 2, 3);
    }

    public void demonstrateExceptionLogging() {
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            logger.error("计算异常", e);
            logger.error("计算异常: {}", e.getMessage());
        }
    }

    public void demonstrateConditionalLogging() {
        if (logger.isDebugEnabled()) {
            logger.debug("耗时计算结果: {}", expensiveComputation());
        }
    }

    private String expensiveComputation() {
        return "computed-value-" + System.currentTimeMillis();
    }
}
