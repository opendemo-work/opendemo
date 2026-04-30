package com.example.demo;

import com.example.demo.entity.Customer;
import com.example.demo.repository.CustomerRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class FlywayMigrationDemoApplicationTest {

    @Autowired
    private CustomerRepository customerRepository;

    @Test
    void contextLoads() {
    }

    @Test
    void testSave() {
        Customer customer = new Customer("测试客户", "test@example.com", "13800138000", "ACTIVE");
        Customer saved = customerRepository.save(customer);
        assertNotNull(saved.getId());
        assertEquals("测试客户", saved.getName());
    }

    @Test
    void testFindById() {
        Customer customer = new Customer("查找客户", "find@example.com", "13900139000", "ACTIVE");
        Customer saved = customerRepository.save(customer);
        Optional<Customer> found = customerRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals("查找客户", found.get().getName());
    }

    @Test
    void testFindAll() {
        customerRepository.save(new Customer("客户A", "a@example.com", "111", "ACTIVE"));
        customerRepository.save(new Customer("客户B", "b@example.com", "222", "ACTIVE"));
        List<Customer> customers = customerRepository.findAll();
        assertNotNull(customers);
        assertTrue(customers.size() >= 2);
    }

    @Test
    void testUpdate() {
        Customer customer = new Customer("更新前", "before@example.com", "333", "ACTIVE");
        Customer saved = customerRepository.save(customer);
        saved.setName("更新后");
        saved.setEmail("after@example.com");
        int rows = customerRepository.update(saved);
        assertEquals(1, rows);
        Optional<Customer> updated = customerRepository.findById(saved.getId());
        assertTrue(updated.isPresent());
        assertEquals("更新后", updated.get().getName());
    }

    @Test
    void testDelete() {
        Customer customer = new Customer("待删除", "delete@example.com", "444", "ACTIVE");
        Customer saved = customerRepository.save(customer);
        int rows = customerRepository.deleteById(saved.getId());
        assertEquals(1, rows);
        Optional<Customer> found = customerRepository.findById(saved.getId());
        assertFalse(found.isPresent());
    }

    @Test
    void testFlywayMigrationsApplied() {
        Customer customer = new Customer("迁移验证", "flyway@example.com", "555", "ACTIVE");
        Customer saved = customerRepository.save(customer);
        Optional<Customer> found = customerRepository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertNotNull(found.get().getEmail());
        assertNotNull(found.get().getStatus());
    }
}
