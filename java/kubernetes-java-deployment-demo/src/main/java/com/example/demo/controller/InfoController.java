package com.example.demo.controller;

import com.example.demo.config.KubernetesConfig;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.util.LinkedHashMap;
import java.util.Map;

@RestController
public class InfoController {

    private final KubernetesConfig kubernetesConfig;
    private final Environment environment;

    @Value("${spring.application.name:kubernetes-demo}")
    private String applicationName;

    @Value("${project.version:1.0.0}")
    private String version;

    public InfoController(KubernetesConfig kubernetesConfig, Environment environment) {
        this.kubernetesConfig = kubernetesConfig;
        this.environment = environment;
    }

    @GetMapping("/info")
    public Map<String, Object> info() {
        RuntimeMXBean runtimeMXBean = ManagementFactory.getRuntimeMXBean();
        Runtime runtime = Runtime.getRuntime();

        Map<String, Object> info = new LinkedHashMap<>();
        info.put("application", applicationName);
        info.put("version", version);
        info.put("profile", String.join(",", environment.getActiveProfiles()));
        info.put("javaVersion", System.getProperty("java.version"));
        info.put("jvmName", runtimeMXBean.getVmName());
        info.put("jvmUptime", runtimeMXBean.getUptime() + "ms");
        info.put("processors", runtime.availableProcessors());
        info.put("maxMemory", runtime.maxMemory() / 1024 / 1024 + "MB");
        info.put("totalMemory", runtime.totalMemory() / 1024 / 1024 + "MB");
        info.put("freeMemory", runtime.freeMemory() / 1024 / 1024 + "MB");

        Map<String, Object> k8sInfo = new LinkedHashMap<>();
        k8sInfo.put("namespace", kubernetesConfig.getNamespace());
        k8sInfo.put("podName", kubernetesConfig.getPodName());
        k8sInfo.put("podIp", kubernetesConfig.getPodIp());
        k8sInfo.put("nodeName", kubernetesConfig.getNodeName());
        info.put("kubernetes", k8sInfo);

        return info;
    }

    @GetMapping("/config")
    public Map<String, Object> config() {
        Map<String, Object> result = new LinkedHashMap<>();
        result.put("message", kubernetesConfig.getWelcomeMessage());
        result.put("featureFlags", kubernetesConfig.getFeatureFlags());
        result.put("logLevel", kubernetesConfig.getLogLevel());
        result.put("maxConnections", kubernetesConfig.getMaxConnections());
        return result;
    }
}
