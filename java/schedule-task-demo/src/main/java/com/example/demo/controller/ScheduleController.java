package com.example.demo.controller;

import com.example.demo.task.ScheduledTasks;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/schedule")
public class ScheduleController {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Autowired
    private ScheduledTasks scheduledTasks;

    @GetMapping("/status")
    public Map<String, Object> status() {
        Map<String, Object> status = new HashMap<>();
        status.put("time", LocalDateTime.now().format(formatter));
        status.put("executionCount", scheduledTasks.getExecutionCount());
        status.put("running", true);
        return status;
    }

    @PostMapping("/trigger")
    public Map<String, String> trigger() {
        Map<String, String> result = new HashMap<>();
        result.put("message", "手动触发成功");
        result.put("time", LocalDateTime.now().format(formatter));
        return result;
    }

    @GetMapping("/history")
    public Map<String, Object> history() {
        Map<String, Object> history = new HashMap<>();
        history.put("totalExecutions", scheduledTasks.getExecutionCount());
        history.put("currentTime", LocalDateTime.now().format(formatter));
        history.put("note", "定时任务执行记录保存在内存中");
        return history;
    }
}
