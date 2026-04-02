package com.example.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import javax.annotation.PostConstruct;

@SpringBootApplication
public class LogbackApplication {
    
    private static final Logger logger = LoggerFactory.getLogger(LogbackApplication.class);
    
    public static void main(String[] args) {
        SpringApplication.run(LogbackApplication.class, args);
    }
    
    @PostConstruct
    public void logMessages() {
        logger.trace("Trace message");
        logger.debug("Debug message");
        logger.info("Info message");
        logger.warn("Warn message");
        logger.error("Error message");
    }
}
