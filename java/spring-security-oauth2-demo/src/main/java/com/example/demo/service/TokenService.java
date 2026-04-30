package com.example.demo.service;

import com.example.demo.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.*;

@Service
public class TokenService {

    @Autowired
    private JwtUtil jwtUtil;

    private static final long ACCESS_TOKEN_EXPIRY_SECONDS = 3600;
    private static final long REFRESH_TOKEN_EXPIRY_SECONDS = 86400;

    public Map<String, Object> generateToken(String username, String role) {
        Instant now = Instant.now();
        Instant accessExpiry = now.plusSeconds(ACCESS_TOKEN_EXPIRY_SECONDS);
        Instant refreshExpiry = now.plusSeconds(REFRESH_TOKEN_EXPIRY_SECONDS);

        Map<String, Object> claims = new HashMap<>();
        claims.put("role", role);
        claims.put("email", username + "@example.com");

        String accessToken = jwtUtil.generateToken(username, claims, accessExpiry);
        String refreshToken = jwtUtil.generateToken(username, Collections.singletonMap("type", "refresh"), refreshExpiry);

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("access_token", accessToken);
        response.put("refresh_token", refreshToken);
        response.put("token_type", "Bearer");
        response.put("expires_in", ACCESS_TOKEN_EXPIRY_SECONDS);
        response.put("scope", role.toLowerCase());
        return response;
    }

    public Map<String, Object> extractTokenInfo(Jwt jwt) {
        Map<String, Object> info = new LinkedHashMap<>();
        info.put("subject", jwt.getSubject());
        info.put("issuedAt", jwt.getIssuedAt());
        info.put("expiresAt", jwt.getExpiresAt());
        info.put("issuer", jwt.getIssuer());
        info.put("claims", jwt.getClaims());
        return info;
    }

    public Map<String, Object> extractUserInfo(Jwt jwt) {
        Map<String, Object> userInfo = new LinkedHashMap<>();
        userInfo.put("username", jwt.getSubject());
        userInfo.put("role", jwt.getClaimAsString("role"));
        userInfo.put("email", jwt.getClaimAsString("email"));
        return userInfo;
    }
}
