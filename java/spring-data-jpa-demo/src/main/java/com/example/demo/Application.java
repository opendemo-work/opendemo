package com.example.demo;

import com.example.demo.config.JpaConfig;
import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.util.List;
import java.util.Optional;

/**
 * Spring Data JPA演示应用
 * 
 * 展示JPA的CRUD操作、查询方法、分页等功能
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║       Spring Data JPA 数据持久化演示                      ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        // 创建容器
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(JpaConfig.class);
        
        UserService userService = context.getBean(UserService.class);
        
        System.out.println("📦 示例1: 创建用户\n");
        User user1 = new User();
        user1.setUsername("张三");
        user1.setEmail("zhangsan@example.com");
        user1.setAge(25);
        userService.createUser(user1);
        System.out.println("  创建成功: " + user1);
        
        User user2 = new User();
        user2.setUsername("李四");
        user2.setEmail("lisi@example.com");
        user2.setAge(30);
        userService.createUser(user2);
        System.out.println("  创建成功: " + user2 + "\n");
        
        System.out.println("📦 示例2: 查询所有用户\n");
        List<User> allUsers = userService.findAll();
        allUsers.forEach(u -> System.out.println("  " + u));
        System.out.println();
        
        System.out.println("📦 示例3: 根据ID查询\n");
        Optional<User> found = userService.findById(1L);
        found.ifPresent(u -> System.out.println("  找到用户: " + u + "\n"));
        
        System.out.println("📦 示例4: 根据用户名查询\n");
        Optional<User> byUsername = userService.findByUsername("张三");
        byUsername.ifPresent(u -> System.out.println("  找到用户: " + u + "\n"));
        
        System.out.println("📦 示例5: 模糊搜索\n");
        List<User> searchResults = userService.searchByUsername("张");
        searchResults.forEach(u -> System.out.println("  搜索结果: " + u));
        System.out.println();
        
        System.out.println("📦 示例6: 年龄范围查询\n");
        List<User> ageRange = userService.findByAgeBetween(20, 28);
        ageRange.forEach(u -> System.out.println("  年龄在20-28之间: " + u));
        System.out.println();
        
        System.out.println("📦 示例7: JPQL查询 - 成年用户\n");
        List<User> adults = userService.findAdultUsers(18);
        adults.forEach(u -> System.out.println("  成年用户: " + u));
        System.out.println();
        
        System.out.println("📦 示例8: 更新用户\n");
        User updateInfo = new User();
        updateInfo.setUsername("张三丰");
        updateInfo.setEmail("zhangsanfeng@example.com");
        updateInfo.setAge(26);
        User updated = userService.updateUser(1L, updateInfo);
        System.out.println("  更新后: " + updated + "\n");
        
        System.out.println("📦 示例9: 统计用户\n");
        long count = userService.countUsers();
        System.out.println("  用户总数: " + count + "\n");
        
        System.out.println("📦 示例10: 删除用户\n");
        userService.deleteUser(2L);
        System.out.println("  删除用户ID=2\n");
        
        System.out.println("📦 最终查询所有用户\n");
        List<User> finalUsers = userService.findAll();
        finalUsers.forEach(u -> System.out.println("  " + u));
        
        System.out.println("\n═══════════════════════════════════════════════════════════");
        System.out.println("Spring Data JPA 特性总结:");
        System.out.println("  ✅ 方法名解析查询");
        System.out.println("  ✅ 自定义JPQL/SQL");
        System.out.println("  ✅ 分页排序");
        System.out.println("  ✅ 事务管理");
        System.out.println("  ✅ 自动生成实现");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
}
