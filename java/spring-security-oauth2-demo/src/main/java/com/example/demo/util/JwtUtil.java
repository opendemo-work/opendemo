package com.example.demo.util;

import com.nimbusds.jose.JWSAlgorithm;
import com.nimbusds.jose.JWSHeader;
import com.nimbusds.jose.JWSSigner;
import com.nimbusds.jose.crypto.MACSigner;
import com.nimbusds.jwt.JWTClaimsSet;
import com.nimbusds.jwt.SignedJWT;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Date;
import java.util.Map;

@Component
public class JwtUtil {

    @Value("${jwt.secret}")
    private String secret;

    public String generateToken(String subject, Map<String, Object> customClaims, Instant expiry) {
        try {
            JWTClaimsSet.Builder claimsBuilder = new JWTClaimsSet.Builder()
                    .subject(subject)
                    .issuer("spring-security-oauth2-demo")
                    .issueTime(new Date())
                    .expirationTime(Date.from(expiry));

            for (Map.Entry<String, Object> entry : customClaims.entrySet()) {
                claimsBuilder.claim(entry.getKey(), entry.getValue());
            }

            SignedJWT signedJWT = new SignedJWT(
                    new JWSHeader(JWSAlgorithm.HS256),
                    claimsBuilder.build()
            );

            JWSSigner signer = new MACSigner(secret);
            signedJWT.sign(signer);
            return signedJWT.serialize();
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate JWT token", e);
        }
    }
}
