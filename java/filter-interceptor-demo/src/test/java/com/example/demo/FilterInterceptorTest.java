package com.example.demo;

import com.example.demo.filter.LoggingFilter;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;

import javax.servlet.ServletException;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

class FilterInterceptorTest {

    private LoggingFilter loggingFilter;
    private MockHttpServletRequest request;
    private MockHttpServletResponse response;
    private MockFilterChain filterChain;

    @BeforeEach
    void setUp() {
        loggingFilter = new LoggingFilter();
        request = new MockHttpServletRequest();
        response = new MockHttpServletResponse();
        filterChain = new MockFilterChain();
    }

    @Test
    void testLoggingFilterDoFilter() throws IOException, ServletException {
        request.setMethod("GET");
        request.setRequestURI("/api/hello");

        loggingFilter.doFilter(request, response, filterChain);

        assertEquals(200, response.getStatus());
    }

    @Test
    void testLoggingFilterWithPostRequest() throws IOException, ServletException {
        request.setMethod("POST");
        request.setRequestURI("/api/users");

        loggingFilter.doFilter(request, response, filterChain);

        assertEquals(200, response.getStatus());
    }

    @Test
    void testLoggingFilterInitDoesNotThrow() {
        assertDoesNotThrow(() -> loggingFilter.init(null));
    }

    @Test
    void testLoggingFilterDestroyDoesNotThrow() {
        assertDoesNotThrow(() -> loggingFilter.destroy());
    }

    @Test
    void testMockRequestNotNull() {
        assertNotNull(request);
        assertNotNull(response);
        assertNotNull(filterChain);
    }

    @Test
    void testRequestUri() {
        request.setRequestURI("/api/test");
        assertEquals("/api/test", request.getRequestURI());
    }

    @Test
    void testRequestMethod() {
        request.setMethod("DELETE");
        assertEquals("DELETE", request.getMethod());
    }
}
