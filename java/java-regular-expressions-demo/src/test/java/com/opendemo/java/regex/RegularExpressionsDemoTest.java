package com.opendemo.java.regex;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java正则表达式示例测试类
 * 测试各种正则表达式功能的正确性
 */
public class RegularExpressionsDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(RegularExpressionsDemoTest.class);
    private RegularExpressionsDemo demo;
    
    @BeforeEach
    void setUp() {
        demo = new RegularExpressionsDemo();
        logger.info("初始化测试环境");
    }
    
    @Test
    void testEmailValidation() {
        logger.info("测试邮箱验证功能");
        
        // 有效的邮箱
        assertTrue(isValidEmail("test@example.com"));
        assertTrue(isValidEmail("user.name@domain.co.uk"));
        assertTrue(isValidEmail("test123@test-domain.org"));
        
        // 无效的邮箱
        assertFalse(isValidEmail("invalid.email"));
        assertFalse(isValidEmail("@domain.com"));
        assertFalse(isValidEmail("test@"));
        assertFalse(isValidEmail("test@domain"));
    }
    
    @Test
    void testPhoneValidation() {
        logger.info("测试电话验证功能");
        
        // 有效的电话号码
        assertTrue(isValidPhone("13812345678"));
        assertTrue(isValidPhone("15900123456"));
        assertTrue(isValidPhone("18812345678"));
        
        // 无效的电话号码
        assertFalse(isValidPhone("12812345678"));  // 错误号段
        assertFalse(isValidPhone("1381234567"));   // 位数不足
        assertFalse(isValidPhone("138123456789")); // 位数过多
        assertFalse(isValidPhone("abcd1234567"));  // 包含字母
    }
    
    @Test
    void testUrlValidation() {
        logger.info("测试URL验证功能");
        
        // 有效的URL
        assertTrue(isValidUrl("http://www.example.com"));
        assertTrue(isValidUrl("https://example.com/path"));
        assertTrue(isValidUrl("ftp://files.example.com"));
        
        // 无效的URL
        assertFalse(isValidUrl("www.example.com"));  // 缺少协议
        assertFalse(isValidUrl("http://"));          // 不完整
        assertFalse(isValidUrl("invalid url"));      // 格式错误
    }
    
    @Test
    void testIpv4Validation() {
        logger.info("测试IPv4地址验证功能");
        
        // 有效的IPv4地址
        assertTrue(isValidIpv4("192.168.1.1"));
        assertTrue(isValidIpv4("127.0.0.1"));
        assertTrue(isValidIpv4("255.255.255.255"));
        
        // 无效的IPv4地址
        assertFalse(isValidIpv4("256.1.1.1"));    // 数字超出范围
        assertFalse(isValidIpv4("192.168.1"));    // 缺少段
        assertFalse(isValidIpv4("192.168.1.1.1")); // 段数过多
        assertFalse(isValidIpv4("192.168.1.a"));  // 包含字母
    }
    
    @Test
    void testTextExtraction() {
        logger.info("测试文本提取功能");
        
        String text = "联系方式：邮箱 john@example.com，电话 13812345678";
        
        // 提取邮箱
        Pattern emailPattern = Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
        Matcher emailMatcher = emailPattern.matcher(text);
        assertTrue(emailMatcher.find());
        assertEquals("john@example.com", emailMatcher.group());
        
        // 提取电话
        Pattern phonePattern = Pattern.compile("1[3-9]\\d{9}");
        Matcher phoneMatcher = phonePattern.matcher(text);
        assertTrue(phoneMatcher.find());
        assertEquals("13812345678", phoneMatcher.group());
    }
    
    @Test
    void testTextReplacement() {
        logger.info("测试文本替换功能");
        
        String original = "身份证号：110101199001011234";
        
        // 身份证脱敏
        String pattern = "(\\d{6})\\d{8}(\\d{4})";
        String result = original.replaceAll(pattern, "$1********$2");
        assertEquals("身份证号：110101********1234", result);
        
        // HTML标签移除
        String html = "<div>Hello</div><p>World</p>";
        String plain = html.replaceAll("<[^>]+>", "");
        assertEquals("HelloWorld", plain);
    }
    
    @Test
    void testPasswordValidation() {
        logger.info("测试密码强度验证");
        
        Pattern passwordPattern = Pattern.compile(
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
        );
        
        // 符合要求的密码
        assertTrue(passwordPattern.matcher("StrongPass123!").matches());
        assertTrue(passwordPattern.matcher("MySecure@2024").matches());
        
        // 不符合要求的密码
        assertFalse(passwordPattern.matcher("weakpass").matches());        // 缺少大写字母、数字、特殊字符
        assertFalse(passwordPattern.matcher("STRONGPASS123!").matches());  // 缺少小写字母
        assertFalse(passwordPattern.matcher("StrongPass!").matches());     // 缺少数字
        assertFalse(passwordPattern.matcher("Strong123").matches());       // 缺少特殊字符
    }
    
    @Test
    void testCsvParsing() {
        logger.info("测试CSV数据解析");
        
        String csvLine = "张三,25,工程师,北京,50000";
        Pattern csvPattern = Pattern.compile("([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)");
        Matcher matcher = csvPattern.matcher(csvLine);
        
        assertTrue(matcher.matches());
        assertEquals("张三", matcher.group(1));
        assertEquals("25", matcher.group(2));
        assertEquals("工程师", matcher.group(3));
        assertEquals("北京", matcher.group(4));
        assertEquals("50000", matcher.group(5));
    }
    
    @Test
    void testConfigParsing() {
        logger.info("测试配置文件解析");
        
        String configLine = "db.host=localhost";
        Pattern configPattern = Pattern.compile("^([\\w.]+)=(.*)$");
        Matcher matcher = configPattern.matcher(configLine);
        
        assertTrue(matcher.matches());
        assertEquals("db.host", matcher.group(1));
        assertEquals("localhost", matcher.group(2));
    }
    
    @Test
    void testPerformanceComparison() {
        logger.info("测试性能对比");
        
        String text = "邮箱 test@example.com 出现多次";
        Pattern compiledPattern = Pattern.compile("\\w+@[\\w.-]+\\.[a-zA-Z]{2,}");
        
        // 测试预编译模式的性能优势
        long startTime1 = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            compiledPattern.matcher(text).find();
        }
        long endTime1 = System.nanoTime();
        
        long startTime2 = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            Pattern.compile("\\w+@[\\w.-]+\\.[a-zA-Z]{2,}").matcher(text).find();
        }
        long endTime2 = System.nanoTime();
        
        // 预编译应该更快
        assertTrue((endTime1 - startTime1) < (endTime2 - startTime2));
    }
    
    // 辅助验证方法
    private boolean isValidEmail(String email) {
        Pattern pattern = Pattern.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$");
        return pattern.matcher(email).matches();
    }
    
    private boolean isValidPhone(String phone) {
        Pattern pattern = Pattern.compile("^1[3-9]\\d{9}$");
        return pattern.matcher(phone).matches();
    }
    
    private boolean isValidUrl(String url) {
        Pattern pattern = Pattern.compile("^(https?|ftp)://[^\\s/$.?#].[^\\s]*$");
        return pattern.matcher(url).matches();
    }
    
    private boolean isValidIpv4(String ip) {
        Pattern pattern = Pattern.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$");
        return pattern.matcher(ip).matches();
    }
}