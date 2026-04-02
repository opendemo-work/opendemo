package com.example.demo;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class AppStartupRunner implements ApplicationRunner {
    
    @Override
    public void run(ApplicationArguments args) {
        System.out.println("[ApplicationRunner] 应用启动完成...");
        System.out.println("[ApplicationRunner] Option参数: " + args.getOptionNames());
        System.out.println("[ApplicationRunner] 普通参数: " + args.getNonOptionArgs());
    }
}
