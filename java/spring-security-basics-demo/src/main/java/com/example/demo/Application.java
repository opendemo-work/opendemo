package com.example.demo;

import com.example.demo.config.SecurityConfig;
import com.example.demo.service.UserService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

/**
 * Spring Security演示应用
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║       Spring Security 基础安全演示                        ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(SecurityConfig.class);
        
        AuthenticationManager authManager = context.getBean(AuthenticationManager.class);
        
        // 测试1: 正确登录
        System.out.println("📦 测试1: 正确登录\n");
        authenticate(authManager, "admin", "admin123");
        
        // 测试2: 错误密码
        System.out.println("📦 测试2: 错误密码\n");
        authenticate(authManager, "admin", "wrongpassword");
        
        // 测试3: 不存在的用户
        System.out.println("📦 测试3: 不存在的用户\n");
        authenticate(authManager, "hacker", "password");
        
        // 测试4: 普通用户登录
        System.out.println("📦 测试4: 普通用户登录\n");
        authenticate(authManager, "user", "user123");
        
        System.out.println("═══════════════════════════════════════════════════════════");
        System.out.println("Spring Security 核心概念:");
        System.out.println("  ✅ Authentication - 认证（你是谁）");
        System.out.println("  ✅ Authorization  - 授权（你能做什么）");
        System.out.println("  ✅ UserDetails    - 用户信息接口");
        System.out.println("  ✅ GrantedAuthority - 权限/角色");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
    
    private static void authenticate(AuthenticationManager authManager, String username, String password) {
        try {
            Authentication authentication = authManager.authenticate(
                    new UsernamePasswordAuthenticationToken(username, password)
            );
            
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
            System.out.println("  ✅ 登录成功!");
            System.out.println("     用户名: " + userDetails.getUsername());
            System.out.print("     角色: ");
            for (GrantedAuthority authority : userDetails.getAuthorities()) {
                System.out.print(authority.getAuthority() + " ");
            }
            System.out.println("\n");
        } catch (AuthenticationException e) {
            System.out.println("  ❌ 登录失败: " + e.getMessage() + "\n");
        }
    }
}
