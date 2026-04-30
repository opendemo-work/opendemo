package com.example.demo.controller;

import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api")
public class ApiController {

    private final List<Map<String, String>> dataList = new ArrayList<>();

    public ApiController() {
        for (int i = 1; i <= 5; i++) {
            Map<String, String> item = new HashMap<>();
            item.put("id", String.valueOf(i));
            item.put("name", "项目" + i);
            item.put("description", "这是第" + i + "个测试数据");
            dataList.add(item);
        }
    }

    @GetMapping("/data")
    public Map<String, Object> getData() {
        Map<String, Object> result = new HashMap<>();
        result.put("message", "CORS配置成功");
        result.put("data", dataList);
        result.put("timestamp", System.currentTimeMillis());
        return result;
    }

    @GetMapping("/data/{id}")
    public Map<String, String> getDataById(@PathVariable String id) {
        return dataList.stream()
                .filter(item -> id.equals(item.get("id")))
                .findFirst()
                .orElse(Collections.emptyMap());
    }

    @PostMapping("/data")
    public Map<String, String> createData(@RequestBody Map<String, String> data) {
        data.put("id", String.valueOf(dataList.size() + 1));
        dataList.add(data);
        Map<String, String> result = new HashMap<>();
        result.put("message", "创建成功");
        result.put("id", data.get("id"));
        return result;
    }

    @PutMapping("/data/{id}")
    public Map<String, String> updateData(@PathVariable String id, @RequestBody Map<String, String> data) {
        Map<String, String> result = new HashMap<>();
        dataList.stream()
                .filter(item -> id.equals(item.get("id")))
                .findFirst()
                .ifPresent(item -> {
                    item.putAll(data);
                    item.put("id", id);
                });
        result.put("message", "更新成功");
        result.put("id", id);
        return result;
    }

    @DeleteMapping("/data/{id}")
    public Map<String, String> deleteData(@PathVariable String id) {
        dataList.removeIf(item -> id.equals(item.get("id")));
        Map<String, String> result = new HashMap<>();
        result.put("message", "删除成功");
        result.put("id", id);
        return result;
    }
}
