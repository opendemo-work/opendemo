package com.example.demo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class HttpService {
    
    @Autowired
    private RestTemplate restTemplate;
    
    public String get(String url) {
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }
    
    public String post(String url, Map<String, Object> data) {
        ResponseEntity<String> response = restTemplate.postForEntity(url, data, String.class);
        return response.getBody();
    }
}
