package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ActuatorApplication {
    public static void main(String[] args) {
        SpringApplication.run(ActuatorApplication.class, args);
        System.out.println("Actuator监控演示应用启动成功!");
        System.out.println("健康检查: http://localhost:8080/actuator/health");
        System.out.println("指标监控: http://localhost:8080/actuator/metrics");
        System.out.println("应用信息: http://localhost:8080/actuator/info");
    }
}
