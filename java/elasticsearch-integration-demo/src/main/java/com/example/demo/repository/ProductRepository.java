package com.example.demo.repository;

import com.example.demo.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.annotations.Query;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 商品Repository
 * 
 * 继承ElasticsearchRepository获得基础CRUD和搜索功能
 */
@Repository
public interface ProductRepository extends ElasticsearchRepository<Product, String> {
    
    /**
     * 根据名称搜索（分词搜索）
     * Spring Data会自动实现此方法
     */
    List<Product> findByNameContaining(String name);
    
    /**
     * 根据分类查询
     */
    List<Product> findByCategory(String category);
    
    /**
     * 根据品牌查询
     */
    List<Product> findByBrand(String brand);
    
    /**
     * 根据价格范围查询
     */
    List<Product> findByPriceBetween(Double minPrice, Double maxPrice);
    
    /**
     * 根据名称或描述搜索
     */
    List<Product> findByNameContainingOrDescriptionContaining(String name, String description);
    
    /**
     * 分页查询
     */
    Page<Product> findByCategory(String category, Pageable pageable);
    
    /**
     * 自定义ES查询
     * 使用Elasticsearch Query DSL
     */
    @Query("{" +
            "  \"bool\": {" +
            "    \"must\": [" +
            "      { \"match\": { \"name\": \"?0\" } }," +
            "      { \"range\": { \"price\": { \"lte\": ?1 } } }" +
            "    ]" +
            "  }" +
            "}")
    List<Product> findByNameAndMaxPrice(String name, Double maxPrice);
}
