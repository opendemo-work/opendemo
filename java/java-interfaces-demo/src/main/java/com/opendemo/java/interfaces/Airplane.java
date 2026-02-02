package com.opendemo.java.interfaces;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 多接口实现示例
public class Airplane implements Vehicle, FlyingVehicle {
    private static final Logger logger = LoggerFactory.getLogger(Airplane.class);
    
    private String airline;
    private String flightNumber;
    private boolean flying;
    private int altitude;
    
    public Airplane(String airline, String flightNumber) {
        this.airline = airline;
        this.flightNumber = flightNumber;
        this.flying = false;
        this.altitude = 0;
        logger.info("创建飞机: {} 航班{}", airline, flightNumber);
    }
    
    // 实现Vehicle接口方法
    @Override
    public void start() {
        logger.info("{} 航班{} 发动机启动", airline, flightNumber);
    }
    
    @Override
    public void stop() {
        if (flying) {
            logger.warn("飞行中无法停止，请先降落");
        } else {
            logger.info("{} 航班{} 关闭发动机", airline, flightNumber);
        }
    }
    
    @Override
    public void accelerate(int speed) {
        if (flying) {
            altitude += speed;
            logger.info("爬升至 {} 米高度", altitude);
        } else {
            logger.info("地面滑行加速");
        }
    }
    
    // 实现FlyingVehicle接口方法
    @Override
    public void takeOff() {
        if (!flying) {
            flying = true;
            altitude = 1000;
            logger.info("{} 航班{} 起飞，高度 {} 米", airline, flightNumber, altitude);
        } else {
            logger.warn("已在飞行中");
        }
    }
    
    @Override
    public void land() {
        if (flying) {
            flying = false;
            altitude = 0;
            logger.info("{} 航班{} 降落", airline, flightNumber);
        } else {
            logger.warn("已在地面");
        }
    }
    
    // 重写默认方法
    @Override
    public void honk() {
        logger.info("{} 航班{} 通过无线电通信", airline, flightNumber);
    }
    
    @Override
    public boolean isRunning() {
        return flying;
    }
    
    // 飞机特有方法
    public void setAltitude(int altitude) {
        this.altitude = altitude;
        logger.info("设置飞行高度: {} 米", altitude);
    }
    
    public int getAltitude() { return altitude; }
    public boolean isFlying() { return flying; }
}