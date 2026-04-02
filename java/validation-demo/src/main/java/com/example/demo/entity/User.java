package com.example.demo.entity;

import com.example.demo.validation.Phone;

import javax.validation.constraints.*;

/**
 * 用户实体 - 演示各种校验注解
 */
public class User {
    
    @NotNull(message = "ID不能为空")
    @Min(value = 1, message = "ID必须大于0")
    private Long id;
    
    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 20, message = "用户名长度必须在2-20之间")
    private String username;
    
    @NotBlank(message = "密码不能为空")
    @Pattern(regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$",
            message = "密码必须包含大小写字母和数字，且长度至少8位")
    private String password;
    
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Min(value = 18, message = "年龄必须大于等于18")
    @Max(value = 120, message = "年龄必须小于等于120")
    private Integer age;
    
    @AssertTrue(message = "必须同意用户协议")
    private Boolean agreeTerms;
    
    @Phone(message = "手机号格式不正确")
    private String phone;
    
    @DecimalMin(value = "0.0", message = "积分不能为负数")
    private Double points;
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public Integer getAge() {
        return age;
    }
    
    public void setAge(Integer age) {
        this.age = age;
    }
    
    public Boolean getAgreeTerms() {
        return agreeTerms;
    }
    
    public void setAgreeTerms(Boolean agreeTerms) {
        this.agreeTerms = agreeTerms;
    }
    
    public String getPhone() {
        return phone;
    }
    
    public void setPhone(String phone) {
        this.phone = phone;
    }
    
    public Double getPoints() {
        return points;
    }
    
    public void setPoints(Double points) {
        this.points = points;
    }
}
