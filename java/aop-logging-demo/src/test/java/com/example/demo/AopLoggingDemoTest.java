package com.example.demo;

import com.example.demo.annotation.Loggable;
import com.example.demo.aspect.PerformanceMonitorAspect;
import com.example.demo.service.UserService;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class AopLoggingDemoTest {

    @Test
    void testLoggableAnnotation() throws NoSuchMethodException {
        assertTrue(UserService.class.getMethod("findById", Long.class)
                .isAnnotationPresent(Loggable.class));
    }

    @Test
    void testLoggableAttributes() throws NoSuchMethodException {
        Loggable loggable = UserService.class.getMethod("findById", Long.class)
                .getAnnotation(Loggable.class);
        assertEquals("查询用户", loggable.value());
        assertTrue(loggable.logParams());
        assertTrue(loggable.logResult());
        assertTrue(loggable.logExecutionTime());
    }

    @Test
    void testUserServiceFindById() {
        UserService service = new UserService();
        String user = service.findById(1L);
        assertEquals("张三", user);
    }

    @Test
    void testUserServiceFindAll() {
        UserService service = new UserService();
        List<String> users = service.findAll();
        assertEquals(3, users.size());
    }

    @Test
    void testUserServiceCreate() {
        UserService service = new UserService();
        String result = service.createUser(4L, "赵六");
        assertEquals("用户创建成功: 赵六", result);
    }

    @Test
    void testUserServiceDelete() {
        UserService service = new UserService();
        assertTrue(service.deleteUser(1L));
        assertFalse(service.deleteUser(999L));
    }

    @Test
    void testUserServiceUpdate() {
        UserService service = new UserService();
        String result = service.updateUser(1L, "张三丰");
        assertEquals("用户更新成功: 张三丰", result);
    }

    @Test
    void testUserServiceUpdateNotFound() {
        UserService service = new UserService();
        assertThrows(IllegalArgumentException.class, () -> service.updateUser(999L, "不存在"));
    }

    @Test
    void testPerformanceMonitorStats() {
        PerformanceMonitorAspect aspect = new PerformanceMonitorAspect();
        Map<String, Map<String, Object>> stats = aspect.getPerformanceStats();
        assertNotNull(stats);
    }
}
