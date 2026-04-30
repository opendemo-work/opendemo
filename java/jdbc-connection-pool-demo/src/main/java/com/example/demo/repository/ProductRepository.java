package com.example.demo.repository;

import com.example.demo.entity.Product;
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
public class ProductRepository {

    private final JdbcTemplate jdbcTemplate;

    private final RowMapper<Product> rowMapper = (rs, rowNum) -> {
        Product product = new Product();
        product.setId(rs.getLong("id"));
        product.setName(rs.getString("name"));
        product.setPrice(rs.getDouble("price"));
        product.setStock(rs.getInt("stock"));
        product.setCategory(rs.getString("category"));
        return product;
    };

    public ProductRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Product save(Product product) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbcTemplate.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO product (name, price, stock, category) VALUES (?, ?, ?, ?)",
                    Statement.RETURN_GENERATED_KEYS
            );
            ps.setString(1, product.getName());
            ps.setDouble(2, product.getPrice());
            ps.setInt(3, product.getStock());
            ps.setString(4, product.getCategory());
            return ps;
        }, keyHolder);
        product.setId(keyHolder.getKey().longValue());
        return product;
    }

    public Optional<Product> findById(Long id) {
        List<Product> results = jdbcTemplate.query(
                "SELECT * FROM product WHERE id = ?",
                rowMapper,
                id
        );
        return results.isEmpty() ? Optional.empty() : Optional.of(results.get(0));
    }

    public List<Product> findAll() {
        return jdbcTemplate.query("SELECT * FROM product", rowMapper);
    }

    public List<Product> findByCategory(String category) {
        return jdbcTemplate.query(
                "SELECT * FROM product WHERE category = ?",
                rowMapper,
                category
        );
    }

    public int update(Product product) {
        return jdbcTemplate.update(
                "UPDATE product SET name = ?, price = ?, stock = ?, category = ? WHERE id = ?",
                product.getName(),
                product.getPrice(),
                product.getStock(),
                product.getCategory(),
                product.getId()
        );
    }

    public int deleteById(Long id) {
        return jdbcTemplate.update("DELETE FROM product WHERE id = ?", id);
    }

    public int count() {
        Integer count = jdbcTemplate.queryForObject("SELECT COUNT(*) FROM product", Integer.class);
        return count != null ? count : 0;
    }
}
