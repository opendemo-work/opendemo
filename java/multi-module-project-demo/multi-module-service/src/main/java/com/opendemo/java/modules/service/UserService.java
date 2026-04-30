package com.opendemo.java.modules.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

public class UserService {

    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    private final List<UserInfo> users = new ArrayList<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    public UserInfo createUser(String username, String email) {
        validateUser(username, email);
        UserInfo user = new UserInfo(idGenerator.getAndIncrement(), username, email);
        users.add(user);
        logger.info("创建用户: {}", user);
        return user;
    }

    public UserInfo getUserById(Long id) {
        return users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("用户不存在: " + id));
    }

    public List<UserInfo> getAllUsers() {
        return Collections.unmodifiableList(users);
    }

    public boolean deleteUser(Long id) {
        return users.removeIf(u -> u.getId().equals(id));
    }

    private void validateUser(String username, String email) {
        if (username == null || username.trim().isEmpty()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("邮箱格式不正确");
        }
    }

    public static class UserInfo {
        private final Long id;
        private final String username;
        private final String email;

        public UserInfo(Long id, String username, String email) {
            this.id = id;
            this.username = username;
            this.email = email;
        }

        public Long getId() { return id; }
        public String getUsername() { return username; }
        public String getEmail() { return email; }

        @Override
        public String toString() {
            return "UserInfo{id=" + id + ", username='" + username + "', email='" + email + "'}";
        }
    }
}
