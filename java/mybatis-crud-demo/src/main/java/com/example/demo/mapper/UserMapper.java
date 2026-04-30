package com.example.demo.mapper;

import com.example.demo.entity.User;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface UserMapper {

    @Insert("INSERT INTO user (username, email, age, phone, status) VALUES (#{username}, #{email}, #{age}, #{phone}, #{status})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);

    @Select("SELECT * FROM user WHERE id = #{id}")
    User findById(@Param("id") Long id);

    @Select("SELECT * FROM user")
    List<User> findAll();

    @Update("UPDATE user SET username = #{username}, email = #{email}, age = #{age}, phone = #{phone}, status = #{status} WHERE id = #{id}")
    int update(User user);

    @Delete("DELETE FROM user WHERE id = #{id}")
    int deleteById(@Param("id") Long id);

    @Select("SELECT * FROM user WHERE status = #{status}")
    List<User> findByStatus(@Param("status") String status);

    List<User> findByCondition(User user);

    List<User> findWithPagination(@Param("offset") int offset, @Param("limit") int limit);
}
