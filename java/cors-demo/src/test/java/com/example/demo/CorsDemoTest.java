package com.example.demo;

import com.example.demo.filter.CorsFilter;
import org.junit.jupiter.api.Test;

import javax.servlet.FilterChain;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class CorsDemoTest {

    @Test
    void testCorsFilterSetsHeaders() throws Exception {
        CorsFilter filter = new CorsFilter();
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain chain = mock(FilterChain.class);

        when(request.getMethod()).thenReturn("GET");
        when(request.getHeader("Origin")).thenReturn("http://localhost:3000");

        filter.doFilter(request, response, chain);

        verify(response).setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
        verify(response).setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        verify(response).setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With");
        verify(response).setHeader("Access-Control-Allow-Credentials", "true");
        verify(response).setHeader("Access-Control-Max-Age", "3600");
        verify(chain).doFilter(request, response);
    }

    @Test
    void testCorsFilterOptionsRequest() throws Exception {
        CorsFilter filter = new CorsFilter();
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain chain = mock(FilterChain.class);

        when(request.getMethod()).thenReturn("OPTIONS");
        when(request.getHeader("Origin")).thenReturn("http://localhost:3000");

        filter.doFilter(request, response, chain);

        verify(response).setStatus(HttpServletResponse.SC_OK);
        verify(chain, never()).doFilter(request, response);
    }

    @Test
    void testCorsFilterNullOrigin() throws Exception {
        CorsFilter filter = new CorsFilter();
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain chain = mock(FilterChain.class);

        when(request.getMethod()).thenReturn("GET");
        when(request.getHeader("Origin")).thenReturn(null);

        filter.doFilter(request, response, chain);

        verify(response).setHeader("Access-Control-Allow-Origin", "*");
    }

    @Test
    void testApiControllerGetData() {
        com.example.demo.controller.ApiController controller = new com.example.demo.controller.ApiController();
        Map<String, Object> result = controller.getData();
        assertTrue(result.containsKey("message"));
        assertTrue(result.containsKey("data"));
        assertTrue(result.containsKey("timestamp"));
    }

    @Test
    void testApiControllerGetDataById() {
        com.example.demo.controller.ApiController controller = new com.example.demo.controller.ApiController();
        Map<String, String> result = controller.getDataById("1");
        assertEquals("1", result.get("id"));
        assertNotNull(result.get("name"));
    }

    @Test
    void testApiControllerCreateData() {
        com.example.demo.controller.ApiController controller = new com.example.demo.controller.ApiController();
        Map<String, String> data = new HashMap<>();
        data.put("name", "新项目");
        Map<String, String> result = controller.createData(data);
        assertEquals("创建成功", result.get("message"));
    }

    @Test
    void testCorsConfigCreation() {
        com.example.demo.config.CorsConfig config = new com.example.demo.config.CorsConfig();
        assertNotNull(config.corsConfigurer());
    }
}
