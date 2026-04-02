package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 用户Repository
 * 
 * 继承MongoRepository获得基础CRUD功能
 */
@Repository
public interface UserRepository extends MongoRepository<User, String> {
    
    /**
     * 根据用户名查询
     * Spring Data会自动实现
     */
    User findByUsername(String username);
    
    /**
     * 根据邮箱查询
     */
    User findByEmail(String email);
    
    /**
     * 根据年龄范围查询
     */
    List<User> findByAgeBetween(Integer minAge, Integer maxAge);
    
    /**
     * 根据城市查询（嵌套字段）
     */
    List<User> findByAddressCity(String city);
    
    /**
     * 根据用户名模糊查询
     */
    List<User> findByUsernameContaining(String username);
    
    /**
     * 根据标签查询
     */
    List<User> findByTagsContaining(String tag);
    
    /**
     * 年龄大于指定值
     */
    List<User> findByAgeGreaterThan(Integer age);
    
    /**
     * 自定义MongoDB查询
     */
    @Query("{ 'age': { $gte: ?0, $lte: ?1 } }")
    List<User> findByAgeRange(Integer minAge, Integer maxAge);
    
    /**
     * 查询包含特定标签且年龄大于指定值的用户
     */
    @Query("{ 'tags': ?0, 'age': { $gt: ?1 } }")
    List<User> findByTagAndMinAge(String tag, Integer minAge);
}
