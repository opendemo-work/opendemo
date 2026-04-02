package com.example.demo;

import com.example.demo.config.GreetingAutoConfiguration;
import com.example.demo.service.GreetingService;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * Spring Boot自动配置演示应用
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║       Spring Boot 自动配置原理演示                        ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        System.out.println("📦 启动应用，观察自动配置过程...\n");
        
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(GreetingAutoConfiguration.class);
        
        System.out.println("\n📦 从容器中获取自动配置的GreetingService\n");
        
        GreetingService greetingService = context.getBean(GreetingService.class);
        
        System.out.println("  使用服务:");
        System.out.println("    " + greetingService.greet("Spring Boot"));
        System.out.println("    " + greetingService.greet("自动配置"));
        
        System.out.println("\n═══════════════════════════════════════════════════════════");
        System.out.println("Spring Boot自动配置核心机制:");
        System.out.println("  1. @ConditionalOnClass     - 类路径条件");
        System.out.println("  2. @ConditionalOnProperty   - 配置属性条件");
        System.out.println("  3. @ConditionalOnMissingBean - Bean缺失条件");
        System.out.println("  4. @EnableConfigurationProperties - 启用配置属性");
        System.out.println("  5. META-INF/spring.factories - 自动配置注册");
        System.out.println("═══════════════════════════════════════════════════════════");
        
        context.close();
    }
}
