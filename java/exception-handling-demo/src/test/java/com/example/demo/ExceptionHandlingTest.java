package com.example.demo;

import com.example.demo.exception.BusinessException;
import com.example.demo.exception.ResourceNotFoundException;
import com.example.demo.handler.GlobalExceptionHandler;
import com.example.demo.model.ErrorResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mock.web.MockHttpServletRequest;

import static org.junit.jupiter.api.Assertions.*;

class ExceptionHandlingTest {

    private GlobalExceptionHandler handler;
    private MockHttpServletRequest request;

    @BeforeEach
    void setUp() {
        handler = new GlobalExceptionHandler();
        request = new MockHttpServletRequest();
        request.setRequestURI("/api/users/999");
    }

    @Test
    void testResourceNotFoundException() {
        ResourceNotFoundException ex = new ResourceNotFoundException("用户不存在: 999");
        ResponseEntity<ErrorResponse> response = handler.handleNotFound(ex, request);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(404, response.getBody().getStatus());
        assertEquals("Not Found", response.getBody().getError());
        assertEquals("用户不存在: 999", response.getBody().getMessage());
        assertEquals("/api/users/999", response.getBody().getPath());
    }

    @Test
    void testBusinessException() {
        BusinessException ex = new BusinessException(400001, "用户名不能为空");
        ResponseEntity<ErrorResponse> response = handler.handleBusiness(ex, request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(400, response.getBody().getStatus());
        assertEquals(400001, response.getBody().getCode());
        assertEquals("用户名不能为空", response.getBody().getMessage());
    }

    @Test
    void testIllegalArgumentException() {
        IllegalArgumentException ex = new IllegalArgumentException("参数不合法");
        ResponseEntity<ErrorResponse> response = handler.handleIllegalArgument(ex, request);

        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(400, response.getBody().getStatus());
        assertEquals("Bad Request", response.getBody().getError());
        assertEquals("参数不合法", response.getBody().getMessage());
    }

    @Test
    void testGenericException() {
        RuntimeException ex = new RuntimeException("系统内部错误");
        ResponseEntity<ErrorResponse> response = handler.handleGeneric(ex, request);

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(500, response.getBody().getStatus());
        assertEquals("Internal Server Error", response.getBody().getError());
        assertEquals("系统内部错误", response.getBody().getMessage());
    }

    @Test
    void testErrorResponseTimestamp() {
        ResourceNotFoundException ex = new ResourceNotFoundException("test");
        ResponseEntity<ErrorResponse> response = handler.handleNotFound(ex, request);

        assertNotNull(response.getBody());
        assertNotNull(response.getBody().getTimestamp());
    }

    @Test
    void testBusinessExceptionCode() {
        BusinessException ex = new BusinessException(400002, "余额不足");
        assertEquals(400002, ex.getCode());
        assertEquals("余额不足", ex.getMessage());
    }

    @Test
    void testResourceNotFoundExceptionMessage() {
        ResourceNotFoundException ex = new ResourceNotFoundException("订单不存在: 123");
        assertEquals("订单不存在: 123", ex.getMessage());
    }

    @Test
    void testErrorResponseWithCode() {
        ErrorResponse error = new ErrorResponse(400, 400001, "用户名不能为空", "/api/users");
        assertEquals(400, error.getStatus());
        assertEquals(400001, error.getCode());
        assertEquals("用户名不能为空", error.getMessage());
        assertEquals("/api/users", error.getPath());
        assertNull(error.getError());
    }

    @Test
    void testErrorResponseWithError() {
        ErrorResponse error = new ErrorResponse(404, "Not Found", "资源不存在", "/api/test");
        assertEquals(404, error.getStatus());
        assertEquals("Not Found", error.getError());
        assertNull(error.getCode());
    }

    @Test
    void testErrorResponseSetters() {
        ErrorResponse error = new ErrorResponse();
        error.setStatus(500);
        error.setError("Internal Server Error");
        error.setMessage("系统错误");
        error.setPath("/api/error");
        error.setCode(500001);

        assertEquals(500, error.getStatus());
        assertEquals("Internal Server Error", error.getError());
        assertEquals("系统错误", error.getMessage());
        assertEquals("/api/error", error.getPath());
        assertEquals(500001, error.getCode());
    }

    @Test
    void testBusinessExceptionInheritance() {
        BusinessException ex = new BusinessException(400001, "test");
        assertTrue(ex instanceof RuntimeException);
    }

    @Test
    void testResourceNotFoundExceptionInheritance() {
        ResourceNotFoundException ex = new ResourceNotFoundException("test");
        assertTrue(ex instanceof RuntimeException);
    }
}
