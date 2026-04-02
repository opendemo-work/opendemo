package com.example.demo.processor;

import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.stereotype.Component;

/**
 * 自定义BeanPostProcessor
 * 
 * 演示Bean初始化前后处理器
 * 可以对所有Bean进行自定义处理
 */
@Component
public class CustomBeanPostProcessor implements BeanPostProcessor {
    
    /**
     * 在Bean初始化之前调用
     */
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        if (beanName.equals("lifecycleBean")) {
            System.out.println("[5] BeanPostProcessor.postProcessBeforeInitialization(): " + beanName);
        }
        return bean;
    }
    
    /**
     * 在Bean初始化之后调用
     */
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        if (beanName.equals("lifecycleBean")) {
            System.out.println("[9] BeanPostProcessor.postProcessAfterInitialization(): " + beanName);
        }
        return bean;
    }
}
