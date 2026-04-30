package com.opendemo.java.gradle.service;

import com.opendemo.java.gradle.model.Task;
import com.opendemo.java.gradle.repository.TaskRepository;

import java.util.List;
import java.util.NoSuchElementException;

public class TaskService {

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    public Task createTask(String title, String description) {
        Task task = new Task(title, description);
        return taskRepository.save(task);
    }

    public Task getTask(String id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("未找到ID为 " + id + " 的任务"));
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    public Task completeTask(String id) {
        Task task = getTask(id);
        task.setStatus("COMPLETED");
        return taskRepository.save(task);
    }

    public Task cancelTask(String id) {
        Task task = getTask(id);
        task.setStatus("CANCELLED");
        return taskRepository.save(task);
    }

    public void deleteTask(String id) {
        taskRepository.deleteById(id);
    }

    public List<Task> getTasksByStatus(String status) {
        return taskRepository.findByStatus(status);
    }
}
