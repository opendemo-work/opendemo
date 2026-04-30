package com.example.demo;

import com.example.demo.service.LoggingService;
import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

import static org.junit.jupiter.api.Assertions.*;

class LogbackDemoTest {

    @Test
    void testLoggerCreation() {
        Logger logger = LoggerFactory.getLogger(LogbackDemoTest.class);
        assertNotNull(logger);
        assertTrue(logger.isInfoEnabled());
    }

    @Test
    void testLoggingServiceAllLevels() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.demonstrateAllLevels());
    }

    @Test
    void testLoggingServiceParameterized() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.demonstrateParameterizedLogging());
    }

    @Test
    void testLoggingServiceExceptionLogging() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.demonstrateExceptionLogging());
    }

    @Test
    void testLoggingServiceConditionalLogging() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.demonstrateConditionalLogging());
    }

    @Test
    void testMdcPutAndGet() {
        MDC.put("requestId", "test-123");
        MDC.put("userId", "user-001");
        assertEquals("test-123", MDC.get("requestId"));
        assertEquals("user-001", MDC.get("userId"));
        MDC.clear();
        assertNull(MDC.get("requestId"));
    }

    @Test
    void testMdcRemove() {
        MDC.put("key", "value");
        assertEquals("value", MDC.get("key"));
        MDC.remove("key");
        assertNull(MDC.get("key"));
    }

    @Test
    void testLoggingServiceLogWithMdc() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.logWithMdc("user001", "LOGIN"));
        assertNull(MDC.get("requestId"));
        assertNull(MDC.get("userId"));
    }

    @Test
    void testLoggingServiceAudit() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.logAudit("user001", "DELETE", "删除用户"));
        assertNull(MDC.get("userId"));
    }

    @Test
    void testLoggingServiceError() {
        LoggingService service = new LoggingService();
        assertDoesNotThrow(() -> service.logError("ERR001", "测试错误", new RuntimeException("test")));
        assertNull(MDC.get("errorCode"));
    }

    @Test
    void testLoggerLevels() {
        Logger logger = LoggerFactory.getLogger(LogbackDemoTest.class);
        assertTrue(logger.isErrorEnabled());
        assertTrue(logger.isWarnEnabled());
        assertTrue(logger.isInfoEnabled());
    }
}
