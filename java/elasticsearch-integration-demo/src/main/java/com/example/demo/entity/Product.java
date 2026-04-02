package com.example.demo.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;
import org.springframework.data.elasticsearch.annotations.Setting;

/**
 * 商品实体
 * 
 * @Document: 标记为ES文档
 * indexName: 索引名称
 * shards: 分片数
 * replicas: 副本数
 */
@Document(indexName = "products", shards = 1, replicas = 0)
@Setting(settingPath = "elasticsearch-settings.json")
public class Product {
    
    @Id
    private String id;
    
    /**
     * 商品名称
     * type = FieldType.Text: 会被分词，用于全文搜索
     * analyzer: 指定分词器
     */
    @Field(type = FieldType.Text, analyzer = "ik_max_word", searchAnalyzer = "ik_smart")
    private String name;
    
    /**
     * 商品描述
     */
    @Field(type = FieldType.Text, analyzer = "ik_max_word")
    private String description;
    
    /**
     * 商品价格
     * type = FieldType.Double: 数值类型
     */
    @Field(type = FieldType.Double)
    private Double price;
    
    /**
     * 商品分类
     * type = FieldType.Keyword: 不会被分词，用于精确匹配和聚合
     */
    @Field(type = FieldType.Keyword)
    private String category;
    
    /**
     * 品牌
     */
    @Field(type = FieldType.Keyword)
    private String brand;
    
    /**
     * 库存数量
     */
    @Field(type = FieldType.Integer)
    private Integer stock;
    
    public Product() {
    }
    
    public Product(String id, String name, String description, Double price, 
                   String category, String brand, Integer stock) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
        this.category = category;
        this.brand = brand;
        this.stock = stock;
    }
    
    public String getId() {
        return id;
    }
    
    public void setId(String id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public Double getPrice() {
        return price;
    }
    
    public void setPrice(Double price) {
        this.price = price;
    }
    
    public String getCategory() {
        return category;
    }
    
    public void setCategory(String category) {
        this.category = category;
    }
    
    public String getBrand() {
        return brand;
    }
    
    public void setBrand(String brand) {
        this.brand = brand;
    }
    
    public Integer getStock() {
        return stock;
    }
    
    public void setStock(Integer stock) {
        this.stock = stock;
    }
    
    @Override
    public String toString() {
        return "Product{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", price=" + price +
                ", category='" + category + '\'' +
                ", brand='" + brand + '\'' +
                '}';
    }
}
