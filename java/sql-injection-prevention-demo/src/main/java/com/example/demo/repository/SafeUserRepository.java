package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public class SafeUserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> searchByUsername(String username) {
        String sql = "SELECT * FROM users WHERE username = ?";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setUsername(rs.getString("username"));
            user.setEmail(rs.getString("email"));
            user.setRole(rs.getString("role"));
            user.setActive(rs.getBoolean("active"));
            return user;
        }, username);
    }

    public List<User> searchByEmail(String email) {
        String sql = "SELECT * FROM users WHERE email LIKE ?";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setUsername(rs.getString("username"));
            user.setEmail(rs.getString("email"));
            user.setRole(rs.getString("role"));
            user.setActive(rs.getBoolean("active"));
            return user;
        }, "%" + email + "%");
    }

    public boolean authenticate(String username, String password) {
        String sql = "SELECT COUNT(*) FROM users WHERE username = ? AND password = ?";
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class, username, password);
        return count != null && count > 0;
    }

    public List<User> searchByUsernameWithPreparedStatement(String username) {
        return jdbcTemplate.query(
                connection -> {
                    java.sql.PreparedStatement ps = connection.prepareStatement(
                            "SELECT * FROM users WHERE username = ?"
                    );
                    ps.setString(1, username);
                    return ps;
                },
                (rs, rowNum) -> {
                    User user = new User();
                    user.setId(rs.getLong("id"));
                    user.setUsername(rs.getString("username"));
                    user.setEmail(rs.getString("email"));
                    user.setRole(rs.getString("role"));
                    user.setActive(rs.getBoolean("active"));
                    return user;
                }
        );
    }

    public List<User> findByRole(String role) {
        String sql = "SELECT * FROM users WHERE role = ? AND active = ?";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setUsername(rs.getString("username"));
            user.setEmail(rs.getString("email"));
            user.setRole(rs.getString("role"));
            user.setActive(rs.getBoolean("active"));
            return user;
        }, role, true);
    }
}
