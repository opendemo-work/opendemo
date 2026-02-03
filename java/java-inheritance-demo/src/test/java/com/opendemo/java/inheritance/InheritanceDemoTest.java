package com.opendemo.java.inheritance;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java继承机制示例测试类
 * 测试继承、方法重写、多态等核心概念
 */
public class InheritanceDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(InheritanceDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化继承测试环境");
    }
    
    @Test
    void testAnimalConstructor() {
        logger.info("测试Animal构造方法");
        
        // 测试无参构造
        Animal animal1 = new Animal();
        assertEquals("未知动物", animal1.getName());
        assertEquals(0, animal1.getAge());
        assertEquals(0.0, animal1.getWeight(), 0.01);
        assertEquals("未知物种", animal1.getSpecies());
        
        // 测试四参构造
        Animal animal2 = new Animal("测试动物", 5, 10.5, "测试物种");
        assertEquals("测试动物", animal2.getName());
        assertEquals(5, animal2.getAge());
        assertEquals(10.5, animal2.getWeight(), 0.01);
        assertEquals("测试物种", animal2.getSpecies());
    }
    
    @Test
    void testMammalInheritance() {
        logger.info("测试Mammal继承");
        
        Mammal mammal = new Mammal("哺乳动物测试", 3, 15.2, true, 90, "棕色");
        
        // 验证继承的属性
        assertEquals("哺乳动物测试", mammal.getName());
        assertEquals(3, mammal.getAge());
        assertEquals(15.2, mammal.getWeight(), 0.01);
        assertEquals("哺乳动物", mammal.getSpecies());
        
        // 验证Mammal特有的属性
        assertTrue(mammal.hasFur());
        assertEquals(90, mammal.getGestationPeriod());
        assertEquals("棕色", mammal.getFurColor());
    }
    
    @Test
    void testDogInheritance() {
        logger.info("测试Dog多层继承");
        
        Dog dog = new Dog("狗狗测试", 2, 8.0, "金毛", true, "飞盘");
        
        // 验证继承链中的所有属性
        assertEquals("狗狗测试", dog.getName());
        assertEquals(2, dog.getAge());
        assertEquals(8.0, dog.getWeight(), 0.01);
        assertEquals("犬类", dog.getSpecies());
        assertTrue(dog.hasFur());
        assertEquals(63, dog.getGestationPeriod()); // Mammal默认值
        assertEquals("多种颜色", dog.getFurColor()); // Mammal默认值
        
        // 验证Dog特有的属性
        assertEquals("金毛", dog.getBreed());
        assertTrue(dog.isTrained());
        assertEquals("飞盘", dog.getFavoriteToy());
    }
    
    @Test
    void testBirdInheritance() {
        logger.info("测试Bird继承");
        
        Bird bird = new Bird("鸟儿测试", 1, 0.3, true, 25.0, "蓝色", true);
        
        // 验证继承的属性
        assertEquals("鸟儿测试", bird.getName());
        assertEquals(1, bird.getAge());
        assertEquals(0.3, bird.getWeight(), 0.01);
        assertEquals("鸟类", bird.getSpecies());
        
        // 验证Bird特有的属性
        assertTrue(bird.canFly());
        assertEquals(25.0, bird.getWingspan(), 0.01);
        assertEquals("蓝色", bird.getFeatherColor());
        assertTrue(bird.isMigrates());
    }
    
    @Test
    void testMethodOverriding() {
        logger.info("测试方法重写");
        
        Animal animal = new Animal("普通动物", 2, 5.0, "普通");
        Mammal mammal = new Mammal("哺乳动物", 3, 10.0, true, 60, "灰色");
        Dog dog = new Dog("狗狗", 1, 6.0, "边牧", false, "球");
        Bird bird = new Bird("鸟儿", 2, 0.3, true, 20.0, "绿色", false);
        
        // 验证方法重写 - 通过行为间接测试
        // 这里主要是验证对象创建和方法调用不抛异常
        assertDoesNotThrow(() -> animal.makeSound());
        assertDoesNotThrow(() -> mammal.makeSound());
        assertDoesNotThrow(() -> dog.makeSound());
        assertDoesNotThrow(() -> bird.makeSound());
        
        assertDoesNotThrow(() -> animal.move());
        assertDoesNotThrow(() -> mammal.move());
        assertDoesNotThrow(() -> dog.move());
        assertDoesNotThrow(() -> bird.move());
    }
    
    @Test
    void testPolymorphism() {
        logger.info("测试多态性");
        
        // 多态引用测试
        Animal[] animals = {
            new Animal("动物1", 1, 2.0, "物种1"),
            new Mammal("哺乳动物1", 2, 5.0, true, 30, "黑色"),
            new Dog("狗1", 1, 3.0, "泰迪", false, "球"),
            new Bird("鸟1", 1, 0.1, true, 15.0, "红色", false)
        };
        
        // 验证多态调用
        for (Animal animal : animals) {
            assertNotNull(animal);
            assertDoesNotThrow(() -> animal.makeSound());
            assertDoesNotThrow(() -> animal.move());
        }
    }
    
    @Test
    void testTypeCasting() {
        logger.info("测试类型转换");
        
        // 向上转型
        Animal animalRef = new Dog("测试犬", 2, 8.0, "金毛", true, "玩具");
        assertEquals("Dog", animalRef.getClass().getSimpleName());
        assertDoesNotThrow(() -> animalRef.makeSound()); // 应该调用Dog的方法
        
        // 向下转型
        if (animalRef instanceof Dog) {
            Dog dogRef = (Dog) animalRef;
            assertEquals("金毛", dogRef.getBreed());
            assertDoesNotThrow(() -> dogRef.fetch("飞盘")); // Dog特有方法
        }
        
        // 验证错误的类型转换会被拒绝
        Animal genericAnimal = new Animal("普通动物", 1, 2.0, "普通");
        if (!(genericAnimal instanceof Dog)) {
            assertThrows(ClassCastException.class, () -> {
                Dog wrongCast = (Dog) genericAnimal;
            });
        }
    }
    
    @Test
    void testStaticMembers() {
        logger.info("测试静态成员");
        
        int initialCount = Animal.getAnimalCount();
        
        // 创建多个不同类型对象
        Animal animal = new Animal("动物", 1, 2.0, "物种");
        Mammal mammal = new Mammal("哺乳动物", 2, 5.0, true, 30, "黑色");
        Dog dog = new Dog("狗", 1, 3.0, "泰迪", false, "球");
        Bird bird = new Bird("鸟", 1, 0.1, true, 15.0, "红色", false);
        
        // 验证静态计数器
        assertEquals(initialCount + 4, Animal.getAnimalCount());
        
        // 测试Bird静态方法
        Bird eagle = new Bird("老鹰", 5, 4.0, true, 200.0, "褐色", true);
        double speed = Bird.calculateFlightSpeed(eagle);
        assertTrue(speed > 0);
        assertTrue(Bird.isLargeBird(eagle));
        
        Bird smallBird = new Bird("小鸟", 1, 0.05, true, 10.0, "黄色", false);
        assertFalse(Bird.isLargeBird(smallBird));
    }
    
    @Test
    void testPropertyValidation() {
        logger.info("测试属性验证");
        
        Animal animal = new Animal();
        Mammal mammal = new Mammal();
        Bird bird = new Bird();
        
        // 测试负数年龄设置
        animal.setAge(-5);
        assertEquals(0, animal.getAge()); // 应该保持原值
        
        // 测试负数体重设置
        animal.setWeight(-10.0);
        assertEquals(0.0, animal.getWeight(), 0.01); // 应该保持原值
        
        // 测试负数翼展设置
        bird.setWingspan(-20.0);
        assertEquals(0.0, bird.getWingspan(), 0.01); // 应该保持原值
        
        // 测试负数妊娠期设置
        mammal.setGestationPeriod(-30);
        assertEquals(0, mammal.getGestationPeriod()); // 应该保持原值
    }
    
    @Test
    void testToStringMethods() {
        logger.info("测试toString方法");
        
        Animal animal = new Animal("测试动物", 2, 5.0, "测试物种");
        Mammal mammal = new Mammal("测试哺乳动物", 3, 10.0, true, 60, "棕色");
        Dog dog = new Dog("测试狗", 1, 6.0, "金毛", true, "飞盘");
        Bird bird = new Bird("测试鸟", 2, 0.3, true, 25.0, "蓝色", true);
        
        // 验证toString不为空且包含关键信息
        assertFalse(animal.toString().isEmpty());
        assertTrue(animal.toString().contains("测试动物"));
        
        assertFalse(mammal.toString().isEmpty());
        assertTrue(mammal.toString().contains("测试哺乳动物"));
        
        assertFalse(dog.toString().isEmpty());
        assertTrue(dog.toString().contains("测试狗"));
        assertTrue(dog.toString().contains("金毛"));
        
        assertFalse(bird.toString().isEmpty());
        assertTrue(bird.toString().contains("测试鸟"));
        assertTrue(bird.toString().contains("蓝色"));
    }
    
    @Test
    void testEqualsAndHashCode() {
        logger.info("测试equals和hashCode方法");
        
        // Animal对象比较
        Animal animal1 = new Animal("测试", 2, 5.0, "物种");
        Animal animal2 = new Animal("测试", 2, 5.0, "物种");
        Animal animal3 = new Animal("不同", 3, 6.0, "不同物种");
        
        assertTrue(animal1.equals(animal2));
        assertFalse(animal1.equals(animal3));
        
        assertEquals(animal1.hashCode(), animal2.hashCode());
        assertNotEquals(animal1.hashCode(), animal3.hashCode());
        
        // Dog对象比较
        Dog dog1 = new Dog("狗狗", 1, 6.0, "金毛", true, "飞盘");
        Dog dog2 = new Dog("狗狗", 1, 6.0, "金毛", true, "飞盘");
        Dog dog3 = new Dog("不同", 2, 8.0, "边牧", false, "球");
        
        assertTrue(dog1.equals(dog2));
        assertFalse(dog1.equals(dog3));
    }
}