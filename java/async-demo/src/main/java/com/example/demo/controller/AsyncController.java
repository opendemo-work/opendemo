package com.example.demo.controller;

import com.example.demo.service.AsyncService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Future;

/**
 * 异步控制器
 */
@RestController
@RequestMapping("/api/async")
public class AsyncController {
    
    @Autowired
    private AsyncService asyncService;
    
    /**
     * 异步方法 - 无返回值
     */
    @GetMapping("/without-return")
    public ResponseEntity<Map<String, Object>> asyncWithoutReturn() {
        long start = System.currentTimeMillis();
        
        asyncService.asyncMethodWithoutReturn();
        
        long end = System.currentTimeMillis();
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", "异步任务已提交");
        result.put("time", (end - start) + "ms");
        result.put("thread", Thread.currentThread().getName());
        
        return ResponseEntity.ok(result);
    }
    
    /**
     * 异步方法 - 使用Future
     */
    @GetMapping("/with-future")
    public ResponseEntity<Map<String, Object>> asyncWithFuture() throws Exception {
        long start = System.currentTimeMillis();
        
        Future<String> future = asyncService.asyncMethodWithFuture();
        
        // 阻塞等待结果
        String taskResult = future.get();
        
        long end = System.currentTimeMillis();
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", taskResult);
        result.put("totalTime", (end - start) + "ms");
        result.put("thread", Thread.currentThread().getName());
        
        return ResponseEntity.ok(result);
    }
    
    /**
     * 异步方法 - 使用CompletableFuture
     */
    @GetMapping("/with-completable")
    public ResponseEntity<Map<String, Object>> asyncWithCompletableFuture() throws Exception {
        long start = System.currentTimeMillis();
        
        CompletableFuture<String> future1 = asyncService.asyncMethodWithCompletableFuture();
        CompletableFuture<String> future2 = asyncService.asyncMethodWithCompletableFuture();
        CompletableFuture<String> future3 = asyncService.asyncMethodWithCompletableFuture();
        
        // 等待所有任务完成
        CompletableFuture.allOf(future1, future2, future3).join();
        
        long end = System.currentTimeMillis();
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", "所有异步任务完成");
        result.put("totalTime", (end - start) + "ms");
        result.put("results", new String[]{
                future1.get(), future2.get(), future3.get()
        });
        
        return ResponseEntity.ok(result);
    }
    
    /**
     * 指定线程池
     */
    @GetMapping("/with-executor")
    public ResponseEntity<Map<String, Object>> asyncWithExecutor() {
        asyncService.asyncMethodWithExecutor();
        
        Map<String, Object> result = new HashMap<>();
        result.put("message", "任务已提交到自定义线程池");
        return ResponseEntity.ok(result);
    }
    
    /**
     * 对比：同步vs异步
     */
    @GetMapping("/compare")
    public ResponseEntity<Map<String, Object>> compare() throws Exception {
        Map<String, Object> result = new HashMap<>();
        
        // 同步执行
        long syncStart = System.currentTimeMillis();
        Thread.sleep(1000);
        Thread.sleep(1000);
        Thread.sleep(1000);
        long syncEnd = System.currentTimeMillis();
        result.put("syncTime", (syncEnd - syncStart) + "ms");
        
        // 异步执行
        long asyncStart = System.currentTimeMillis();
        CompletableFuture<String> f1 = asyncService.asyncMethodWithCompletableFuture();
        CompletableFuture<String> f2 = asyncService.asyncMethodWithCompletableFuture();
        CompletableFuture<String> f3 = asyncService.asyncMethodWithCompletableFuture();
        CompletableFuture.allOf(f1, f2, f3).join();
        long asyncEnd = System.currentTimeMillis();
        result.put("asyncTime", (asyncEnd - asyncStart) + "ms");
        
        return ResponseEntity.ok(result);
    }
}
