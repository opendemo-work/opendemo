package com.opendemo.java.gradle;

import com.opendemo.java.gradle.model.Task;
import com.opendemo.java.gradle.repository.TaskRepository;
import com.opendemo.java.gradle.service.TaskService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class GradleBuildDemo {

    private static final Logger logger = LoggerFactory.getLogger(GradleBuildDemo.class);

    public static void main(String[] args) {
        logger.info("=== Gradle Build Script Demo ===");
        logger.info("本项目演示Gradle构建工具的基本用法");
        logger.info("");

        logger.info("--- 1. Gradle 核心概念 ---");
        printGradleConcepts();

        logger.info("");
        logger.info("--- 2. Task Service 演示 ---");
        demonstrateTaskService();
    }

    private static void printGradleConcepts() {
        String[] concepts = {
            "Gradle 核心概念:",
            "  - Project: 每个build.gradle对应一个Project对象",
            "  - Task: 构建的最小执行单元，类似Maven的goal",
            "  - Plugin: 提供预定义的Task和约定",
            "  - Dependency Management: 声明式依赖管理",
            "",
            "Gradle vs Maven 对比:",
            "  - 构建脚本: Groovy/Kotlin DSL vs XML",
            "  - 构建速度: 增量构建 + 构建缓存 vs 全量构建",
            "  - 灵活性: 高度可定制 vs 约定驱动",
            "  - 多项目支持: 天然支持 vs 需要配置模块",
        };
        for (String line : concepts) {
            logger.info(line);
        }
    }

    private static void demonstrateTaskService() {
        TaskService taskService = new TaskService(new TaskRepository());

        taskService.createTask("编译项目", "使用Gradle编译Java源代码");
        taskService.createTask("运行测试", "执行JUnit单元测试");
        taskService.createTask("打包发布", "构建JAR包并发布到仓库");

        List<Task> allTasks = taskService.getAllTasks();
        logger.info("已创建任务数量: {}", allTasks.size());

        for (Task task : allTasks) {
            logger.info("  任务: [{}] {} - {}", task.getStatus(), task.getTitle(), task.getDescription());
        }

        taskService.completeTask(allTasks.get(0).getId());
        Task completed = taskService.getTask(allTasks.get(0).getId());
        logger.info("完成任务 '{}' 后状态: {}", completed.getTitle(), completed.getStatus());
    }
}
