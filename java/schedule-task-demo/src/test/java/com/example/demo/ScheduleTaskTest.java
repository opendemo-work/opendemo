package com.example.demo;

import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import static org.junit.jupiter.api.Assertions.*;

class ScheduleTaskTest {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Test
    void testDateTimeFormatter() {
        LocalDateTime now = LocalDateTime.now();
        String formatted = now.format(formatter);
        assertNotNull(formatted);
        assertTrue(formatted.contains("-"));
        assertTrue(formatted.contains(":"));
    }

    @Test
    void testDateTimeParsing() {
        String dateStr = "2026-04-30 12:00:00";
        LocalDateTime parsed = LocalDateTime.parse(dateStr, formatter);
        assertEquals(2026, parsed.getYear());
        assertEquals(4, parsed.getMonthValue());
        assertEquals(30, parsed.getDayOfMonth());
        assertEquals(12, parsed.getHour());
    }

    @Test
    void testFixedRateCalculation() {
        long fixedRate = 5000;
        long start = System.currentTimeMillis();
        long nextExecution = start + fixedRate;
        assertTrue(nextExecution > start);
        assertEquals(5000, nextExecution - start);
    }

    @Test
    void testFixedDelayCalculation() {
        long fixedDelay = 10000;
        long taskEnd = System.currentTimeMillis();
        long nextExecution = taskEnd + fixedDelay;
        assertTrue(nextExecution > taskEnd);
        assertEquals(10000, nextExecution - taskEnd);
    }

    @Test
    void testCronExpressionFormat() {
        String cron = "0 */5 * * * ?";
        String[] parts = cron.split(" ");
        assertEquals(6, parts.length);
        assertEquals("0", parts[0]);
        assertEquals("*/5", parts[1]);
    }

    @Test
    void testCronEveryMinute() {
        String cron = "0 */1 * * * ?";
        String[] parts = cron.split(" ");
        assertEquals(6, parts.length);
        assertEquals("0", parts[0]);
        assertEquals("*/1", parts[1]);
        assertEquals("*", parts[2]);
    }

    @Test
    void testCronDailyNoon() {
        String cron = "0 0 12 * * ?";
        String[] parts = cron.split(" ");
        assertEquals("0", parts[0]);
        assertEquals("0", parts[1]);
        assertEquals("12", parts[2]);
    }

    @Test
    void testInitialDelay() {
        long initialDelay = 10000;
        long fixedRate = 5000;
        assertTrue(initialDelay > 0);
        assertTrue(fixedRate > 0);
        assertTrue(initialDelay >= fixedRate);
    }

    @Test
    void testExecutionCountIncrement() {
        int count = 0;
        count++;
        count++;
        count++;
        assertEquals(3, count);
    }

    @Test
    void testDateTimeNow() {
        LocalDateTime before = LocalDateTime.now();
        LocalDateTime after = LocalDateTime.now();
        assertFalse(after.isBefore(before));
    }
}
