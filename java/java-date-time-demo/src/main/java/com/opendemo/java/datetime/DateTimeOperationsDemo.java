package com.opendemo.java.datetime;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;
import java.time.temporal.ChronoUnit;
import java.time.temporal.TemporalAdjusters;
import java.util.Locale;

/**
 * Java日期时间操作完整示例
 * 
 * 演示Java 8+新的日期时间API，包括LocalDateTime、ZonedDateTime、
 * DateTimeFormatter等现代日期时间处理方式
 * 
 * @author OpenDemo Team
 * @since 1.0.0
 */
public class DateTimeOperationsDemo {
    
    private static final Logger logger = LoggerFactory.getLogger(DateTimeOperationsDemo.class);
    
    // 常用日期时间格式
    private static final DateTimeFormatter STANDARD_FORMATTER = 
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final DateTimeFormatter CHINESE_FORMATTER = 
        DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH时mm分ss秒");
    
    public static void main(String[] args) {
        logger.info("=== Java日期时间操作完整示例 ===");
        
        DateTimeOperationsDemo demo = new DateTimeOperationsDemo();
        
        // 1. LocalDate演示
        demo.demonstrateLocalDate();
        
        // 2. LocalTime演示
        demo.demonstrateLocalTime();
        
        // 3. LocalDateTime演示
        demo.demonstrateLocalDateTime();
        
        // 4. ZonedDateTime演示
        demo.demonstrateZonedDateTime();
        
        // 5. 日期时间格式化
        demo.demonstrateDateTimeFormatting();
        
        // 6. 日期时间计算
        demo.demonstrateDateTimeCalculations();
        
        // 7. 日期时间解析
        demo.demonstrateDateTimeParsing();
        
        // 8. 时区处理
        demo.demonstrateTimeZoneHandling();
        
        logger.info("=== 示例演示完成 ===");
    }
    
    /**
     * 演示LocalDate（仅日期）操作
     */
    public void demonstrateLocalDate() {
        logger.info("\n--- 1. LocalDate操作 ---");
        
        // 创建LocalDate实例
        LocalDate today = LocalDate.now();
        logger.info("今天日期: {}", today);
        
        LocalDate specificDate = LocalDate.of(2026, 2, 2);
        logger.info("指定日期: {}", specificDate);
        
        LocalDate parsedDate = LocalDate.parse("2026-12-25");
        logger.info("解析日期: {}", parsedDate);
        
        // 日期计算
        LocalDate tomorrow = today.plusDays(1);
        logger.info("明天日期: {}", tomorrow);
        
        LocalDate nextMonth = today.plusMonths(1);
        logger.info("下个月日期: {}", nextMonth);
        
        LocalDate lastWeek = today.minusWeeks(1);
        logger.info("上周日期: {}", lastWeek);
        
        // 日期查询
        logger.info("今天是星期几: {}", today.getDayOfWeek());
        logger.info("今天是第几天: {}", today.getDayOfYear());
        logger.info("本月天数: {}", today.lengthOfMonth());
        logger.info("今年是否闰年: {}", today.isLeapYear());
        
        // 日期比较
        LocalDate anotherDate = LocalDate.of(2026, 12, 25);
        logger.info("今天在圣诞节之前: {}", today.isBefore(anotherDate));
        logger.info("今天在圣诞节之后: {}", today.isAfter(anotherDate));
        logger.info("今天等于圣诞节: {}", today.isEqual(anotherDate));
    }
    
    /**
     * 演示LocalTime（仅时间）操作
     */
    public void demonstrateLocalTime() {
        logger.info("\n--- 2. LocalTime操作 ---");
        
        // 创建LocalTime实例
        LocalTime now = LocalTime.now();
        logger.info("现在时间: {}", now);
        
        LocalTime specificTime = LocalTime.of(14, 30, 45);
        logger.info("指定时间: {}", specificTime);
        
        LocalTime parsedTime = LocalTime.parse("09:15:30");
        logger.info("解析时间: {}", parsedTime);
        
        // 时间计算
        LocalTime later = now.plusHours(2);
        logger.info("2小时后: {}", later);
        
        LocalTime earlier = now.minusMinutes(30);
        logger.info("30分钟前: {}", earlier);
        
        // 时间查询
        logger.info("当前小时: {}", now.getHour());
        logger.info("当前分钟: {}", now.getMinute());
        logger.info("当前秒数: {}", now.getSecond());
        
        // 时间比较
        LocalTime meetingTime = LocalTime.of(15, 0);
        logger.info("现在在会议时间之前: {}", now.isBefore(meetingTime));
        logger.info("现在在会议时间之后: {}", now.isAfter(meetingTime));
    }
    
