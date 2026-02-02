package com.opendemo.java.polymorphism;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.ArrayList;
import java.util.List;

/**
 * Java多态特性演示程序
 * 展示运行时多态、接口多态、抽象类多态等各种多态形式
 */
public class PolymorphismDemo {
    private static final Logger logger = LoggerFactory.getLogger(PolymorphismDemo.class);
    
    public static void main(String[] args) {
        logger.info("=== Java多态特性完整演示 ===");
        
        PolymorphismDemo demo = new PolymorphismDemo();
        
        demo.demonstrateRuntimePolymorphism();
        demo.demonstrateInterfacePolymorphism();
        demo.demonstrateAbstractClassPolymorphism();
        demo.demonstrateMultiplePolymorphism();
        demo.demonstratePolymorphicCollections();
        demo.demonstrateDynamicBinding();
        
        logger.info("=== 演示完成 ===");
    }
    
    /**
     * 演示运行时多态（动态绑定）
     */
    public void demonstrateRuntimePolymorphism() {
        logger.info("--- 运行时多态演示 ---");
        
        // 父类引用指向子类对象
        Shape[] shapes = {
            new Rectangle(5.0, 3.0, "红色", true),
            new Circle(4.0, "蓝色", false),
            new Triangle(3.0, 4.0, 5.0, "绿色", true)
        };
        
        logger.info("通过父类引用调用重写方法（运行时决定具体实现）:");
        for (Shape shape : shapes) {
            logger.info("图形类型: {}", shape.getClass().getSimpleName());
            shape.displayInfo();  // 调用重写的方法
            shape.draw();         // 调用抽象方法的具体实现
            logger.info("");
        }
    }
    
    /**
     * 演示接口多态
     */
    public void demonstrateInterfacePolymorphism() {
        logger.info("--- 接口多态演示 ---");
        
        // 接口引用指向实现类对象
        Drawable[] drawableObjects = {
            new Rectangle(3.0, 2.0, "黄色", true),
            new Circle(2.5, "紫色", false),
            new Triangle(2.0, 2.0, 2.0, "橙色", true)
        };
        
        logger.info("通过接口引用调用方法:");
        for (Drawable drawable : drawableObjects) {
            logger.info("对象类型: {}", drawable.getClass().getSimpleName());
            drawable.draw();   // 调用接口方法
            drawable.display(); // 调用默认方法
            logger.info("");
        }
        
        // 调用接口静态方法
        logger.info("调用接口静态方法:");
        Drawable.showInfo();
        logger.info("");
    }
    
    /**
     * 演示抽象类多态
     */
    public void demonstrateAbstractClassPolymorphism() {
        logger.info("--- 抽象类多态演示 ---");
        
        // 抽象类引用指向具体子类
        Shape shape1 = new Rectangle(4.0, 6.0, "青色", true);
        Shape shape2 = new Circle(3.0, "粉色", false);
        Shape shape3 = new Triangle(5.0, 5.0, 5.0, "棕色", true);
        
        logger.info("抽象类多态特性:");
        Shape[] shapes = {shape1, shape2, shape3};
        
        for (Shape shape : shapes) {
            logger.info("形状: {}", shape.toString());
            logger.info("面积: {}", String.format("%.2f", shape.getArea()));
            logger.info("周长: {}", String.format("%.2f", shape.getPerimeter()));
            
            // 调用模板方法
            shape.render();
            logger.info("");
        }
    }
    
    /**
     * 演示多重多态（同时实现多个接口）
     */
    public void demonstrateMultiplePolymorphism() {
        logger.info("--- 多重多态演示 ---");
        
        Triangle triangle = new Triangle(3.0, 4.0, 5.0, "彩虹色", true);
        
        // 通过不同引用类型访问
        logger.info("通过不同引用类型访问同一对象:");
        
        // 1. 通过具体类引用
        logger.info("1. 通过Triangle引用:");
        triangle.draw();
        triangle.resize(2.0);
        triangle.rotate(45);
        
        // 2. 通过Shape抽象类引用
        logger.info("\n2. 通过Shape引用:");
        Shape shapeRef = triangle;
        shapeRef.draw();
        shapeRef.displayInfo();
        
        // 3. 通过Drawable接口引用
        logger.info("\n3. 通过Drawable引用:");
        Drawable drawableRef = triangle;
        drawableRef.draw();
        drawableRef.erase();
        
        // 4. 通过Resizable接口引用
        logger.info("\n4. 通过Resizable引用:");
        Resizable resizableRef = triangle;
        resizableRef.scaleUp();
        resizableRef.scaleDown();
        
        logger.info("");
    }
    
