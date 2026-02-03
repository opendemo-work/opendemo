package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 接口实现类
public class Car implements Vehicle, SerializableMarker {
    private static final Logger logger = LoggerFactory.getLogger(Car.class);
    
    private String brand;
    private String model;
    private boolean running;
    private int currentSpeed;
    
    public Car(String brand, String model) {
        this.brand = brand;
        this.model = model;
        this.running = false;
        this.currentSpeed = 0;
        logger.info("创建汽车: {} {}", brand, model);
    }
    
    // 实现Vehicle接口的抽象方法
    @Override
    public void start() {
        if (!running) {
            running = true;
            currentSpeed = 0;
            logger.info("{} {} 发动机启动", brand, model);
        } else {
            logger.warn("汽车已在运行中");
        }
    }
    
    @Override
    public void stop() {
        if (running) {
            running = false;
            currentSpeed = 0;
            logger.info("{} {} 停止运行", brand, model);
        } else {
            logger.warn("汽车已停止");
        }
    }
    
    @Override
    public void accelerate(int speed) {
        if (running) {
            if (speed > 0) {
                currentSpeed += speed;
                logger.info("{} {} 加速到 {} km/h", brand, model, currentSpeed);
            } else {
                logger.warn("加速度必须为正数: {}", speed);
            }
        } else {
            logger.warn("请先启动汽车");
        }
    }
    
    // 可以选择性重写默认方法
    @Override
    public void honk() {
        logger.info("{} {} 鸣笛: 嘀嘀嘀!", brand, model);
    }
    
    @Override
    public boolean isRunning() {
        return running;
    }
    
    // Car特有方法
    public void openTrunk() {
        logger.info("{} {} 后备箱打开", brand, model);
    }
    
    public void turnOnLights() {
        logger.info("{} {} 车灯开启", brand, model);
    }
    
    public String getBrand() { return brand; }
    public String getModel() { return model; }
    public int getCurrentSpeed() { return currentSpeed; }
}