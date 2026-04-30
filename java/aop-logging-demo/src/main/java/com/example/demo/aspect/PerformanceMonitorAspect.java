package com.example.demo.aspect;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.util.StopWatch;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Aspect
@Component
public class PerformanceMonitorAspect {

    private static final Logger logger = LoggerFactory.getLogger(PerformanceMonitorAspect.class);
    private final Map<String, AtomicLong> methodCallCount = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> methodTotalTime = new ConcurrentHashMap<>();

    @Around("execution(* com.example.demo.service.*.*(..))")
    public Object monitorPerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().toShortString();
        StopWatch stopWatch = new StopWatch();
        stopWatch.start();

        try {
            Object result = joinPoint.proceed();
            stopWatch.stop();
            recordMetrics(methodName, stopWatch.getTotalTimeMillis());
            return result;
        } catch (Throwable t) {
            stopWatch.stop();
            recordMetrics(methodName, stopWatch.getTotalTimeMillis());
            throw t;
        }
    }

    private void recordMetrics(String methodName, long elapsedTime) {
        methodCallCount.computeIfAbsent(methodName, k -> new AtomicLong(0)).incrementAndGet();
        methodTotalTime.computeIfAbsent(methodName, k -> new AtomicLong(0)).addAndGet(elapsedTime);

        long calls = methodCallCount.get(methodName).get();
        long totalTime = methodTotalTime.get(methodName).get();
        double avgTime = calls > 0 ? (double) totalTime / calls : 0;

        logger.info("[性能监控] 方法: {}, 调用次数: {}, 平均耗时: {:.2f}ms", methodName, calls, avgTime);
    }

    public Map<String, Map<String, Object>> getPerformanceStats() {
        Map<String, Map<String, Object>> stats = new HashMap<>();
        for (Map.Entry<String, AtomicLong> entry : methodCallCount.entrySet()) {
            String method = entry.getKey();
            long calls = entry.getValue().get();
            long totalTime = methodTotalTime.getOrDefault(method, new AtomicLong(0)).get();
            double avgTime = calls > 0 ? (double) totalTime / calls : 0;

            Map<String, Object> methodStats = new HashMap<>();
            methodStats.put("calls", calls);
            methodStats.put("totalTime", totalTime);
            methodStats.put("avgTime", avgTime);
            stats.put(method, methodStats);
        }
        return stats;
    }
}
