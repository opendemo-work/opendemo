package com.example.demo.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class KubernetesConfig {

    @Value("${KUBERNETES_NAMESPACE:default}")
    private String namespace;

    @Value("${HOSTNAME:localhost}")
    private String podName;

    @Value("${POD_IP:127.0.0.1}")
    private String podIp;

    @Value("${NODE_NAME:local-node}")
    private String nodeName;

    @Value("${app.welcome-message:欢迎使用Kubernetes部署演示应用}")
    private String welcomeMessage;

    @Value("${app.feature-flags:new-feature,experimental-api}")
    private String featureFlags;

    @Value("${app.log-level:INFO}")
    private String logLevel;

    @Value("${app.max-connections:100}")
    private int maxConnections;

    public String getNamespace() {
        return namespace;
    }

    public String getPodName() {
        return podName;
    }

    public String getPodIp() {
        return podIp;
    }

    public String getNodeName() {
        return nodeName;
    }

    public String getWelcomeMessage() {
        return welcomeMessage;
    }

    public String getFeatureFlags() {
        return featureFlags;
    }

    public String getLogLevel() {
        return logLevel;
    }

    public int getMaxConnections() {
        return maxConnections;
    }
}
