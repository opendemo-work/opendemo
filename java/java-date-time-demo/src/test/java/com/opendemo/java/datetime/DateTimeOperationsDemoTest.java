package com.opendemo.java.datetime;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

/**
 * DateTimeOperationsDemo测试类
 * 
 * 测试日期时间操作的各种功能
 * 
 * @author OpenDemo Team
 */
class DateTimeOperationsDemoTest {
    
    private DateTimeOperationsDemo demo;
    
    @BeforeEach
    void setUp() {
        demo = new DateTimeOperationsDemo();
    }
    
    @Test
    void testLocalDateOperations() {
        // 测试LocalDate创建
        LocalDate today = LocalDate.now();
        LocalDate specificDate = LocalDate.of(2026, 2, 2);
        LocalDate parsedDate = LocalDate.parse("2026-12-25");
        
        assertNotNull(today);
        assertEquals(2026, specificDate.getYear());
        assertEquals(12, parsedDate.getMonthValue());
        assertEquals(25, parsedDate.getDayOfMonth());
        
        // 测试日期计算
        LocalDate tomorrow = today.plusDays(1);
        assertEquals(today.getDayOfYear() + 1, tomorrow.getDayOfYear());
        
        LocalDate lastMonth = today.minusMonths(1);
        assertEquals(today.getMonthValue() - 1, lastMonth.getMonthValue());
    }
    
    @Test
    void testLocalTimeOperations() {
        // 测试LocalTime创建
        LocalTime now = LocalTime.now();
        LocalTime specificTime = LocalTime.of(14, 30, 45);
        LocalTime parsedTime = LocalTime.parse("09:15:30");
        
        assertNotNull(now);
        assertEquals(14, specificTime.getHour());
        assertEquals(15, parsedTime.getMinute());
        
        // 测试时间计算
        LocalTime later = now.plusHours(2);
        assertEquals((now.getHour() + 2) % 24, later.getHour());
        
        LocalTime earlier = now.minusMinutes(30);
        int expectedMinute = now.getMinute() - 30;
        if (expectedMinute < 0) {
            expectedMinute += 60;
        }
        assertEquals(expectedMinute, earlier.getMinute());
    }
    
    @Test
    void testLocalDateTimeOperations() {
        // 测试LocalDateTime创建
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime specificDateTime = LocalDateTime.of(2026, 12, 25, 18, 30, 0);
        LocalDateTime parsedDateTime = LocalDateTime.parse("2026-07-01T10:15:30");
        
        assertNotNull(now);
        assertEquals(2026, specificDateTime.getYear());
        assertEquals(7, parsedDateTime.getMonthValue());
        assertEquals(1, parsedDateTime.getDayOfMonth());
        
        // 测试日期时间计算
        LocalDateTime future = now.plusDays(7).plusHours(3);
        assertEquals(now.getDayOfYear() + 7, future.getDayOfYear());
        assertEquals((now.getHour() + 3) % 24, future.getHour());
    }
    
    @Test
    void testZonedDateTimeOperations() {
        // 测试时区创建
        ZonedDateTime beijingTime = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
        ZonedDateTime nyTime = ZonedDateTime.now(ZoneId.of("America/New_York"));
        
        assertNotNull(beijingTime);
        assertNotNull(nyTime);
        assertNotEquals(beijingTime.getZone(), nyTime.getZone());
        
        // 测试时区转换
        ZonedDateTime utcTime = beijingTime.withZoneSameInstant(ZoneId.of("UTC"));
        assertEquals(beijingTime.toInstant(), utcTime.toInstant());
    }
    
    @Test
    void testDateTimeFormatting() {
        LocalDateTime dateTime = LocalDateTime.of(2026, 2, 2, 14, 30, 45);
        
        // 测试标准格式化
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formatted = dateTime.format(formatter);
        assertEquals("2026-02-02 14:30:45", formatted);
        
        // 测试ISO格式
        String isoFormatted = dateTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);
        assertTrue(isoFormatted.contains("2026-02-02T14:30:45"));
    }
    
    @Test
    void testDateTimeParsing() {
        // 测试标准解析
        LocalDateTime parsed1 = LocalDateTime.parse("2026-02-02T14:30:45");
        assertEquals(2026, parsed1.getYear());
        assertEquals(2, parsed1.getMonthValue());
        assertEquals(2, parsed1.getDayOfMonth());
        assertEquals(14, parsed1.getHour());
        
        // 测试自定义格式解析
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        LocalDateTime parsed2 = LocalDateTime.parse("2026-12-25 18:00:00", formatter);
        assertEquals(2026, parsed2.getYear());
        assertEquals(12, parsed2.getMonthValue());
        assertEquals(25, parsed2.getDayOfMonth());
    }
    
    @Test
    void testDateTimeCalculations() {
        LocalDate startDate = LocalDate.of(2026, 1, 1);
        LocalDate endDate = LocalDate.of(2026, 12, 31);
        
        // 测试期间计算
        long daysBetween = ChronoUnit.DAYS.between(startDate, endDate);
        assertEquals(364, daysBetween);
        
        // 测试时间调整
        LocalDate firstDay = startDate.with(java.time.temporal.TemporalAdjusters.firstDayOfMonth());
        assertEquals(1, firstDay.getDayOfMonth());
        
        LocalDate lastDay = startDate.with(java.time.temporal.TemporalAdjusters.lastDayOfMonth());
        assertEquals(31, lastDay.getDayOfMonth());
    }
    
    @Test
    void testTimeZoneHandling() {
        // 测试时区ID有效性
        assertTrue(ZoneId.getAvailableZoneIds().contains("Asia/Shanghai"));
        assertTrue(ZoneId.getAvailableZoneIds().contains("America/New_York"));
        assertTrue(ZoneId.getAvailableZoneIds().contains("UTC"));
        
        // 测试时区转换一致性
        LocalDateTime baseTime = LocalDateTime.of(2026, 6, 15, 12, 0);
        ZonedDateTime shanghaiTime = baseTime.atZone(ZoneId.of("Asia/Shanghai"));
        ZonedDateTime utcTime = shanghaiTime.withZoneSameInstant(ZoneId.of("UTC"));
        
        assertEquals(shanghaiTime.toInstant(), utcTime.toInstant());
    }
    
    @Test
    void testEdgeCases() {
        // 测试闰年
        LocalDate leapYear = LocalDate.of(2024, 2, 29);
        assertTrue(leapYear.isLeapYear());
        assertEquals(29, leapYear.lengthOfMonth());
        
        // 测试非闰年
        LocalDate nonLeapYear = LocalDate.of(2026, 2, 28);
        assertFalse(nonLeapYear.isLeapYear());
        assertEquals(28, nonLeapYear.lengthOfMonth());
        
        // 测试月末边界
        LocalDate endOfMonth = LocalDate.of(2026, 1, 31);
        LocalDate nextMonth = endOfMonth.plusMonths(1);
        assertEquals(2, nextMonth.getMonthValue());
        assertEquals(28, nextMonth.getDayOfMonth()); // 2026年2月有28天
    }
}