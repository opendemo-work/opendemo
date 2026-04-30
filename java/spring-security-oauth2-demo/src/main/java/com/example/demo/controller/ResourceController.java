package com.example.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

@RestController
@RequestMapping("/api")
public class ResourceController {

    @GetMapping("/public/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("status", "UP");
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/user/profile")
    public ResponseEntity<Map<String, Object>> getUserProfile(@AuthenticationPrincipal Jwt jwt) {
        Map<String, Object> profile = new LinkedHashMap<>();
        profile.put("username", jwt.getClaimAsString("sub"));
        profile.put("role", jwt.getClaimAsString("role"));
        profile.put("email", jwt.getClaimAsString("email"));
        return ResponseEntity.ok(profile);
    }

    @GetMapping("/admin/users")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<Map<String, Object>>> getUsers() {
        List<Map<String, Object>> users = new ArrayList<>();
        users.add(createUserMap("alice", "alice@example.com", "USER"));
        users.add(createUserMap("bob", "bob@example.com", "ADMIN"));
        users.add(createUserMap("charlie", "charlie@example.com", "USER"));
        return ResponseEntity.ok(users);
    }

    @DeleteMapping("/admin/users/{username}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Map<String, Object>> deleteUser(@PathVariable String username) {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("message", "User " + username + " deleted successfully");
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    private Map<String, Object> createUserMap(String username, String email, String role) {
        Map<String, Object> user = new LinkedHashMap<>();
        user.put("username", username);
        user.put("email", email);
        user.put("role", role);
        return user;
    }
}