    /**
     * 演示多态集合
     */
    public void demonstratePolymorphicCollections() {
        logger.info("--- 多态集合演示 ---");
        
        // 创建多态集合
        List<Shape> shapeList = new ArrayList<>();
        shapeList.add(new Rectangle(2.0, 3.0, "红色", false));
        shapeList.add(new Circle(2.5, "蓝色", true));
        shapeList.add(new Triangle(3.0, 4.0, 5.0, "绿色", true));
        
        logger.info("处理多态集合中的对象:");
        double totalArea = 0;
        double totalPerimeter = 0;
        
        for (Shape shape : shapeList) {
            logger.info("处理{}:", shape.getClass().getSimpleName());
            shape.draw();
            shape.displayInfo();
            
            totalArea += shape.getArea();
            totalPerimeter += shape.getPerimeter();
            logger.info("");
        }
        
        logger.info("总计:");
        logger.info("总面积: {}", String.format("%.2f", totalArea));
        logger.info("总周长: {}", String.format("%.2f", totalPerimeter));
        logger.info("");
    }
    
    /**
     * 演示动态绑定机制
     */
    public void demonstrateDynamicBinding() {
        logger.info("--- 动态绑定机制演示 ---");
        
        // 编译时类型 vs 运行时类型
        Shape shapeRef;
        
        logger.info("动态绑定演示 - 运行时决定方法调用:");
        
        // 第一次赋值
        shapeRef = new Rectangle(3.0, 4.0, "金色", true);
        logger.info("引用类型: Shape, 实际类型: {}", shapeRef.getClass().getSimpleName());
        shapeRef.draw();  // 调用Rectangle.draw()
        shapeRef.render(); // 调用Shape模板方法，但draw()是动态绑定的
        
        logger.info("");
        
        // 第二次赋值
        shapeRef = new Circle(2.0, "银色", false);
        logger.info("引用类型: Shape, 实际类型: {}", shapeRef.getClass().getSimpleName());
        shapeRef.draw();  // 调用Circle.draw()
        shapeRef.render(); // 同样是动态绑定
        
        logger.info("");
        
        // 第三次赋值
        shapeRef = new Triangle(2.0, 2.0, 2.0, "铜色", true);
        logger.info("引用类型: Shape, 实际类型: {}", shapeRef.getClass().getSimpleName());
        shapeRef.draw();  // 调用Triangle.draw()
        shapeRef.render(); // 动态绑定
        
        logger.info("");
        
        // 演示instanceof操作符
        logger.info("类型检查演示:");
        Shape[] shapes = {
            new Rectangle(1.0, 1.0),
            new Circle(1.0),
            new Triangle(1.0, 1.0, 1.0)
        };
        
        for (Shape shape : shapes) {
            logger.info("对象类型: {}", shape.getClass().getSimpleName());
            
            if (shape instanceof Rectangle) {
                Rectangle rect = (Rectangle) shape;
                logger.info("  这是一个矩形，是否为正方形: {}", rect.isSquare());
            }
            
            if (shape instanceof Circle) {
                Circle circle = (Circle) shape;
                logger.info("  这是一个圆形，直径: {}", String.format("%.2f", circle.getDiameter()));
            }
            
            if (shape instanceof Triangle) {
                Triangle triangle = (Triangle) shape;
                logger.info("  这是一个三角形");
                logger.info("    是否有效: {}", triangle.isValid());
                logger.info("    是否等边: {}", triangle.isEquilateral());
                logger.info("    是否等腰: {}", triangle.isIsosceles());
                logger.info("    是否直角: {}", triangle.isRightTriangle());
            }
            
            logger.info("");
        }
    }
}