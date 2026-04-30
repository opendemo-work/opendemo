package com.example.demo.repository;

import com.example.demo.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.QueryHints;
import org.springframework.data.repository.query.Param;
import javax.persistence.QueryHint;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

public interface ProductRepository extends JpaRepository<Product, Long> {

    List<Product> findByCategory(String category);

    @Query("SELECT p FROM Product p WHERE p.category = :category")
    List<Product> findByCategoryWithQuery(@Param("category") String category);

    @Query("SELECT p FROM Product p WHERE p.category = :category AND p.price BETWEEN :minPrice AND :maxPrice")
    List<Product> findByCategoryAndPriceRange(@Param("category") String category,
                                               @Param("minPrice") BigDecimal minPrice,
                                               @Param("maxPrice") BigDecimal maxPrice);

    @Query("SELECT p.id, p.name, p.price FROM Product p WHERE p.category = :category")
    List<Object[]> findProjectedByCategory(@Param("category") String category);

    @Query("SELECT p FROM Product p WHERE p.name LIKE %:keyword% OR p.description LIKE %:keyword%")
    Page<Product> searchByKeyword(@Param("keyword") String keyword, Pageable pageable);

    @QueryHints(@QueryHint(name = org.hibernate.jpa.QueryHints.HINT_FETCH_SIZE, value = "100"))
    @Query("SELECT p FROM Product p WHERE p.active = true")
    List<Product> findAllActiveWithFetchSize();

    @Modifying
    @Query("UPDATE Product p SET p.price = p.price * :multiplier WHERE p.category = :category")
    int updatePriceByCategory(@Param("multiplier") BigDecimal multiplier, @Param("category") String category);

    @Modifying
    @Query("UPDATE Product p SET p.stockQuantity = :quantity WHERE p.id IN :ids")
    int batchUpdateStock(@Param("quantity") Integer quantity, @Param("ids") List<Long> ids);

    @Query("SELECT p.category, COUNT(p), AVG(p.price) FROM Product p GROUP BY p.category")
    List<Object[]> getCategoryStats();

    long countByCategory(String category);

    boolean existsBySku(String sku);

    Optional<Product> findBySku(String sku);

    List<Product> findByNameContainingIgnoreCase(String namePart);

    @Query(value = "SELECT * FROM products WHERE price > :minPrice ORDER BY price DESC LIMIT :limit", nativeQuery = true)
    List<Product> findTopByPriceNative(@Param("minPrice") BigDecimal minPrice, @Param("limit") int limit);
}
