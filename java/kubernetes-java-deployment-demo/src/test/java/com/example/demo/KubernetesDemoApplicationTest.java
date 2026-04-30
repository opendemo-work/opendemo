package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class KubernetesDemoApplicationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void contextLoads() {
    }

    @Test
    void testHealthEndpoint() throws Exception {
        mockMvc.perform(get("/health"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.application").exists())
                .andExpect(jsonPath("$.timestamp").exists());
    }

    @Test
    void testLivenessEndpoint() throws Exception {
        mockMvc.perform(get("/liveness"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("ALIVE"));
    }

    @Test
    void testReadinessEndpoint() throws Exception {
        mockMvc.perform(get("/readiness"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("READY"));
    }

    @Test
    void testInfoEndpoint() throws Exception {
        mockMvc.perform(get("/info"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.application").exists())
                .andExpect(jsonPath("$.version").exists())
                .andExpect(jsonPath("$.kubernetes").exists())
                .andExpect(jsonPath("$.kubernetes.namespace").exists());
    }

    @Test
    void testConfigEndpoint() throws Exception {
        mockMvc.perform(get("/config"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").exists())
                .andExpect(jsonPath("$.logLevel").exists());
    }
}
