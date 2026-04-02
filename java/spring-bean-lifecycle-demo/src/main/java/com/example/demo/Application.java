package com.example.demo;

import com.example.demo.config.LifecycleConfig;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

/**
 * Spring Bean生命周期演示应用
 * 
 * 展示Bean从实例化到销毁的完整生命周期
 */
public class Application {
    
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════════╗");
        System.out.println("║     Spring Bean 生命周期完整演示                          ║");
        System.out.println("╚══════════════════════════════════════════════════════════╝\n");
        
        System.out.println("📦 步骤1: 创建IoC容器（开始Bean生命周期）\n");
        
        // 创建容器 - 这会触发所有Bean的创建和初始化
        AnnotationConfigApplicationContext context = 
                new AnnotationConfigApplicationContext(LifecycleConfig.class);
        
        System.out.println("\n✅ 容器创建完成，所有Bean初始化完成\n");
        
        // 获取Bean并使用
        System.out.println("📦 步骤2: 获取并使用Bean\n");
        LifecycleBean bean = context.getBean(LifecycleBean.class);
        bean.doSomething();
        
        System.out.println("\n📊 Bean信息:");
        System.out.println("   Bean名称: " + bean.getBeanName());
        System.out.println("   应用名称: " + bean.getAppName());
        
        // 关闭容器 - 触发销毁回调
        System.out.println("\n📦 步骤3: 关闭容器（触发Bean销毁）\n");
        context.close();
        
        System.out.println("\n✅ 容器关闭，所有Bean销毁完成");
        System.out.println("\n═══════════════════════════════════════════════════════════");
        System.out.println("Bean生命周期总结:");
        System.out.println("  [1] 构造器实例化");
        System.out.println("  [2] BeanNameAware.setBeanName()");
        System.out.println("  [3] BeanFactoryAware.setBeanFactory()");
        System.out.println("  [4] ApplicationContextAware.setApplicationContext()");
        System.out.println("  [5] BeanPostProcessor.postProcessBeforeInitialization()");
        System.out.println("  [6] @PostConstruct");
        System.out.println("  [7] InitializingBean.afterPropertiesSet()");
        System.out.println("  [8] 自定义init-method");
        System.out.println("  [9] BeanPostProcessor.postProcessAfterInitialization()");
        System.out.println("  [10] Bean就绪使用");
        System.out.println("  [11] @PreDestroy");
        System.out.println("  [12] DisposableBean.destroy()");
        System.out.println("  [13] 自定义destroy-method");
        System.out.println("═══════════════════════════════════════════════════════════");
    }
}
