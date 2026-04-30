package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class VulnerableUserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> searchByUsername(String username) {
        String sql = "SELECT * FROM users WHERE username = '" + username + "'";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setUsername(rs.getString("username"));
            user.setEmail(rs.getString("email"));
            user.setRole(rs.getString("role"));
            user.setActive(rs.getBoolean("active"));
            return user;
        });
    }

    public List<User> searchByEmail(String email) {
        String sql = "SELECT * FROM users WHERE email LIKE '%" + email + "%'";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setUsername(rs.getString("username"));
            user.setEmail(rs.getString("email"));
            user.setRole(rs.getString("role"));
            user.setActive(rs.getBoolean("active"));
            return user;
        });
    }

    public boolean authenticate(String username, String password) {
        String sql = "SELECT COUNT(*) FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class);
        return count != null && count > 0;
    }
}
