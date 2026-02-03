package com.opendemo.java.regex;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

/**
 * Java正则表达式完整示例
 * 
 * 演示Java中正则表达式的各种应用场景：
 * - 基础模式匹配和验证
 * - 文本提取和替换
 * - 复杂数据解析
 * - 表单验证场景
 * - 性能优化技巧
 */
public class RegularExpressionsDemo {
    private static final Logger logger = LoggerFactory.getLogger(RegularExpressionsDemo.class);
    
    // 预编译常用正则表达式模式
    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    );
    
    private static final Pattern PHONE_PATTERN = Pattern.compile(
        "^1[3-9]\\d{9}$"
    );
    
    private static final Pattern URL_PATTERN = Pattern.compile(
        "^(https?|ftp)://[^\\s/$.?#].[^\\s]*$"
    );
    
    private static final Pattern IPV4_PATTERN = Pattern.compile(
        "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    );
    
    public static void main(String[] args) {
        logger.info("=== Java正则表达式完整示例 ===");
        
        RegularExpressionsDemo demo = new RegularExpressionsDemo();
        
        demo.demonstrateBasicMatching();
        demo.demonstrateTextExtraction();
        demo.demonstrateTextReplacement();
        demo.demonstrateDataValidation();
        demo.demonstrateComplexParsing();
        demo.demonstratePerformanceOptimization();
        
        logger.info("=== 示例演示完成 ===");
    }
    
    /**
     * 演示基础模式匹配
     */
    public void demonstrateBasicMatching() {
        logger.info("--- 基础模式匹配 ---");
        
        String text = "联系方式：邮箱 john@example.com，电话 13812345678";
        
        // 邮箱匹配
        Matcher emailMatcher = EMAIL_PATTERN.matcher(text);
        if (emailMatcher.find()) {
            logger.info("找到邮箱: {}", emailMatcher.group());
        }
        
        // 电话匹配
        Matcher phoneMatcher = PHONE_PATTERN.matcher(text);
        if (phoneMatcher.find()) {
            logger.info("找到电话: {}", phoneMatcher.group());
        }
        
        // 使用String.matches()方法
        String simpleEmail = "test@domain.com";
        boolean isValid = simpleEmail.matches("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
        logger.info("简单邮箱验证结果: {}", isValid);
    }
    
    /**
     * 演示文本提取
     */
    public void demonstrateTextExtraction() {
        logger.info("--- 文本提取 ---");
        
        String logText = """
            2024-01-15 10:30:25 INFO  User login successful - userId: 12345
            2024-01-15 10:31:12 ERROR Database connection failed - error: timeout
            2024-01-15 10:32:45 WARN  High memory usage detected - usage: 85%
            """;
        
        // 提取时间戳
        Pattern timestampPattern = Pattern.compile("(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})");
        Matcher timestampMatcher = timestampPattern.matcher(logText);
        
        logger.info("提取的时间戳:");
        while (timestampMatcher.find()) {
            logger.info("  {}", timestampMatcher.group(1));
        }
        
        // 提取日志级别和消息
        Pattern logPattern = Pattern.compile(
            "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})\\s+(INFO|WARN|ERROR)\\s+(.+)"
        );
        Matcher logMatcher = logPattern.matcher(logText);
        
        logger.info("解析的日志信息:");
        while (logMatcher.find()) {
            String timestamp = logMatcher.group(1);
            String level = logMatcher.group(2);
            String message = logMatcher.group(3);
            logger.info("  时间: {} | 级别: {} | 消息: {}", timestamp, level, message);
        }
    }
    
    /**
     * 演示文本替换
     */
    public void demonstrateTextReplacement() {
        logger.info("--- 文本替换 ---");
        
        String sensitiveText = "用户张三的身份证号是110101199001011234，手机号码是13800138000";
        
        // 身份证号脱敏
        String idCardPattern = "(\\d{6})\\d{8}(\\d{4})";
        String maskedIdCard = sensitiveText.replaceAll(idCardPattern, "$1********$2");
        logger.info("身份证脱敏后: {}", maskedIdCard);
        
        // 手机号码脱敏
        String phonePattern = "(\\d{3})\\d{4}(\\d{4})";
        String maskedPhone = sensitiveText.replaceAll(phonePattern, "$1****$2");
        logger.info("手机脱敏后: {}", maskedPhone);
        
        // 批量替换
        String htmlText = "<div>Hello</div><p>World</p><span>!</span>";
        String plainText = htmlText.replaceAll("<[^>]+>", "");
        logger.info("HTML标签移除: {}", plainText);
    }
    
    /**
     * 演示数据验证
     */
    public void demonstrateDataValidation() {
        logger.info("--- 数据验证 ---");
        
        // 邮箱验证测试
        String[] emails = {
            "valid@example.com",
            "invalid.email",
            "test@sub.domain.co.uk",
            "@invalid.com"
        };
        
        logger.info("邮箱验证结果:");
        for (String email : emails) {
            boolean valid = EMAIL_PATTERN.matcher(email).matches();
            logger.info("  {} -> {}", email, valid ? "✓ 有效" : "✗ 无效");
        }
        
        // 电话验证测试
        String[] phones = {
            "13812345678",
            "12812345678",  // 错误的号段
            "1381234567",   // 位数不足
            "138123456789"  // 位数过多
        };
        
        logger.info("电话验证结果:");
        for (String phone : phones) {
            boolean valid = PHONE_PATTERN.matcher(phone).matches();
            logger.info("  {} -> {}", phone, valid ? "✓ 有效" : "✗ 无效");
        }
        
        // 密码强度验证
        Pattern passwordPattern = Pattern.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
        );
        
        String[] passwords = {
            "weakpass",
            "StrongPass123!",
            "STRONGPASS123!",
            "strongpass123!"
        };
        
        logger.info("密码强度验证:");
        for (String pwd : passwords) {
            boolean valid = passwordPattern.matcher(pwd).matches();
            logger.info("  {} -> {}", pwd, valid ? "✓ 符合要求" : "✗ 不符合要求");
        }
    }
    
    /**
     * 演示复杂数据解析
     */
    public void demonstrateComplexParsing() {
        logger.info("--- 复杂数据解析 ---");
        
        // CSV数据解析
        String csvLine = "张三,25,工程师,北京,50000";
        Pattern csvPattern = Pattern.compile("([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)");
        Matcher csvMatcher = csvPattern.matcher(csvLine);
        
        if (csvMatcher.matches()) {
            Map<String, String> personData = new HashMap<>();
            personData.put("姓名", csvMatcher.group(1));
            personData.put("年龄", csvMatcher.group(2));
            personData.put("职位", csvMatcher.group(3));
            personData.put("城市", csvMatcher.group(4));
            personData.put("薪资", csvMatcher.group(5));
            
            logger.info("解析的人员信息:");
            personData.forEach((key, value) -> 
                logger.info("  {}: {}", key, value)
            );
        }
        
        // 配置文件解析
        String configText = """
            # 数据库配置
            db.host=localhost
            db.port=3306
            db.name=myapp
            db.username=admin
            db.password=secret123
            
            # 应用配置
            app.debug=true
            app.timeout=30000
            """;
        
        Pattern configPattern = Pattern.compile("^([\\w.]+)=(.*)$", Pattern.MULTILINE);
        Matcher configMatcher = configPattern.matcher(configText);
        
        Map<String, String> configMap = new HashMap<>();
        while (configMatcher.find()) {
            configMap.put(configMatcher.group(1), configMatcher.group(2));
        }
        
        logger.info("解析的配置项:");
        configMap.forEach((key, value) -> 
            logger.info("  {} = {}", key, value)
        );
    }
    
    /**
     * 演示性能优化
     */
    public void demonstratePerformanceOptimization() {
        logger.info("--- 性能优化 ---");
        
        String largeText = "联系方式：邮箱 user1@example.com，电话 13800138001；邮箱 user2@test.org，电话 13900139002";
        
        // 方法1：重复编译模式（低效）
        long startTime1 = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            Pattern.compile("\\w+@[\\w.-]+\\.[a-zA-Z]{2,}").matcher(largeText).find();
        }
        long endTime1 = System.nanoTime();
        logger.info("重复编译耗时: {} ns", endTime1 - startTime1);
        
        // 方法2：预编译模式（高效）
        long startTime2 = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            EMAIL_PATTERN.matcher(largeText).find();
        }
        long endTime2 = System.nanoTime();
        logger.info("预编译耗时: {} ns", endTime2 - startTime2);
        
        logger.info("性能提升: {:.2f}倍", (double)(endTime1 - startTime1) / (endTime2 - startTime2));
        
        // 展示Pattern类的实用方法
        logger.info("EMAIL_PATTERN标志: {}", EMAIL_PATTERN.flags());
        logger.info("EMAIL_PATTERN模式: {}", EMAIL_PATTERN.pattern());
        logger.info("EMAIL_PATTERN是否固定字符串: {}", EMAIL_PATTERN.toString().equals(Pattern.quote(EMAIL_PATTERN.pattern())));
    }
}