    /**
     * 演示LocalDateTime（日期+时间）操作
     */
    public void demonstrateLocalDateTime() {
        logger.info("\n--- 3. LocalDateTime操作 ---");
        
        // 创建LocalDateTime实例
        LocalDateTime now = LocalDateTime.now();
        logger.info("现在日期时间: {}", now);
        
        LocalDateTime specificDateTime = LocalDateTime.of(2026, 12, 25, 18, 30, 0);
        logger.info("指定日期时间: {}", specificDateTime);
        
        LocalDateTime parsedDateTime = LocalDateTime.parse("2026-07-01T10:15:30");
        logger.info("解析日期时间: {}", parsedDateTime);
        
        // 日期时间计算
        LocalDateTime future = now.plusDays(7).plusHours(3);
        logger.info("一周3小时后: {}", future);
        
        LocalDateTime past = now.minusMonths(1).minusMinutes(15);
        logger.info("一个月15分钟前: {}", past);
        
        // 获取组成部分
        logger.info("年份: {}", now.getYear());
        logger.info("月份: {}", now.getMonth());
        logger.info("日期: {}", now.getDayOfMonth());
        logger.info("小时: {}", now.getHour());
        logger.info("分钟: {}", now.getMinute());
    }
    
    /**
     * 演示ZonedDateTime（带时区的日期时间）操作
     */
    public void demonstrateZonedDateTime() {
        logger.info("\n--- 4. ZonedDateTime操作 ---");
        
        // 创建ZonedDateTime实例
        ZonedDateTime nowBeijing = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
        logger.info("北京时间: {}", nowBeijing);
        
        ZonedDateTime nowNewYork = ZonedDateTime.now(ZoneId.of("America/New_York"));
        logger.info("纽约时间: {}", nowNewYork);
        
        ZonedDateTime nowLondon = ZonedDateTime.now(ZoneId.of("Europe/London"));
        logger.info("伦敦时间: {}", nowLondon);
        
        // 时区转换
        ZonedDateTime utcTime = nowBeijing.withZoneSameInstant(ZoneId.of("UTC"));
        logger.info("UTC时间: {}", utcTime);
        
        // 创建特定时区的时间
        ZonedDateTime tokyoMeeting = ZonedDateTime.of(
            LocalDate.of(2026, 3, 15),
            LocalTime.of(14, 0),
            ZoneId.of("Asia/Tokyo")
        );
        logger.info("东京会议时间: {}", tokyoMeeting);
        
        // 时区偏移
        ZoneOffset offset = nowBeijing.getOffset();
        logger.info("北京时区偏移: {}", offset);
    }
    
