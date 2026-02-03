package com.opendemo.java.encapsulation;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.regex.Pattern;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * ValidationUtils验证工具类 - 演示封装的验证逻辑
 * 提供各种数据验证的静态方法，隐藏复杂的验证实现
 */
public class ValidationUtils {
    private static final Logger logger = LoggerFactory.getLogger(ValidationUtils.class);
    
    // 预编译的正则表达式模式
    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    );
    
    private static final Pattern PHONE_PATTERN = Pattern.compile(
        "^1[3-9]\\d{9}$"
    );
    
    private static final Pattern ID_CARD_PATTERN = Pattern.compile(
        "^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$"
    );
    
    private static final Pattern PASSWORD_PATTERN = Pattern.compile(
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
    );
    
    // 私有构造方法 - 防止实例化
    private ValidationUtils() {
        throw new AssertionError("工具类不应被实例化");
    }
    
    // 电子邮件验证
    public static boolean isValidEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            logger.debug("邮箱验证失败: 输入为空");
            return false;
        }
        
        boolean result = EMAIL_PATTERN.matcher(email.trim()).matches();
        if (!result) {
            logger.debug("邮箱格式不正确: {}", email);
        }
        return result;
    }
    
    // 手机号码验证
    public static boolean isValidPhoneNumber(String phoneNumber) {
        if (phoneNumber == null || phoneNumber.trim().isEmpty()) {
            logger.debug("手机号验证失败: 输入为空");
            return false;
        }
        
        boolean result = PHONE_PATTERN.matcher(phoneNumber.trim()).matches();
        if (!result) {
            logger.debug("手机号格式不正确: {}", phoneNumber);
        }
        return result;
    }
    
    // 身份证号验证
    public static boolean isValidIdCard(String idCard) {
        if (idCard == null || idCard.trim().isEmpty()) {
            logger.debug("身份证验证失败: 输入为空");
            return false;
        }
        
        String trimmedId = idCard.trim().toUpperCase();
        boolean result = ID_CARD_PATTERN.matcher(trimmedId).matches();
        
        if (result) {
            result = isValidIdCardChecksum(trimmedId);
        }
        
        if (!result) {
            logger.debug("身份证格式或校验码不正确: {}", idCard);
        }
        return result;
    }
    
    // 密码强度验证
    public static boolean isValidPassword(String password) {
        if (password == null || password.length() < 8) {
            logger.debug("密码验证失败: 长度不足8位");
            return false;
        }
        
        boolean result = PASSWORD_PATTERN.matcher(password).matches();
        if (!result) {
            logger.debug("密码强度不够: {}", password);
        }
        return result;
    }
    
    // 金额验证
    public static boolean isValidAmount(BigDecimal amount) {
        if (amount == null) {
            logger.debug("金额验证失败: 输入为空");
            return false;
        }
        
        boolean result = amount.compareTo(BigDecimal.ZERO) >= 0;
        if (!result) {
            logger.debug("金额不能为负数: {}", amount);
        }
        return result;
    }
    
    public static boolean isValidAmount(BigDecimal amount, BigDecimal min, BigDecimal max) {
        if (!isValidAmount(amount)) {
            return false;
        }
        
        boolean result = true;
        if (min != null && amount.compareTo(min) < 0) {
            logger.debug("金额小于最小值 {}: {}", min, amount);
            result = false;
        }
        
        if (max != null && amount.compareTo(max) > 0) {
            logger.debug("金额大于最大值 {}: {}", max, amount);
            result = false;
        }
        
        return result;
    }
    
    // 年龄验证
    public static boolean isValidAge(int age) {
        boolean result = age >= 0 && age <= 150;
        if (!result) {
            logger.debug("年龄超出合理范围 [0-150]: {}", age);
        }
        return result;
    }
    
    // 姓名验证
    public static boolean isValidName(String name) {
        if (name == null || name.trim().isEmpty()) {
            logger.debug("姓名验证失败: 输入为空");
            return false;
        }
        
        String trimmedName = name.trim();
        boolean result = trimmedName.length() >= 2 && trimmedName.length() <= 50;
        if (!result) {
            logger.debug("姓名长度应在2-50个字符之间: {}", name);
        }
        return result;
    }
    
    // 日期验证
    public static boolean isValidDate(LocalDate date) {
        if (date == null) {
            logger.debug("日期验证失败: 输入为空");
            return false;
        }
        
        boolean result = !date.isAfter(LocalDate.now());
        if (!result) {
            logger.debug("日期不能晚于今天: {}", date);
        }
        return result;
    }
    
    public static boolean isValidDateRange(LocalDate startDate, LocalDate endDate) {
        if (startDate == null || endDate == null) {
            logger.debug("日期范围验证失败: 输入为空");
            return false;
        }
        
        boolean result = !startDate.isAfter(endDate);
        if (!result) {
            logger.debug("开始日期不能晚于结束日期: {} -> {}", startDate, endDate);
        }
        return result;
    }
    
    // 字符串验证
    public static boolean isNotBlank(String str) {
        return str != null && !str.trim().isEmpty();
    }
    
    public static boolean isLengthValid(String str, int minLength, int maxLength) {
        if (str == null) return false;
        int length = str.trim().length();
        return length >= minLength && length <= maxLength;
    }
    
    // 数字验证
    public static boolean isPositive(Integer number) {
        return number != null && number > 0;
    }
    
    public static boolean isPositive(Long number) {
        return number != null && number > 0;
    }
    
    public static boolean isInRange(int value, int min, int max) {
        return value >= min && value <= max;
    }
    
    // 综合验证方法
    public static ValidationResult validatePersonInfo(String name, String email, String phone, int age) {
        ValidationResult result = new ValidationResult();
        
        if (!isValidName(name)) {
            result.addError("姓名格式不正确");
        }
        
        if (!isValidEmail(email)) {
            result.addError("邮箱格式不正确");
        }
        
        if (!isValidPhoneNumber(phone)) {
            result.addError("手机号格式不正确");
        }
        
        if (!isValidAge(age)) {
            result.addError("年龄超出合理范围");
        }
        
        return result;
    }
    
    // 身份证校验码验证（私有方法）
    private static boolean isValidIdCardChecksum(String idCard) {
        if (idCard.length() != 18) return false;
        
        int[] weights = {7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2};
        char[] checksumCodes = {'1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'};
        
        int sum = 0;
        for (int i = 0; i < 17; i++) {
            sum += Character.getNumericValue(idCard.charAt(i)) * weights[i];
        }
        
        char expectedChecksum = checksumCodes[sum % 11];
        char actualChecksum = idCard.charAt(17);
        
        return expectedChecksum == actualChecksum;
    }
    
    // 验证结果封装类
    public static class ValidationResult {
        private final java.util.List<String> errors = new java.util.ArrayList<>();
        
        public void addError(String error) {
            if (error != null && !error.trim().isEmpty()) {
                errors.add(error.trim());
            }
        }
        
        public boolean isValid() {
            return errors.isEmpty();
        }
        
        public java.util.List<String> getErrors() {
            return new java.util.ArrayList<>(errors);
        }
        
        public String getErrorMessage() {
            return String.join("; ", errors);
        }
        
        @Override
        public String toString() {
            return isValid() ? "验证通过" : "验证失败: " + getErrorMessage();
        }
    }
}