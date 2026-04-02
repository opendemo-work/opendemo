package com.example.demo;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

/**
 * Bean生命周期演示类
 * 
 * 实现了多个Spring生命周期接口，展示完整的生命周期回调
 */
@Component
public class LifecycleBean implements 
        BeanNameAware,           // 感知Bean名称
        BeanFactoryAware,        // 感知BeanFactory
        ApplicationContextAware, // 感知ApplicationContext
        InitializingBean,        // 初始化回调
        DisposableBean {         // 销毁回调
    
    private String beanName;
    private BeanFactory beanFactory;
    private ApplicationContext applicationContext;
    
    @Value("${app.name:DefaultApp}")
    private String appName;
    
    @Autowired(required = false)
    private DependencyBean dependencyBean;
    
    // ========== 1. 实例化阶段 ==========
    
    /**
     * 构造器
     */
    public LifecycleBean() {
        System.out.println("[1] 构造器: LifecycleBean 实例化");
    }
    
    // ========== 2. 属性赋值阶段 ==========
    
    /**
     * 依赖注入完成后显示
     */
    public void showDependency() {
        System.out.println("    依赖注入完成: appName=" + appName);
        if (dependencyBean != null) {
            System.out.println("    依赖Bean: " + dependencyBean.getClass().getSimpleName());
        }
    }
    
    // ========== 3. Aware接口回调 ==========
    
    @Override
    public void setBeanName(String name) {
        this.beanName = name;
        System.out.println("[2] BeanNameAware.setBeanName(): " + name);
    }
    
    @Override
    public void setBeanFactory(BeanFactory beanFactory) throws BeansException {
        this.beanFactory = beanFactory;
        System.out.println("[3] BeanFactoryAware.setBeanFactory(): " + beanFactory.getClass().getSimpleName());
    }
    
    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
        System.out.println("[4] ApplicationContextAware.setApplicationContext(): " + applicationContext.getClass().getSimpleName());
    }
    
    // ========== 4. BeanPostProcessor前置处理 ==========
    // 在CustomBeanPostProcessor中实现
    
    // ========== 5. 初始化阶段 ==========
    
    @PostConstruct
    public void postConstruct() {
        System.out.println("[6] @PostConstruct: 初始化开始");
    }
    
    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("[7] InitializingBean.afterPropertiesSet(): 属性设置完成");
        showDependency();
    }
    
    public void customInit() {
        System.out.println("[8] 自定义init-method: 初始化完成");
    }
    
    // ========== 6. BeanPostProcessor后置处理 ==========
    // 在CustomBeanPostProcessor中实现
    
    // ========== 7. Bean就绪使用 ==========
    
    public String getBeanName() {
        return beanName;
    }
    
    public String getAppName() {
        return appName;
    }
    
    public void doSomething() {
        System.out.println("[9] Bean使用中: LifecycleBean.doSomething()");
    }
    
    // ========== 8. 销毁阶段 ==========
    
    @PreDestroy
    public void preDestroy() {
        System.out.println("[10] @PreDestroy: 销毁开始");
    }
    
    @Override
    public void destroy() throws Exception {
        System.out.println("[11] DisposableBean.destroy(): 销毁中");
    }
    
    public void customDestroy() {
        System.out.println("[12] 自定义destroy-method: 销毁完成");
    }
}
