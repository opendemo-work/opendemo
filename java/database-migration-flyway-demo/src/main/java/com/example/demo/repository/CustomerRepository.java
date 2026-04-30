package com.example.demo.repository;

import com.example.demo.entity.Customer;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.List;
import java.util.Optional;

@Repository
public class CustomerRepository {

    private final JdbcTemplate jdbcTemplate;

    private final RowMapper<Customer> rowMapper = (rs, rowNum) -> {
        Customer customer = new Customer();
        customer.setId(rs.getLong("id"));
        customer.setName(rs.getString("name"));
        customer.setEmail(rs.getString("email"));
        customer.setPhone(rs.getString("phone"));
        customer.setStatus(rs.getString("status"));
        return customer;
    };

    public CustomerRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Customer save(Customer customer) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbcTemplate.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO customer (name, email, phone, status) VALUES (?, ?, ?, ?)",
                    Statement.RETURN_GENERATED_KEYS
            );
            ps.setString(1, customer.getName());
            ps.setString(2, customer.getEmail());
            ps.setString(3, customer.getPhone());
            ps.setString(4, customer.getStatus());
            return ps;
        }, keyHolder);
        customer.setId(keyHolder.getKey().longValue());
        return customer;
    }

    public Optional<Customer> findById(Long id) {
        List<Customer> results = jdbcTemplate.query(
                "SELECT * FROM customer WHERE id = ?",
                rowMapper,
                id
        );
        return results.isEmpty() ? Optional.empty() : Optional.of(results.get(0));
    }

    public List<Customer> findAll() {
        return jdbcTemplate.query("SELECT * FROM customer", rowMapper);
    }

    public int update(Customer customer) {
        return jdbcTemplate.update(
                "UPDATE customer SET name = ?, email = ?, phone = ?, status = ? WHERE id = ?",
                customer.getName(),
                customer.getEmail(),
                customer.getPhone(),
                customer.getStatus(),
                customer.getId()
        );
    }

    public int deleteById(Long id) {
        return jdbcTemplate.update("DELETE FROM customer WHERE id = ?", id);
    }
}