    /**
     * 演示日期时间格式化
     */
    public void demonstrateDateTimeFormatting() {
        logger.info("\n--- 5. 日期时间格式化 ---");
        
        LocalDateTime now = LocalDateTime.now();
        
        // 预定义格式
        logger.info("ISO格式: {}", now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        logger.info("短格式: {}", now.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT)));
        logger.info("中等格式: {}", now.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM)));
        logger.info("长格式: {}", now.format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.LONG)));
        
        // 自定义格式
        logger.info("标准格式: {}", now.format(STANDARD_FORMATTER));
        logger.info("中文格式: {}", now.format(CHINESE_FORMATTER));
        
        // 不同语言格式
        DateTimeFormatter frenchFormatter = DateTimeFormatter.ofPattern("EEEE dd MMMM yyyy", Locale.FRENCH);
        logger.info("法语格式: {}", now.format(frenchFormatter));
        
        DateTimeFormatter germanFormatter = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm", Locale.GERMAN);
        logger.info("德语格式: {}", now.format(germanFormatter));
    }
    
    /**
     * 演示日期时间计算
     */
    public void demonstrateDateTimeCalculations() {
        logger.info("\n--- 6. 日期时间计算 ---");
        
        LocalDate startDate = LocalDate.of(2026, 1, 1);
        LocalDate endDate = LocalDate.of(2026, 12, 31);
        
        // 期间计算
        Period period = Period.between(startDate, endDate);
        logger.info("期间: {}个月{}天", period.getMonths(), period.getDays());
        
        // 天数差计算
        long daysBetween = ChronoUnit.DAYS.between(startDate, endDate);
        logger.info("相差天数: {}", daysBetween);
        
        // 小时差计算
        LocalDateTime startDateTime = LocalDateTime.of(2026, 1, 1, 9, 0);
        LocalDateTime endDateTime = LocalDateTime.of(2026, 1, 2, 17, 30);
        long hoursBetween = ChronoUnit.HOURS.between(startDateTime, endDateTime);
        logger.info("相差小时数: {}", hoursBetween);
        
        // 时间调整
        LocalDate firstDayOfMonth = startDate.with(TemporalAdjusters.firstDayOfMonth());
        logger.info("月初第一天: {}", firstDayOfMonth);
        
        LocalDate lastDayOfMonth = startDate.with(TemporalAdjusters.lastDayOfMonth());
        logger.info("月末最后一天: {}", lastDayOfMonth);
        
        LocalDate nextFriday = startDate.with(TemporalAdjusters.next(DayOfWeek.FRIDAY));
        logger.info("下一个周五: {}", nextFriday);
        
        LocalDate firstDayOfNextMonth = startDate.with(TemporalAdjusters.firstDayOfNextMonth());
        logger.info("下月第一天: {}", firstDayOfNextMonth);
    }
    
    /**
     * 演示日期时间解析
     */
    public void demonstrateDateTimeParsing() {
        logger.info("\n--- 7. 日期时间解析 ---");
        
        // 不同格式的解析
        try {
            LocalDate date1 = LocalDate.parse("2026-02-02");
            logger.info("ISO格式解析: {}", date1);
            
            LocalDate date2 = LocalDate.parse("02/02/2026", DateTimeFormatter.ofPattern("MM/dd/yyyy"));
            logger.info("美式格式解析: {}", date2);
            
            LocalDate date3 = LocalDate.parse("2026年02月02日", DateTimeFormatter.ofPattern("yyyy年MM月dd日"));
            logger.info("中文格式解析: {}", date3);
            
            LocalDateTime dateTime1 = LocalDateTime.parse("2026-02-02T14:30:45");
            logger.info("ISO时间解析: {}", dateTime1);
            
            LocalDateTime dateTime2 = LocalDateTime.parse("2026-02-02 14:30:45", 
                DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
            logger.info("自定义格式解析: {}", dateTime2);
            
        } catch (Exception e) {
            logger.error("解析错误: ", e);
        }
    }
    
    /**
     * 演示时区处理
     */
    public void demonstrateTimeZoneHandling() {
        logger.info("\n--- 8. 时区处理 ---");
        
        // 获取所有可用时区
        logger.info("可用时区数量: {}", ZoneId.getAvailableZoneIds().size());
        
        // 常用时区
        String[] commonZones = {
            "Asia/Shanghai", "Asia/Tokyo", "Europe/London", 
            "America/New_York", "America/Los_Angeles", "UTC"
        };
        
        LocalDateTime baseTime = LocalDateTime.of(2026, 6, 15, 12, 0);
        logger.info("基准时间(无时区): {}", baseTime);
        
        for (String zoneId : commonZones) {
            ZonedDateTime zonedTime = baseTime.atZone(ZoneId.of(zoneId));
            logger.info("{}时间: {}", zoneId, zonedTime.format(
                DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z")));
        }
        
        // 时区转换示例
        ZonedDateTime beijingTime = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
        ZonedDateTime nyTime = beijingTime.withZoneSameInstant(ZoneId.of("America/New_York"));
        logger.info("北京时间 {} 对应纽约时间 {}", 
            beijingTime.format(STANDARD_FORMATTER),
            nyTime.format(STANDARD_FORMATTER));
    }
}