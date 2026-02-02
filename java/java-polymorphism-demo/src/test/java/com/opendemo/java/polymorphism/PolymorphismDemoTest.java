package com.opendemo.java.polymorphism;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Java多态特性示例测试类
 * 测试各种多态形式的正确性和功能
 */
public class PolymorphismDemoTest {
    private static final Logger logger = LoggerFactory.getLogger(PolymorphismDemoTest.class);
    
    @BeforeEach
    void setUp() {
        logger.info("初始化多态测试环境");
    }
    
    @Test
    void testAbstractClassPolymorphism() {
        logger.info("测试抽象类多态");
        
        // 通过抽象类引用访问具体实现
        Shape shape1 = new Rectangle(3.0, 4.0, "红色", true);
        Shape shape2 = new Circle(2.0, "蓝色", false);
        Shape shape3 = new Triangle(3.0, 4.0, 5.0, "绿色", true);
        
        // 验证多态调用
        assertEquals(12.0, shape1.getArea(), 0.01);  // 矩形面积
        assertEquals(12.57, shape2.getArea(), 0.01); // 圆形面积
        assertEquals(6.0, shape3.getArea(), 0.01);   // 三角形面积
        
        // 验证方法调用不抛异常
        assertDoesNotThrow(() -> shape1.draw());
        assertDoesNotThrow(() -> shape2.draw());
        assertDoesNotThrow(() -> shape3.draw());
    }
    
    @Test
    void testInterfacePolymorphism() {
        logger.info("测试接口多态");
        
        // 通过接口引用访问实现类
        Drawable drawable1 = new Rectangle(2.0, 3.0, "黄色", true);
        Drawable drawable2 = new Circle(1.5, "紫色", false);
        Drawable drawable3 = new Triangle(2.0, 2.0, 2.0, "橙色", true);
        
        // 验证接口方法调用
        assertDoesNotThrow(() -> drawable1.draw());
        assertDoesNotThrow(() -> drawable2.draw());
        assertDoesNotThrow(() -> drawable3.draw());
        
        assertDoesNotThrow(() -> drawable1.erase());
        assertDoesNotThrow(() -> drawable2.erase());
        assertDoesNotThrow(() -> drawable3.erase());
        
        // 验证默认方法
        assertDoesNotThrow(() -> drawable1.display());
        assertDoesNotThrow(() -> drawable2.hide());
    }
    
    @Test
    void testMultipleInterfaceImplementation() {
        logger.info("测试多重接口实现");
        
        Triangle triangle = new Triangle(3.0, 4.0, 5.0, "彩虹色", true);
        
        // 验证可以通过不同接口引用访问
        Shape shapeRef = triangle;
        Drawable drawableRef = triangle;
        Resizable resizableRef = triangle;
        
        // 验证Shape接口
        assertEquals(6.0, shapeRef.getArea(), 0.01);
        assertDoesNotThrow(() -> shapeRef.draw());
        
        // 验证Drawable接口
        assertDoesNotThrow(() -> drawableRef.draw());
        assertDoesNotThrow(() -> drawableRef.erase());
        
        // 验证Resizable接口
        assertEquals(6.0, resizableRef.getSize(), 0.01);
        assertDoesNotThrow(() -> resizableRef.resize(2.0));
        assertDoesNotThrow(() -> resizableRef.scaleUp());
    }
    
    @Test
    void testRuntimePolymorphism() {
        logger.info("测试运行时多态");
        
        Shape[] shapes = {
            new Rectangle(2.0, 3.0),
            new Circle(2.0),
            new Triangle(3.0, 4.0, 5.0)
        };
        
        // 验证运行时确定调用哪个方法
        double[] expectedAreas = {6.0, 12.57, 6.0};
        
        for (int i = 0; i < shapes.length; i++) {
            assertEquals(expectedAreas[i], shapes[i].getArea(), 0.01);
            assertDoesNotThrow(() -> shapes[i].draw());
        }
    }
    
    @Test
    void testPolymorphicBehavior() {
        logger.info("测试多态行为");
        
        // 同一方法调用产生不同行为
        Shape[] shapes = {
            new Rectangle(1.0, 1.0),
            new Circle(1.0),
            new Triangle(1.0, 1.0, 1.0)
        };
        
        for (Shape shape : shapes) {
            // 每个shape的draw()方法实现都不同
            assertDoesNotThrow(() -> shape.draw());
            assertTrue(shape.getArea() > 0);
            assertTrue(shape.getPerimeter() > 0);
        }
    }
    
