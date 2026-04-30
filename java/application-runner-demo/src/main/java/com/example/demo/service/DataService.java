package com.example.demo.service;

import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class DataService {

    private final Map<String, String> dataStore = new ConcurrentHashMap<>();

    public void put(String key, String value) {
        dataStore.put(key, value);
    }

    public String get(String key) {
        return dataStore.get(key);
    }

    public Map<String, String> getAll() {
        return new ConcurrentHashMap<>(dataStore);
    }

    public int size() {
        return dataStore.size();
    }

    public void clear() {
        dataStore.clear();
    }

    public boolean contains(String key) {
        return dataStore.containsKey(key);
    }
}
