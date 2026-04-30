package com.example.demo.controller;

import com.example.demo.service.UserSearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserSearchController {

    @Autowired
    private UserSearchService userSearchService;

    @GetMapping("/search/vulnerable")
    public ResponseEntity<Map<String, Object>> searchVulnerable(@RequestParam String username) {
        return ResponseEntity.ok(userSearchService.searchVulnerable(username));
    }

    @GetMapping("/search/safe")
    public ResponseEntity<Map<String, Object>> searchSafe(@RequestParam String username) {
        return ResponseEntity.ok(userSearchService.searchSafe(username));
    }

    @GetMapping("/search/compare")
    public ResponseEntity<Map<String, Object>> compareSearch(@RequestParam String username) {
        return ResponseEntity.ok(userSearchService.compareSearch(username));
    }

    @PostMapping("/auth/vulnerable")
    public ResponseEntity<Map<String, Object>> authenticateVulnerable(
            @RequestParam String username,
            @RequestParam String password) {
        return ResponseEntity.ok(userSearchService.authenticateVulnerable(username, password));
    }

    @PostMapping("/auth/safe")
    public ResponseEntity<Map<String, Object>> authenticateSafe(
            @RequestParam String username,
            @RequestParam String password) {
        return ResponseEntity.ok(userSearchService.authenticateSafe(username, password));
    }
}