    @Test
    void testInstanceofOperator() {
        logger.info("测试instanceof操作符");
        
        Shape shape = new Rectangle(2.0, 3.0);
        
        // 验证类型检查
        assertTrue(shape instanceof Shape);
        assertTrue(shape instanceof Rectangle);
        assertFalse(shape instanceof Circle);
        assertFalse(shape instanceof Triangle);
        
        // 验证类型转换
        if (shape instanceof Rectangle) {
            Rectangle rect = (Rectangle) shape;
            assertEquals(2.0, rect.getWidth(), 0.01);
            assertEquals(3.0, rect.getHeight(), 0.01);
        }
    }
    
    @Test
    void testTypeCasting() {
        logger.info("测试类型转换");
        
        Shape shapeRef = new Circle(2.0, "蓝色", true);
        
        // 向上转型（自动）
        assertEquals("Circle", shapeRef.getClass().getSimpleName());
        
        // 向下转型（需要显式转换和检查）
        if (shapeRef instanceof Circle) {
            Circle circleRef = (Circle) shapeRef;
            assertEquals(2.0, circleRef.getRadius(), 0.01);
            assertEquals("蓝色", circleRef.getColor());
            assertTrue(circleRef.isFilled());
        }
        
        // 验证错误的类型转换
        Shape rectangleShape = new Rectangle(1.0, 1.0);
        if (!(rectangleShape instanceof Circle)) {
            assertThrows(ClassCastException.class, () -> {
                Circle wrongCast = (Circle) rectangleShape;
            });
        }
    }
    
    @Test
    void testTemplateMethodPattern() {
        logger.info("测试模板方法模式");
        
        Shape shape = new Rectangle(2.0, 3.0, "红色", true);
        
        // 验证模板方法执行
        assertDoesNotThrow(() -> shape.render());
        // render()方法会依次调用prepareCanvas(), draw(), fill(), finishRendering()
    }
    
    @Test
    void testDefaultInterfaceMethods() {
        logger.info("测试接口默认方法");
        
        Resizable resizable = Resizable.createResizable(10.0);
        
        assertEquals(10.0, resizable.getSize(), 0.01);
        assertDoesNotThrow(() -> resizable.scaleUp());
        assertDoesNotThrow(() -> resizable.scaleDown());
        assertTrue(resizable.isResizable());
    }
    
    @Test
    void testSpecificClassFeatures() {
        logger.info("测试具体类特有功能");
        
        Rectangle rectangle = new Rectangle(3.0, 4.0);
        Circle circle = new Circle(2.0);
        Triangle triangle = new Triangle(3.0, 4.0, 5.0);
        
        // 矩形特有方法
        assertTrue(rectangle.isSquare()); // 3.0 ≈ 4.0 (在误差范围内)
        assertDoesNotThrow(() -> rectangle.resize(2.0));
        
        // 圆形特有方法
        assertEquals(4.0, circle.getDiameter(), 0.01);
        assertTrue(circle.containsPoint(1.0, 1.0));  // 点(1,1)在半径为2的圆内
        assertFalse(circle.containsPoint(3.0, 3.0)); // 点(3,3)在圆外
        
        // 三角形特有方法
        assertTrue(triangle.isValid());
        assertTrue(triangle.isRightTriangle()); // 3-4-5是直角三角形
        assertDoesNotThrow(() -> triangle.rotate(90));
    }
    
    @Test
    void testPropertyValidation() {
        logger.info("测试属性验证");
        
        Rectangle rect = new Rectangle();
        Circle circle = new Circle();
        Triangle triangle = new Triangle();
        
        // 测试负数输入验证
        rect.setWidth(-5.0);
        assertEquals(1.0, rect.getWidth(), 0.01); // 应该保持原值
        
        circle.setRadius(-2.0);
        assertEquals(1.0, circle.getRadius(), 0.01); // 应该保持原值
        
        triangle.setSideA(-3.0);
        assertEquals(1.0, triangle.getSideA(), 0.01); // 应该保持原值
    }
    
    @Test
    void testToStringAndEquals() {
        logger.info("测试toString和equals方法");
        
        Rectangle rect1 = new Rectangle(2.0, 3.0, "红色", true);
        Rectangle rect2 = new Rectangle(2.0, 3.0, "红色", true);
        Rectangle rect3 = new Rectangle(3.0, 4.0, "蓝色", false);
        
        // 验证toString
        assertFalse(rect1.toString().isEmpty());
        assertTrue(rect1.toString().contains("Rectangle"));
        assertTrue(rect1.toString().contains("2.0"));
        assertTrue(rect1.toString().contains("3.0"));
        
        // 验证equals
        assertTrue(rect1.equals(rect2));
        assertFalse(rect1.equals(rect3));
        
        // 验证hashCode
        assertEquals(rect1.hashCode(), rect2.hashCode());
        assertNotEquals(rect1.hashCode(), rect3.hashCode());
    }
}