package com.opendemo.java.oop;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java类与对象示例测试类
 * 测试Person类和Car类的各种功能
 */
public class ClassesObjectsDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(ClassesObjectsDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化测试环境");
    }
    
    @Test
    void testPersonConstructor() {
        logger.info("测试Person构造方法");
        
        // 测试无参构造
        Person person1 = new Person();
        assertEquals("未知", person1.getName());
        assertEquals(0, person1.getAge());
        assertEquals("unknown@example.com", person1.getEmail());
        
        // 测试两参构造
        Person person2 = new Person("测试用户", 25);
        assertEquals("测试用户", person2.getName());
        assertEquals(25, person2.getAge());
        assertEquals("测试用户".toLowerCase().replace(" ", ".") + "@example.com", person2.getEmail());
        
        // 测试三参构造
        Person person3 = new Person("完整用户", 30, "full@test.com");
        assertEquals("完整用户", person3.getName());
        assertEquals(30, person3.getAge());
        assertEquals("full@test.com", person3.getEmail());
    }
    
    @Test
    void testPersonGettersAndSetters() {
        logger.info("测试Person的Getter和Setter方法");
        
        Person person = new Person();
        
        // 测试setName
        person.setName("新姓名");
        assertEquals("新姓名", person.getName());
        
        person.setName("");  // 无效姓名
        assertEquals("新姓名", person.getName()); // 应该保持原值
        
        person.setName(null); // null值
        assertEquals("新姓名", person.getName()); // 应该保持原值
        
        // 测试setAge
        person.setAge(25);
        assertEquals(25, person.getAge());
        
        person.setAge(-1);   // 无效年龄
        assertEquals(25, person.getAge()); // 应该保持原值
        
        person.setAge(200);  // 超出范围
        assertEquals(25, person.getAge()); // 应该保持原值
        
        // 测试setEmail
        person.setEmail("valid@email.com");
        assertEquals("valid@email.com", person.getEmail());
        
        person.setEmail("invalid-email"); // 无效邮箱
        assertEquals("valid@email.com", person.getEmail()); // 应该保持原值
        
        person.setEmail(null); // null值
        assertEquals("valid@email.com", person.getEmail()); // 应该保持原值
    }
    
    @Test
    void testPersonBusinessMethods() {
        logger.info("测试Person业务方法");
        
        Person person = new Person("测试用户", 17);
        
        // 测试introduce方法
        person.introduce(); // 只是输出日志，无需断言
        
        // 测试isAdult方法
        assertFalse(person.isAdult()); // 17岁不是成年人
        
        person.setAge(18);
        assertTrue(person.isAdult()); // 18岁是成年人
        
        // 测试celebrateBirthday方法
        int originalAge = person.getAge();
        person.celebrateBirthday();
        assertEquals(originalAge + 1, person.getAge());
    }
    
    @Test
    void testCarConstructor() {
        logger.info("测试Car构造方法");
        
        // 测试两参构造
        Car car1 = new Car("丰田", "卡罗拉", 2020);
        assertEquals("丰田", car1.getBrand());
        assertEquals("卡罗拉", car1.getModel());
        assertEquals(2020, car1.getYear());
        assertEquals("白色", car1.getColor());
        assertEquals(0.0, car1.getPrice(), 0.01);
        
        // 测试五参构造
        Car car2 = new Car("本田", "雅阁", 2022, "黑色", 250000);
        assertEquals("本田", car2.getBrand());
        assertEquals("雅阁", car2.getModel());
        assertEquals(2022, car2.getYear());
        assertEquals("黑色", car2.getColor());
        assertEquals(250000, car2.getPrice(), 0.01);
    }
    
    @Test
    void testCarGettersAndSetters() {
        logger.info("测试Car的Getter和Setter方法");
        
        Car car = new Car("测试", "车型", 2020);
        
        // 测试setColor
        car.setColor("红色");
        assertEquals("红色", car.getColor());
        
        // 测试setPrice
        car.setPrice(300000);
        assertEquals(300000, car.getPrice(), 0.01);
        
        car.setPrice(-50000); // 无效价格
        assertEquals(300000, car.getPrice(), 0.01); // 应该保持原值
    }
    
    @Test
    void testCarBusinessMethods() {
        logger.info("测试Car业务方法");
        
        Car car = new Car("测试", "车型", 2020);
        
        // 测试初始状态
        assertFalse(car.isRunning());
        assertEquals(0, car.getSpeed());
        
        // 测试启动
        car.start();
        assertTrue(car.isRunning());
        assertEquals(0, car.getSpeed());
        
        // 测试重复启动
        car.start(); // 应该有警告日志，但不影响状态
        assertTrue(car.isRunning());
        
        // 测试加速
        car.accelerate(50);
        assertEquals(50, car.getSpeed());
        
        car.accelerate(-10); // 负数加速度
        assertEquals(50, car.getSpeed()); // 应该保持不变
        
        // 测试刹车
        car.brake(20);
        assertEquals(30, car.getSpeed());
        
        car.brake(-5); // 负数减速度
        assertEquals(30, car.getSpeed()); // 应该保持不变
        
        // 测试停止
        car.stop();
        assertFalse(car.isRunning());
        assertEquals(0, car.getSpeed());
        
        // 测试未启动时的操作
        car.accelerate(30); // 应该有警告日志
        assertEquals(0, car.getSpeed()); // 应该保持0
    }
    
    @Test
    void testObjectRelationships() {
        logger.info("测试对象间关系");
        
        Person owner = new Person("车主", 30);
        Car car = new Car("奔驰", "C级", 2023);
        
        // 测试设置所有者
        car.setOwner(owner);
        assertEquals(owner, car.getOwner());
        assertEquals("车主", car.getOwner().getName());
        
        // 测试清除所有者
        car.setOwner(null);
        assertNull(car.getOwner());
    }
    
    @Test
    void testStaticMembers() {
        logger.info("测试静态成员");
        
        int initialCount = Person.getPersonCount();
        
        // 创建几个Person对象
        Person p1 = new Person("用户1", 20);
        Person p2 = new Person("用户2", 25);
        
        assertEquals(initialCount + 2, Person.getPersonCount());
        
        // 测试静态方法
        Car car = new Car("测试", "车型", 2022);
        assertEquals("2022年 测试 车型", Car.getCarInfo(car));
        assertEquals("无效的汽车对象", Car.getCarInfo(null));
        
        // 测试新车判断
        Car newCar = new Car("新", "车型", java.time.Year.now().getValue());
        assertTrue(Car.isNewCar(newCar));
        
        Car oldCar = new Car("旧", "车型", 2020);
        assertFalse(Car.isNewCar(oldCar));
    }
    
    @Test
    void testToStringMethods() {
        logger.info("测试toString方法");
        
        Person person = new Person("测试用户", 25, "test@email.com");
        String personStr = person.toString();
        assertTrue(personStr.contains("测试用户"));
        assertTrue(personStr.contains("25"));
        assertTrue(personStr.contains("test@email.com"));
        
        Car car = new Car("丰田", "凯美瑞", 2023, "银色", 250000);
        String carStr = car.toString();
        assertTrue(carStr.contains("丰田"));
        assertTrue(carStr.contains("凯美瑞"));
        assertTrue(carStr.contains("2023"));
        assertTrue(carStr.contains("银色"));
    }
    
    @Test
    void testEqualsAndHashCode() {
        logger.info("测试equals和hashCode方法");
        
        // Person对象比较
        Person person1 = new Person("测试", 25, "test@email.com");
        Person person2 = new Person("测试", 25, "test@email.com");
        Person person3 = new Person("不同", 30, "different@email.com");
        
        assertTrue(person1.equals(person2));
        assertFalse(person1.equals(person3));
        assertFalse(person1.equals(null));
        assertFalse(person1.equals("not a person"));
        
        assertEquals(person1.hashCode(), person2.hashCode());
        assertNotEquals(person1.hashCode(), person3.hashCode());
        
        // Car对象比较
        Car car1 = new Car("丰田", "凯美瑞", 2023, "白色", 250000);
        Car car2 = new Car("丰田", "凯美瑞", 2023, "白色", 250000);
        Car car3 = new Car("本田", "雅阁", 2022, "黑色", 200000);
        
        assertTrue(car1.equals(car2));
        assertFalse(car1.equals(car3));
        
        assertEquals(car1.hashCode(), car2.hashCode());
        assertNotEquals(car1.hashCode(), car3.hashCode());
    }
}