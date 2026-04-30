package com.opendemo.java.gradle.repository;

import com.opendemo.java.gradle.model.Task;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class TaskRepository {

    private final Map<String, Task> store = new ConcurrentHashMap<>();

    public Task save(Task task) {
        store.put(task.getId(), task);
        return task;
    }

    public Optional<Task> findById(String id) {
        return Optional.ofNullable(store.get(id));
    }

    public List<Task> findAll() {
        return new ArrayList<>(store.values());
    }

    public List<Task> findByStatus(String status) {
        return store.values().stream()
                .filter(task -> task.getStatus().equals(status))
                .collect(Collectors.toList());
    }

    public void deleteById(String id) {
        store.remove(id);
    }

    public boolean existsById(String id) {
        return store.containsKey(id);
    }

    public long count() {
        return store.size();
    }
}
