package com.example.demo.aspect;

import com.example.demo.annotation.Loggable;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Aspect
@Component
public class LoggingAspect {

    @Around("@annotation(loggable)")
    public Object logMethod(ProceedingJoinPoint joinPoint, Loggable loggable) throws Throwable {
        Logger logger = LoggerFactory.getLogger(joinPoint.getTarget().getClass());
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        String methodName = signature.getName();

        String description = loggable.value().isEmpty() ? methodName : loggable.value();

        if (loggable.logParams()) {
            logger.info("[{}] 开始执行, 参数: {}", description, Arrays.toString(joinPoint.getArgs()));
        }

        long startTime = System.currentTimeMillis();
        try {
            Object result = joinPoint.proceed();
            long elapsedTime = System.currentTimeMillis() - startTime;

            if (loggable.logResult()) {
                logger.info("[{}] 执行成功, 返回值: {}", description, result);
            }
            if (loggable.logExecutionTime()) {
                logger.info("[{}] 执行耗时: {}ms", description, elapsedTime);
            }
            return result;
        } catch (Throwable ex) {
            long elapsedTime = System.currentTimeMillis() - startTime;
            logger.error("[{}] 执行异常, 耗时: {}ms, 异常: {}", description, elapsedTime, ex.getMessage());
            throw ex;
        }
    }

    @Around("execution(* com.example.demo.service.*.*(..))")
    public Object logServiceMethods(ProceedingJoinPoint joinPoint) throws Throwable {
        Logger logger = LoggerFactory.getLogger(joinPoint.getTarget().getClass());
        String methodName = joinPoint.getSignature().getName();

        logger.info("调用服务方法: {}", methodName);
        long start = System.currentTimeMillis();
        try {
            Object result = joinPoint.proceed();
            long elapsed = System.currentTimeMillis() - start;
            logger.info("服务方法 {} 执行完成, 耗时: {}ms", methodName, elapsed);
            return result;
        } catch (Exception e) {
            logger.error("服务方法 {} 执行失败: {}", methodName, e.getMessage());
            throw e;
        }
    }
}
