package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class ExternalApiService {

    private static final Logger logger = LoggerFactory.getLogger(ExternalApiService.class);
    private final RestTemplate restTemplate;

    public ExternalApiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String getPostById(int id) {
        String url = "https://jsonplaceholder.typicode.com/posts/" + id;
        logger.info("GET请求: {}", url);
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        logger.info("响应状态: {}", response.getStatusCode());
        return response.getBody();
    }

    public String createPost(Map<String, Object> postData) {
        String url = "https://jsonplaceholder.typicode.com/posts";
        logger.info("POST请求: {}", url);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(postData, headers);

        ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
        return response.getBody();
    }

    public String updatePost(int id, Map<String, Object> postData) {
        String url = "https://jsonplaceholder.typicode.com/posts/" + id;
        logger.info("PUT请求: {}", url);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(postData, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                url, HttpMethod.PUT, entity, String.class);
        return response.getBody();
    }

    public boolean deletePost(int id) {
        String url = "https://jsonplaceholder.typicode.com/posts/" + id;
        logger.info("DELETE请求: {}", url);
        ResponseEntity<Void> response = restTemplate.exchange(
                url, HttpMethod.DELETE, null, Void.class);
        return response.getStatusCode().is2xxSuccessful();
    }

    public String getUsers() {
        String url = "https://jsonplaceholder.typicode.com/users";
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }

    public ResponseEntity<String> exchangeRequest(String url, HttpMethod method,
                                                   Map<String, String> headers,
                                                   String body) {
        HttpHeaders httpHeaders = new HttpHeaders();
        headers.forEach(httpHeaders::add);
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<String> entity = new HttpEntity<>(body, httpHeaders);
        return restTemplate.exchange(url, method, entity, String.class);
    }
}
