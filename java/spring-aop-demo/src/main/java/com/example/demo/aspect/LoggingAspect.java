package com.example.demo.aspect;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

import java.util.Arrays;

/**
 * 日志记录切面
 * 
 * 演示各种Advice类型：
 * - @Before: 前置通知
 * - @AfterReturning: 返回通知
 * - @AfterThrowing: 异常通知
 * - @After: 后置通知
 * - @Around: 环绕通知
 */
@Aspect
@Component
public class LoggingAspect {
    
    /**
     * 定义切点：拦截OrderService的所有方法
     */
    @Pointcut("execution(* com.example.demo.service.OrderService.*(..))")
    public void orderServicePointcut() {}
    
    /**
     * 前置通知：方法执行前调用
     */
    @Before("orderServicePointcut()")
    public void beforeAdvice(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        System.out.println("[AOP @Before] " + methodName + " 开始执行，参数: " + Arrays.toString(args));
    }
    
    /**
     * 返回通知：方法成功返回后调用
     */
    @AfterReturning(pointcut = "orderServicePointcut()", returning = "result")
    public void afterReturningAdvice(JoinPoint joinPoint, Object result) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[AOP @AfterReturning] " + methodName + " 执行成功，返回值: " + result);
    }
    
    /**
     * 异常通知：方法抛出异常后调用
     */
    @AfterThrowing(pointcut = "orderServicePointcut()", throwing = "exception")
    public void afterThrowingAdvice(JoinPoint joinPoint, Exception exception) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[AOP @AfterThrowing] " + methodName + " 抛出异常: " + exception.getMessage());
    }
    
    /**
     * 后置通知：无论方法是否成功，最后都会调用
     */
    @After("orderServicePointcut()")
    public void afterAdvice(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[AOP @After] " + methodName + " 执行结束\n");
    }
    
    /**
     * 环绕通知：包围方法执行，可以控制是否执行目标方法
     */
    @Around("execution(* com.example.demo.service.OrderService.processOrder(..))")
    public Object aroundAdvice(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[AOP @Around] " + methodName + " 环绕通知 - 前置处理");
        
        long startTime = System.currentTimeMillis();
        
        // 执行目标方法
        Object result = null;
        try {
            result = joinPoint.proceed();
        } catch (Exception e) {
            System.out.println("[AOP @Around] 捕获异常: " + e.getMessage());
            throw e;
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("[AOP @Around] " + methodName + " 执行耗时: " + (endTime - startTime) + "ms");
        System.out.println("[AOP @Around] 环绕通知 - 后置处理");
        
        return result;
    }
}
