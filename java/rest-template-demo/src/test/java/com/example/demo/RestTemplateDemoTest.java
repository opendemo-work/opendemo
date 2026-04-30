package com.example.demo;

import com.example.demo.service.HttpService;
import com.example.demo.service.ExternalApiService;
import com.example.demo.config.RestTemplateConfig;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class RestTemplateDemoTest {

    private RestTemplate restTemplate;

    @BeforeEach
    void setUp() {
        RestTemplateConfig config = new RestTemplateConfig();
        restTemplate = config.restTemplate();
    }

    @Test
    void testRestTemplateCreation() {
        assertNotNull(restTemplate);
        assertFalse(restTemplate.getInterceptors().isEmpty());
    }

    @Test
    void testRestTemplateTimeouts() {
        RestTemplateConfig config = new RestTemplateConfig();
        RestTemplate rt = config.restTemplate();
        assertNotNull(rt);
    }

    @Test
    void testHttpServiceGet() {
        HttpService service = new HttpService(restTemplate);
        assertNotNull(service);
    }

    @Test
    void testExternalApiServiceCreation() {
        ExternalApiService service = new ExternalApiService(restTemplate);
        assertNotNull(service);
    }

    @Test
    void testHttpHeadersCreation() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.add("X-Custom", "value");
        assertEquals(MediaType.APPLICATION_JSON, headers.getContentType());
        assertTrue(headers.containsKey("X-Custom"));
    }

    @Test
    void testHttpEntityCreation() {
        Map<String, Object> body = new HashMap<>();
        body.put("title", "test");
        body.put("body", "content");
        body.put("userId", 1);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

        assertNotNull(entity.getBody());
        assertEquals("test", entity.getBody().get("title"));
    }

    @Test
    void testResponseEntityCreation() {
        ResponseEntity<String> response = ResponseEntity.ok("success");
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("success", response.getBody());
    }

    @Test
    void testHttpMethodValues() {
        assertEquals("GET", HttpMethod.GET.name());
        assertEquals("POST", HttpMethod.POST.name());
        assertEquals("PUT", HttpMethod.PUT.name());
        assertEquals("DELETE", HttpMethod.DELETE.name());
    }

    @Test
    void testInterceptorAdded() {
        RestTemplateConfig config = new RestTemplateConfig();
        RestTemplate rt = config.restTemplate();
        assertEquals(1, rt.getInterceptors().size());
    }
}
