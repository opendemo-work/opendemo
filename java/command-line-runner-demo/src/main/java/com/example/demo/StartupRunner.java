package com.example.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupRunner implements CommandLineRunner {
    
    @Override
    public void run(String... args) {
        System.out.println("[CommandLineRunner] 应用启动完成，执行初始化任务...");
        for (String arg : args) {
            System.out.println("[CommandLineRunner] 参数: " + arg);
        }
    }
}
