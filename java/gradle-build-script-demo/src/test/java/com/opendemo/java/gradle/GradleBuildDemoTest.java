package com.opendemo.java.gradle;

import com.opendemo.java.gradle.model.Task;
import com.opendemo.java.gradle.repository.TaskRepository;
import com.opendemo.java.gradle.service.TaskService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

class GradleBuildDemoTest {

    private TaskService taskService;

    @BeforeEach
    void setUp() {
        taskService = new TaskService(new TaskRepository());
    }

    @Test
    void testMainRunsSuccessfully() {
        assertDoesNotThrow(() -> GradleBuildDemo.main(new String[]{}));
    }

    @Test
    void testCreateTask() {
        Task task = taskService.createTask("测试任务", "任务描述");
        assertNotNull(task.getId());
        assertEquals("测试任务", task.getTitle());
        assertEquals("PENDING", task.getStatus());
    }

    @Test
    void testGetTask() {
        Task created = taskService.createTask("获取任务", "测试获取");
        Task found = taskService.getTask(created.getId());
        assertEquals(created.getId(), found.getId());
    }

    @Test
    void testGetTaskNotFound() {
        assertThrows(NoSuchElementException.class, () -> taskService.getTask("nonexistent"));
    }

    @Test
    void testCompleteTask() {
        Task created = taskService.createTask("完成任务", "测试完成");
        Task completed = taskService.completeTask(created.getId());
        assertEquals("COMPLETED", completed.getStatus());
    }

    @Test
    void testCancelTask() {
        Task created = taskService.createTask("取消任务", "测试取消");
        Task cancelled = taskService.cancelTask(created.getId());
        assertEquals("CANCELLED", cancelled.getStatus());
    }

    @Test
    void testGetAllTasks() {
        taskService.createTask("任务1", "描述1");
        taskService.createTask("任务2", "描述2");
        List<Task> tasks = taskService.getAllTasks();
        assertEquals(2, tasks.size());
    }

    @Test
    void testGetTasksByStatus() {
        Task t1 = taskService.createTask("待办", "描述");
        taskService.createTask("另一个待办", "描述2");
        taskService.completeTask(t1.getId());
        List<Task> pending = taskService.getTasksByStatus("PENDING");
        assertEquals(1, pending.size());
        List<Task> completed = taskService.getTasksByStatus("COMPLETED");
        assertEquals(1, completed.size());
    }

    @Test
    void testDeleteTask() {
        Task created = taskService.createTask("删除任务", "测试删除");
        taskService.deleteTask(created.getId());
        assertEquals(0, taskService.getAllTasks().size());
    }
}
