package com.example.demo.controller;

import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/csrf")
public class CsrfController {

    @GetMapping("/token")
    public Map<String, Object> getCsrfToken(HttpServletRequest request) {
        CsrfToken csrfToken = (CsrfToken) request.getAttribute(CsrfToken.class.getName());
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("headerName", csrfToken.getHeaderName());
        response.put("parameterName", csrfToken.getParameterName());
        response.put("token", csrfToken.getToken());
        response.put("message", "在后续请求中通过 Header 或参数携带此 CSRF Token");
        return response;
    }
}
