package com.example.demo.service;

import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.AsyncResult;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Future;

/**
 * 异步服务
 */
@Service
public class AsyncService {
    
    /**
     * 异步方法 - 无返回值
     */
    @Async
    public void asyncMethodWithoutReturn() {
        System.out.println("[异步方法-无返回值] 开始执行，线程: " + Thread.currentThread().getName());
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[异步方法-无返回值] 执行完成");
    }
    
    /**
     * 异步方法 - 使用Future返回
     */
    @Async
    public Future<String> asyncMethodWithFuture() {
        System.out.println("[异步方法-Future] 开始执行，线程: " + Thread.currentThread().getName());
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[异步方法-Future] 执行完成");
        return new AsyncResult<>("任务完成");
    }
    
    /**
     * 异步方法 - 使用CompletableFuture返回
     */
    @Async
    public CompletableFuture<String> asyncMethodWithCompletableFuture() {
        System.out.println("[异步方法-CompletableFuture] 开始执行，线程: " + Thread.currentThread().getName());
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[异步方法-CompletableFuture] 执行完成");
        return CompletableFuture.completedFuture("任务完成");
    }
    
    /**
     * 指定线程池
     */
    @Async("taskExecutor")
    public void asyncMethodWithExecutor() {
        System.out.println("[指定线程池] 开始执行，线程: " + Thread.currentThread().getName());
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("[指定线程池] 执行完成");
    }
}
