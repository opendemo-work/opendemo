package com.opendemo.java.encapsulation;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Properties;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;
import java.io.InputStream;
import java.io.IOException;

/**
 * Configuration配置类 - 演示封装的配置管理
 * 展示如何安全地管理和访问应用程序配置
 */
public class Configuration {
    private static final Logger logger = LoggerFactory.getLogger(Configuration.class);
    
    // 私有成员变量
    private final Map<String, String> configMap;
    private final String configSource;
    private volatile boolean loaded; // volatile确保内存可见性
    
    // 常量定义
    private static final String DEFAULT_CONFIG_FILE = "application.properties";
    private static final String ENV_PREFIX = "APP_";
    
    // 单例实例
    private static volatile Configuration instance;
    
    // 私有构造方法
    private Configuration() {
        this.configMap = new ConcurrentHashMap<>();
        this.configSource = DEFAULT_CONFIG_FILE;
        this.loaded = false;
        logger.info("创建Configuration实例");
    }
    
    // 单例获取方法
    public static Configuration getInstance() {
        if (instance == null) {
            synchronized (Configuration.class) {
                if (instance == null) {
                    instance = new Configuration();
                }
            }
        }
        return instance;
    }
    
    // 加载配置
    public synchronized void load() {
        if (loaded) {
            logger.debug("配置已加载，跳过重复加载");
            return;
        }
        
        try {
            // 1. 从配置文件加载
            loadFromFile(DEFAULT_CONFIG_FILE);
            
            // 2. 从环境变量加载（覆盖文件配置）
            loadFromEnvironment();
            
            // 3. 从系统属性加载（最高优先级）
            loadFromSystemProperties();
            
            loaded = true;
            logger.info("配置加载完成，共加载 {} 个配置项", configMap.size());
            
        } catch (Exception e) {
            logger.error("配置加载失败", e);
            throw new RuntimeException("配置加载失败", e);
        }
    }
    
    // 私有加载方法
    private void loadFromFile(String fileName) {
        try (InputStream inputStream = getClass().getClassLoader().getResourceAsStream(fileName)) {
            if (inputStream != null) {
                Properties props = new Properties();
                props.load(inputStream);
                
                props.forEach((key, value) -> {
                    if (key != null && value != null) {
                        configMap.put(key.toString(), value.toString());
                        logger.debug("从文件加载配置: {} = {}", key, value);
                    }
                });
            } else {
                logger.warn("未找到配置文件: {}", fileName);
            }
        } catch (IOException e) {
            logger.warn("读取配置文件失败: {}", fileName, e);
        }
    }
    
    private void loadFromEnvironment() {
        System.getenv().forEach((key, value) -> {
            if (key != null && key.startsWith(ENV_PREFIX) && value != null) {
                String configKey = key.substring(ENV_PREFIX.length()).toLowerCase();
                configMap.put(configKey, value);
                logger.debug("从环境变量加载配置: {} = {}", configKey, value);
            }
        });
    }
    
    private void loadFromSystemProperties() {
        System.getProperties().forEach((key, value) -> {
            if (key != null && key.toString().startsWith("app.") && value != null) {
                String configKey = key.toString().substring(4); // 移除"app."前缀
                configMap.put(configKey, value.toString());
                logger.debug("从系统属性加载配置: {} = {}", configKey, value);
            }
        });
    }
    
    // 配置获取方法 - 带默认值
    public String getProperty(String key) {
        ensureLoaded();
        return configMap.get(key);
    }
    
    public String getProperty(String key, String defaultValue) {
        ensureLoaded();
        return configMap.getOrDefault(key, defaultValue);
    }
    
    public int getIntProperty(String key, int defaultValue) {
        String value = getProperty(key);
        if (value == null) return defaultValue;
        
        try {
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            logger.warn("配置项 {} 的值 {} 无法转换为整数，使用默认值 {}", key, value, defaultValue);
            return defaultValue;
        }
    }
    
    public long getLongProperty(String key, long defaultValue) {
        String value = getProperty(key);
        if (value == null) return defaultValue;
        
        try {
            return Long.parseLong(value.trim());
        } catch (NumberFormatException e) {
            logger.warn("配置项 {} 的值 {} 无法转换为长整数，使用默认值 {}", key, value, defaultValue);
            return defaultValue;
        }
    }
    
    public boolean getBooleanProperty(String key, boolean defaultValue) {
        String value = getProperty(key);
        if (value == null) return defaultValue;
        
        return "true".equalsIgnoreCase(value.trim()) || "1".equals(value.trim());
    }
    
    public double getDoubleProperty(String key, double defaultValue) {
        String value = getProperty(key);
        if (value == null) return defaultValue;
        
        try {
            return Double.parseDouble(value.trim());
        } catch (NumberFormatException e) {
            logger.warn("配置项 {} 的值 {} 无法转换为双精度数，使用默认值 {}", key, value, defaultValue);
            return defaultValue;
        }
    }
    
    // 配置设置方法
    public synchronized void setProperty(String key, String value) {
        ensureLoaded();
        if (key != null && value != null) {
            configMap.put(key, value);
            logger.debug("设置配置项: {} = {}", key, value);
        }
    }
    
    // 批量操作
    public Map<String, String> getAllProperties() {
        ensureLoaded();
        return new ConcurrentHashMap<>(configMap);
    }
    
    public void setProperties(Map<String, String> properties) {
        if (properties != null) {
            properties.forEach(this::setProperty);
        }
    }
    
    // 配置信息方法
    public boolean containsProperty(String key) {
        ensureLoaded();
        return configMap.containsKey(key);
    }
    
    public int getPropertyCount() {
        ensureLoaded();
        return configMap.size();
    }
    
    public boolean isEmpty() {
        ensureLoaded();
        return configMap.isEmpty();
    }
    
    // 验证方法
    public boolean validateRequiredProperties(String... requiredKeys) {
        if (requiredKeys == null || requiredKeys.length == 0) {
            return true;
        }
        
        for (String key : requiredKeys) {
            if (!containsProperty(key) || getProperty(key) == null) {
                logger.error("缺少必需的配置项: {}", key);
                return false;
            }
        }
        return true;
    }
    
    // 重新加载配置
    public synchronized void reload() {
        logger.info("重新加载配置");
        configMap.clear();
        loaded = false;
        load();
    }
    
    // 私有辅助方法
    private void ensureLoaded() {
        if (!loaded) {
            load();
        }
    }
    
    // 重写Object方法
    @Override
    public String toString() {
        ensureLoaded();
        return String.format("Configuration{source='%s', properties=%d, loaded=%s}", 
                           configSource, configMap.size(), loaded);
    }
    
    // 配置监听器接口
    public interface ConfigListener {
        void onConfigChanged(String key, String oldValue, String newValue);
    }
    
    // 配置构建器类
    public static class Builder {
        private final Configuration config = new Configuration();
        
        public Builder setProperty(String key, String value) {
            config.setProperty(key, value);
            return this;
        }
        
        public Builder setProperties(Map<String, String> properties) {
            config.setProperties(properties);
            return this;
        }
        
        public Configuration build() {
            config.load();
            return config;
        }
    }
    
    // 静态工厂方法
    public static Configuration createDefault() {
        return new Builder().build();
    }
    
    public static Configuration createWithProperties(Map<String, String> properties) {
        return new Builder().setProperties(properties).build();
    }
}