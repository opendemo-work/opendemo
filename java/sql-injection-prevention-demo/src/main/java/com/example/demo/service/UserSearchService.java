package com.example.demo.service;

import com.example.demo.entity.User;
import com.example.demo.repository.SafeUserRepository;
import com.example.demo.repository.VulnerableUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class UserSearchService {

    @Autowired
    private VulnerableUserRepository vulnerableUserRepository;

    @Autowired
    private SafeUserRepository safeUserRepository;

    public Map<String, Object> searchVulnerable(String username) {
        Map<String, Object> result = new LinkedHashMap<>();
        try {
            List<User> users = vulnerableUserRepository.searchByUsername(username);
            result.put("status", "SUCCESS");
            result.put("method", "字符串拼接（不安全）");
            result.put("input", username);
            result.put("results", users);
            result.put("count", users.size());
        } catch (Exception e) {
            result.put("status", "ERROR");
            result.put("method", "字符串拼接（不安全）");
            result.put("input", username);
            result.put("error", e.getMessage());
        }
        return result;
    }

    public Map<String, Object> searchSafe(String username) {
        Map<String, Object> result = new LinkedHashMap<>();
        try {
            List<User> users = safeUserRepository.searchByUsername(username);
            result.put("status", "SUCCESS");
            result.put("method", "PreparedStatement 参数化查询（安全）");
            result.put("input", username);
            result.put("results", users);
            result.put("count", users.size());
        } catch (Exception e) {
            result.put("status", "ERROR");
            result.put("method", "PreparedStatement 参数化查询（安全）");
            result.put("input", username);
            result.put("error", e.getMessage());
        }
        return result;
    }

    public Map<String, Object> authenticateVulnerable(String username, String password) {
        Map<String, Object> result = new LinkedHashMap<>();
        boolean authenticated = vulnerableUserRepository.authenticate(username, password);
        result.put("status", authenticated ? "AUTHENTICATED" : "FAILED");
        result.put("method", "字符串拼接（不安全）");
        result.put("warning", authenticated ? "注意：此方法容易受到 SQL 注入攻击" : "");
        return result;
    }

    public Map<String, Object> authenticateSafe(String username, String password) {
        Map<String, Object> result = new LinkedHashMap<>();
        boolean authenticated = safeUserRepository.authenticate(username, password);
        result.put("status", authenticated ? "AUTHENTICATED" : "FAILED");
        result.put("method", "PreparedStatement 参数化查询（安全）");
        return result;
    }

    public Map<String, Object> compareSearch(String username) {
        Map<String, Object> comparison = new LinkedHashMap<>();
        comparison.put("vulnerable", searchVulnerable(username));
        comparison.put("safe", searchSafe(username));
        comparison.put("explanation", "对比展示：相同输入在安全和不安全查询中的不同行为");
        return comparison;
    }
}
