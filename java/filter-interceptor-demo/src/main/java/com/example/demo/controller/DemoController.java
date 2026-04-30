package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class DemoController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from Filter Interceptor Demo!";
    }

    @GetMapping("/hello/{name}")
    public String helloName(@PathVariable String name) {
        return "Hello, " + name + "!";
    }

    @GetMapping("/public/status")
    public String status() {
        return "OK";
    }
}
