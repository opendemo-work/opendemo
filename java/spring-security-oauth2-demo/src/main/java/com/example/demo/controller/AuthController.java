package com.example.demo.controller;

import com.example.demo.dto.UserDto;
import com.example.demo.service.TokenService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private TokenService tokenService;

    @PostMapping("/token")
    public ResponseEntity<Map<String, Object>> generateToken(@RequestBody UserDto userDto) {
        Map<String, Object> tokenResponse = tokenService.generateToken(
                userDto.getUsername(), userDto.getRole()
        );
        return ResponseEntity.ok(tokenResponse);
    }

    @GetMapping("/token-info")
    public ResponseEntity<Map<String, Object>> getTokenInfo(@AuthenticationPrincipal Jwt jwt) {
        return ResponseEntity.ok(tokenService.extractTokenInfo(jwt));
    }

    @GetMapping("/userinfo")
    public ResponseEntity<Map<String, Object>> getUserInfo(@AuthenticationPrincipal Jwt jwt) {
        return ResponseEntity.ok(tokenService.extractUserInfo(jwt));
    }
}
