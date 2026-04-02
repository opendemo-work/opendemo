package com.example.demo;

import com.example.demo.config.WebConfig;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * Spring MVC演示应用
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║       Spring MVC Web开发演示                              ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(WebConfig.class);
        
        System.out.println("Spring MVC应用已启动\n");
        System.out.println("RESTful API端点:");
        System.out.println("  GET    /api/users      - 获取所有用户");
        System.out.println("  GET    /api/users/{id} - 根据ID获取用户");
        System.out.println("  POST   /api/users      - 创建用户");
        System.out.println("  PUT    /api/users/{id} - 更新用户");
        System.out.println("  DELETE /api/users/{id} - 删除用户");
        System.out.println("\n部署到Tomcat后可使用上述API\n");
        
        System.out.println("═══════════════════════════════════════════════════════════");
        System.out.println("Spring MVC核心组件:");
        System.out.println("  @Controller      - 控制器注解");
        System.out.println("  @RestController  - REST控制器");
        System.out.println("  @RequestMapping  - 请求映射");
        System.out.println("  @GetMapping      - GET请求");
        System.out.println("  @PostMapping     - POST请求");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
}
