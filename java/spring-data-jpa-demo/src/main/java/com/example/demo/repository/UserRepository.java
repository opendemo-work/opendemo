package com.example.demo.repository;

import com.example.demo.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 用户数据访问接口
 * 
 * 继承JpaRepository，获得基础的CRUD操作
 * 自定义查询方法展示Spring Data JPA的强大功能
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    /**
     * 根据用户名查询（方法名解析）
     */
    Optional<User> findByUsername(String username);
    
    /**
     * 根据邮箱查询
     */
    Optional<User> findByEmail(String email);
    
    /**
     * 根据用户名或邮箱查询
     */
    Optional<User> findByUsernameOrEmail(String username, String email);
    
    /**
     * 根据年龄范围查询
     */
    List<User> findByAgeBetween(int minAge, int maxAge);
    
    /**
     * 根据用户名模糊查询
     */
    List<User> findByUsernameContaining(String keyword);
    
    /**
     * 分页查询所有用户
     */
    Page<User> findAll(Pageable pageable);
    
    /**
     * 查询年龄大于指定值的用户
     */
    List<User> findByAgeGreaterThan(int age);
    
    /**
     * 使用JPQL查询
     */
    @Query("SELECT u FROM User u WHERE u.age >= :minAge ORDER BY u.age DESC")
    List<User> findAdultUsers(@Param("minAge") int minAge);
    
    /**
     * 使用原生SQL查询
     */
    @Query(value = "SELECT * FROM users WHERE age > ?1", nativeQuery = true)
    List<User> findUsersOlderThan(int age);
    
    /**
     * 统计用户数量
     */
    long countByAgeGreaterThan(int age);
    
    /**
     * 检查用户名是否存在
     */
    boolean existsByUsername(String username);
}
