package com.example.demo.repository;

import com.example.demo.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.jdbc.DataJdbcTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@DataJdbcTest
@ActiveProfiles("test")
class SafeUserRepositoryTest {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private SafeUserRepository safeUserRepository;

    @BeforeEach
    void setUp() {
        safeUserRepository = new SafeUserRepository();
        safeUserRepository.jdbcTemplate = jdbcTemplate;

        jdbcTemplate.execute("DELETE FROM users");
        jdbcTemplate.execute("INSERT INTO users (username, password, email, role, active) VALUES ('alice', 'pass123', 'alice@test.com', 'ADMIN', TRUE)");
        jdbcTemplate.execute("INSERT INTO users (username, password, email, role, active) VALUES ('bob', 'pass456', 'bob@test.com', 'USER', TRUE)");
        jdbcTemplate.execute("INSERT INTO users (username, password, email, role, active) VALUES ('charlie', 'pass789', 'charlie@test.com', 'USER', FALSE)");
    }

    @Test
    void searchByUsername_shouldReturnCorrectUser() {
        List<User> users = safeUserRepository.searchByUsername("alice");
        assertEquals(1, users.size());
        assertEquals("alice", users.get(0).getUsername());
        assertEquals("ADMIN", users.get(0).getRole());
    }

    @Test
    void searchByUsername_shouldReturnEmptyForNonExistent() {
        List<User> users = safeUserRepository.searchByUsername("nonexistent");
        assertTrue(users.isEmpty());
    }

    @Test
    void searchByUsername_shouldNotBeVulnerableToSqlInjection() {
        List<User> users = safeUserRepository.searchByUsername("' OR '1'='1");
        assertTrue(users.isEmpty());
    }

    @Test
    void searchByUsername_shouldNotBeVulnerableToDropTable() {
        List<User> users = safeUserRepository.searchByUsername("'; DROP TABLE users; --");
        assertTrue(users.isEmpty());
        assertTrue(safeUserRepository.searchByUsername("alice").size() > 0);
    }

    @Test
    void searchByUsername_shouldNotBeVulnerableToUnionAttack() {
        List<User> users = safeUserRepository.searchByUsername("' UNION SELECT 1, 'hacked', 'pwd', 'email', 'ADMIN', TRUE --");
        assertTrue(users.isEmpty());
    }

    @Test
    void searchByEmail_shouldReturnMatchingUsers() {
        List<User> users = safeUserRepository.searchByEmail("test.com");
        assertEquals(3, users.size());
    }

    @Test
    void authenticate_shouldReturnTrueForValidCredentials() {
        assertTrue(safeUserRepository.authenticate("alice", "pass123"));
    }

    @Test
    void authenticate_shouldReturnFalseForInvalidPassword() {
        assertFalse(safeUserRepository.authenticate("alice", "wrongpassword"));
    }

    @Test
    void authenticate_shouldNotBeVulnerableToSqlInjection() {
        assertFalse(safeUserRepository.authenticate("' OR '1'='1' --", "anything"));
        assertFalse(safeUserRepository.authenticate("alice", "' OR '1'='1"));
    }

    @Test
    void findByRole_shouldReturnActiveUsersOnly() {
        List<User> users = safeUserRepository.findByRole("USER");
        assertEquals(1, users.size());
        assertEquals("bob", users.get(0).getUsername());
    }
}
