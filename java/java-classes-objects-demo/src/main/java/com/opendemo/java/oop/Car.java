package com.opendemo.java.oop;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Car类 - 演示类的关系和复杂对象
 * 展示对象间的关联关系和更复杂的业务逻辑
 */
public class Car {
    private static final Logger logger = LoggerFactory.getLogger(Car.class);
    
    // 成员变量
    private String brand;
    private String model;
    private int year;
    private String color;
    private double price;
    private boolean isRunning;
    private int speed;
    private Person owner; // 关联关系 - 汽车有一个所有者
    
    // 构造方法
    public Car(String brand, String model, int year) {
        this.brand = brand;
        this.model = model;
        this.year = year;
        this.color = "白色";
        this.price = 0.0;
        this.isRunning = false;
        this.speed = 0;
        this.owner = null;
        logger.info("创建了{} {}汽车", brand, model);
    }
    
    public Car(String brand, String model, int year, String color, double price) {
        this(brand, model, year); // 调用其他构造方法
        this.color = color;
        this.price = price;
        logger.info("创建了{} {} {}汽车，价格: ¥{}", color, brand, model, price);
    }
    
    // Getter和Setter方法
    public String getBrand() {
        return brand;
    }
    
    public String getModel() {
        return model;
    }
    
    public int getYear() {
        return year;
    }
    
    public String getColor() {
        return color;
    }
    
    public void setColor(String color) {
        this.color = color;
        logger.info("汽车颜色更改为: {}", color);
    }
    
    public double getPrice() {
        return price;
    }
    
    public void setPrice(double price) {
        if (price >= 0) {
            this.price = price;
            logger.info("汽车价格更新为: ¥{}", price);
        } else {
            logger.warn("价格不能为负数: {}", price);
        }
    }
    
    public Person getOwner() {
        return owner;
    }
    
    public void setOwner(Person owner) {
        this.owner = owner;
        if (owner != null) {
            logger.info("汽车所有者设置为: {}", owner.getName());
        } else {
            logger.info("汽车所有者已清除");
        }
    }
    
    // 业务方法
    public void start() {
        if (!isRunning) {
            isRunning = true;
            speed = 0;
            logger.info("{} {} 发动机启动了", brand, model);
        } else {
            logger.warn("汽车已经在运行中");
        }
    }
    
    public void stop() {
        if (isRunning) {
            isRunning = false;
            speed = 0;
            logger.info("{} {} 停止了", brand, model);
        } else {
            logger.warn("汽车已经停止了");
        }
    }
    
    public void accelerate(int increment) {
        if (isRunning) {
            if (increment > 0) {
                speed += increment;
                logger.info("加速到 {} km/h", speed);
            } else {
                logger.warn("加速度必须为正数: {}", increment);
            }
        } else {
            logger.warn("请先启动汽车");
        }
    }
    
    public void brake(int decrement) {
        if (speed > 0) {
            if (decrement > 0) {
                speed = Math.max(0, speed - decrement);
                logger.info("减速到 {} km/h", speed);
            } else {
                logger.warn("减速度必须为正数: {}", decrement);
            }
        } else {
            logger.warn("汽车已经停止，无需刹车");
        }
    }
    
    public void showInfo() {
        logger.info("=== 汽车信息 ===");
        logger.info("品牌: {}", brand);
        logger.info("型号: {}", model);
        logger.info("年份: {}", year);
        logger.info("颜色: {}", color);
        logger.info("价格: ¥{}", String.format("%.2f", price));
        logger.info("状态: {}", isRunning ? "运行中" : "已停止");
        logger.info("速度: {} km/h", speed);
        if (owner != null) {
            logger.info("所有者: {}", owner.getName());
        } else {
            logger.info("所有者: 无");
        }
    }
    
    // 静态工具方法
    public static String getCarInfo(Car car) {
        if (car == null) return "无效的汽车对象";
        return String.format("%d年 %s %s", car.year, car.brand, car.model);
    }
    
    public static boolean isNewCar(Car car) {
        if (car == null) return false;
        int currentYear = java.time.Year.now().getValue();
        return (currentYear - car.year) <= 2;
    }
    
    @Override
    public String toString() {
        return String.format("%d %s %s (%s)", year, brand, model, color);
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Car car = (Car) obj;
        return year == car.year && 
               Double.compare(car.price, price) == 0 &&
               brand.equals(car.brand) && 
               model.equals(car.model);
    }
    
    @Override
    public int hashCode() {
        return brand.hashCode() + model.hashCode() + year + (int)price;
    }
}