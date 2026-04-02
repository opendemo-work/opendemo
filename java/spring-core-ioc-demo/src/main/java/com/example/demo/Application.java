package com.example.demo;

import com.example.demo.config.AppConfig;
import com.example.demo.model.User;
import com.example.demo.service.UserService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.util.List;

/**
 * Spring IoC演示应用主类
 * 
 * 演示Spring IoC容器的核心功能：
 * 1. 容器启动与初始化
 * 2. Bean的创建与管理
 * 3. 依赖注入
 * 4. Bean生命周期
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("=== Spring IoC 演示开始 ===\n");
        
        // 1. 创建IoC容器 - 使用注解配置
        System.out.println("1. 创建IoC容器...");
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(AppConfig.class);
        System.out.println("   容器创建完成\n");
        
        // 2. 从容器中获取Bean
        System.out.println("2. 从容器中获取UserService Bean...");
        UserService userService = context.getBean(UserService.class);
        System.out.println("   Bean获取成功: " + userService.getClass().getSimpleName() + "\n");
        
        // 3. 使用Bean执行业务操作
        System.out.println("3. 执行业务操作...");
        
        // 查询所有用户
        System.out.println("   查询所有用户:");
        List<User> users = userService.findAll();
        users.forEach(user -> System.out.println("   - " + user));
        System.out.println();
        
        // 根据ID查询用户
        System.out.println("   根据ID查询用户(1):");
        User user = userService.findById(1L);
        System.out.println("   - " + user + "\n");
        
        // 创建新用户
        System.out.println("   创建新用户:");
        User newUser = new User(null, "赵六", "zhaoliu@example.com", 35);
        User created = userService.createUser(newUser);
        System.out.println("   - 创建成功: " + created + "\n");
        
        // 更新用户
        System.out.println("   更新用户:");
        created.setAge(36);
        User updated = userService.updateUser(created);
        System.out.println("   - 更新成功: " + updated + "\n");
        
        // 再次查询所有用户
        System.out.println("   再次查询所有用户:");
        users = userService.findAll();
        users.forEach(u -> System.out.println("   - " + u));
        System.out.println();
        
        // 4. 关闭容器
        System.out.println("4. 关闭IoC容器...");
        context.close();
        System.out.println("   容器已关闭\n");
        
        System.out.println("=== Spring IoC 演示结束 ===");
    }
}
