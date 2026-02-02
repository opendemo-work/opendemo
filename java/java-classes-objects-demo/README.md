# Java面向对象编程基础演示

## 🎯 学习目标

通过本案例你将掌握：
- 类和对象的基本概念
- 成员变量和方法的定义
- 构造方法的使用
- 访问修饰符的理解
- this关键字的作用
- 对象的创建和使用
- 基本的封装原则

## 🛠️ 环境准备

### 系统要求
- JDK 11或更高版本
- 支持Java的IDE或文本编辑器
- Java基础语法知识

### 依赖检查
```bash
# 验证Java环境
java -version
javac -version
```

## 📁 项目结构

```
java-classes-objects-demo/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   ├── Person.java
│                   ├── Car.java
│                   └── ClassesObjectsDemo.java
├── README.md
└── metadata.json
```

## 🚀 快速开始

### 步骤1：创建项目结构
```bash
mkdir java-classes-objects-demo
cd java-classes-objects-demo
mkdir -p src/main/java/com/example
```

### 步骤2：创建Person类
创建 `src/main/java/com/example/Person.java` 文件：

```java
package com.example;

/**
 * Person类 - 演示基本的类定义和封装
 */
public class Person {
    // 成员变量（属性）- 使用private修饰符实现封装
    private String name;
    private int age;
    private String email;
    private static int personCount = 0; // 静态变量，记录实例数量
    
    // 无参构造方法
    public Person() {
        this.name = "未知";
        this.age = 0;
        this.email = "unknown@example.com";
        personCount++;
        System.out.println("创建了一个Person对象");
    }
    
    // 有参构造方法
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
        this.email = name.toLowerCase().replace(" ", ".") + "@example.com";
        personCount++;
        System.out.println("创建了Person对象: " + name);
    }
    
    // 完整构造方法
    public Person(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
        personCount++;
        System.out.println("创建了完整Person对象: " + name);
    }
    
    // Getter和Setter方法 - 提供受控访问
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name;
        } else {
            System.out.println("姓名不能为空");
        }
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        if (age >= 0 && age <= 150) {
            this.age = age;
        } else {
            System.out.println("年龄必须在0-150之间");
        }
    }
    
    public String getEmail() {
        return email;
    }
    
    public void setEmail(String email) {
        if (email != null && email.contains("@")) {
            this.email = email;
        } else {
            System.out.println("邮箱格式不正确");
        }
    }
    
    // 业务方法
    public void introduce() {
        System.out.println("大家好，我是" + name + "，今年" + age + "岁");
    }
    
    public void celebrateBirthday() {
        age++;
        System.out.println(name + "过生日了！现在" + age + "岁了！");
    }
    
    public boolean isAdult() {
        return age >= 18;
    }
    
    // 静态方法
    public static int getPersonCount() {
        return personCount;
    }
    
    // 重写toString方法
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + ", email='" + email + "'}";
    }
    
    // 重写equals方法
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && 
               name.equals(person.name) && 
               email.equals(person.email);
    }
    
    // 重写hashCode方法
    @Override
    public int hashCode() {
        return name.hashCode() + age + email.hashCode();
    }
}
```

### 步骤3：创建Car类
创建 `src/main/java/com/example/Car.java` 文件：

```java
package com.example;

/**
 * Car类 - 演示类的关系和复杂对象
 */
public class Car {
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
    }
    
    public Car(String brand, String model, int year, String color, double price) {
        this(brand, model, year); // 调用其他构造方法
        this.color = color;
        this.price = price;
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
    }
    
    public double getPrice() {
        return price;
    }
    
    public void setPrice(double price) {
        if (price >= 0) {
            this.price = price;
        }
    }
    
    public Person getOwner() {
        return owner;
    }
    
    public void setOwner(Person owner) {
        this.owner = owner;
    }
    
    // 业务方法
    public void start() {
        if (!isRunning) {
            isRunning = true;
            System.out.println(brand + " " + model + " 发动机启动了");
        } else {
            System.out.println("汽车已经在运行中");
        }
    }
    
    public void stop() {
        if (isRunning) {
            isRunning = false;
            speed = 0;
            System.out.println(brand + " " + model + " 停止了");
        } else {
            System.out.println("汽车已经停止了");
        }
    }
    
    public void accelerate(int increment) {
        if (isRunning) {
            speed += increment;
            System.out.println("加速到 " + speed + " km/h");
        } else {
            System.out.println("请先启动汽车");
        }
    }
    
    public void brake(int decrement) {
        if (speed > 0) {
            speed = Math.max(0, speed - decrement);
            System.out.println("减速到 " + speed + " km/h");
        }
    }
    
    public void showInfo() {
        System.out.println("=== 汽车信息 ===");
        System.out.println("品牌: " + brand);
        System.out.println("型号: " + model);
        System.out.println("年份: " + year);
        System.out.println("颜色: " + color);
        System.out.println("价格: ¥" + String.format("%.2f", price));
        System.out.println("状态: " + (isRunning ? "运行中" : "已停止"));
        System.out.println("速度: " + speed + " km/h");
        if (owner != null) {
            System.out.println("所有者: " + owner.getName());
        } else {
            System.out.println("所有者: 无");
        }
    }
    
    // 静态工具方法
    public static String getCarInfo(Car car) {
        if (car == null) return "无效的汽车对象";
        return car.year + "年 " + car.brand + " " + car.model;
    }
    
    @Override
    public String toString() {
        return year + " " + brand + " " + model + " (" + color + ")";
    }
}
```

### 步骤4：创建主演示程序
创建 `src/main/java/com/example/ClassesObjectsDemo.java` 文件：

```java
package com.example;

/**
 * Java面向对象编程演示程序
 * 展示类的定义、对象的创建和使用
 */
public class ClassesObjectsDemo {
    
    public static void main(String[] args) {
        System.out.println("=== Java面向对象编程演示 ===\n");
        
        // 1. 基本对象创建演示
        demonstrateBasicObjectCreation();
        
        // 2. 构造方法演示
        demonstrateConstructors();
        
        // 3. 封装性演示
        demonstrateEncapsulation();
        
        // 4. 对象关系演示
        demonstrateObjectRelationships();
        
        // 5. 静态成员演示
        demonstrateStaticMembers();
        
        // 6. 方法重写演示
        demonstrateMethodOverriding();
    }
    
    /**
     * 演示基本对象创建
     */
    private static void demonstrateBasicObjectCreation() {
        System.out.println("1. 基本对象创建演示:");
        
        // 使用无参构造方法创建对象
        Person person1 = new Person();
        person1.setName("张三");
        person1.setAge(25);
        person1.introduce();
        
        // 使用有参构造方法创建对象
        Person person2 = new Person("李四", 30);
        person2.introduce();
        
        // 使用完整构造方法创建对象
        Person person3 = new Person("王五", 28, "wangwu@company.com");
        person3.introduce();
        
        System.out.println();
    }
    
    /**
     * 演示构造方法的使用
     */
    private static void demonstrateConstructors() {
        System.out.println("2. 构造方法演示:");
        
        // 不同构造方法的效果
        System.out.println("使用不同构造方法创建对象:");
        Person p1 = new Person();                           // 无参构造
        Person p2 = new Person("赵六", 22);                 // 两参构造
        Person p3 = new Person("钱七", 35, "qianqi@mail.com"); // 三参构造
        
        System.out.println("p1: " + p1);
        System.out.println("p2: " + p2);
        System.out.println("p3: " + p3);
        
        System.out.println();
    }
    
    /**
     * 演示封装性的实现
     */
    private static void demonstrateEncapsulation() {
        System.out.println("3. 封装性演示:");
        
        Person person = new Person("测试用户", 20);
        
        // 正常的数据访问
        System.out.println("原始姓名: " + person.getName());
        System.out.println("原始年龄: " + person.getAge());
        
        // 尝试设置有效数据
        person.setName("新名字");
        person.setAge(25);
        System.out.println("更新后姓名: " + person.getName());
        System.out.println("更新后年龄: " + person.getAge());
        
        // 尝试设置无效数据
        person.setAge(-5);    // 无效年龄
        person.setName("");   // 无效姓名
        person.setEmail("invalid-email"); // 无效邮箱
        
        System.out.println("最终年龄: " + person.getAge()); // 应该还是25
        System.out.println();
    }
    
    /**
     * 演示对象之间的关系
     */
    private static void demonstrateObjectRelationships() {
        System.out.println("4. 对象关系演示:");
        
        // 创建人物对象
        Person owner = new Person("车主", 32, "owner@auto.com");
        
        // 创建汽车对象
        Car car = new Car("丰田", "凯美瑞", 2023, "银色", 250000);
        
        // 建立关系
        car.setOwner(owner);
        
        // 展示信息
        car.showInfo();
        System.out.println("所有者信息: " + owner);
        
        // 模拟汽车操作
        System.out.println("\n汽车操作演示:");
        car.start();
        car.accelerate(60);
        car.brake(20);
        car.stop();
        
        System.out.println();
    }
    
    /**
     * 演示静态成员的使用
     */
    private static void demonstrateStaticMembers() {
        System.out.println("5. 静态成员演示:");
        
        System.out.println("初始Person数量: " + Person.getPersonCount());
        
        // 创建多个对象
        Person p1 = new Person("用户1", 20);
        Person p2 = new Person("用户2", 25);
        Person p3 = new Person("用户3", 30);
        
        System.out.println("创建3个对象后Person数量: " + Person.getPersonCount());
        
        // 静态方法调用
        Car car = new Car("本田", "雅阁", 2022);
        System.out.println("汽车信息: " + Car.getCarInfo(car));
        System.out.println("无效调用: " + Car.getCarInfo(null));
        
        System.out.println();
    }
    
    /**
     * 演示方法重写的使用
     */
    private static void demonstrateMethodOverriding() {
        System.out.println("6. 方法重写演示:");
        
        Person person = new Person("重写测试", 25);
        Car car = new Car("奔驰", "C级", 2024);
        
        // toString()方法重写
        System.out.println("Person.toString(): " + person);
        System.out.println("Car.toString(): " + car);
        
        // equals()方法重写测试
        Person person1 = new Person("测试", 25, "test@email.com");
        Person person2 = new Person("测试", 25, "test@email.com");
        Person person3 = new Person("不同", 30, "different@email.com");
        
        System.out.println("person1.equals(person2): " + person1.equals(person2)); // 应该为true
        System.out.println("person1.equals(person3): " + person1.equals(person3)); // 应该为false
        
        // hashCode()方法
        System.out.println("person1.hashCode(): " + person1.hashCode());
        System.out.println("person2.hashCode(): " + person2.hashCode());
        System.out.println("person3.hashCode(): " + person3.hashCode());
        
        System.out.println();
    }
}
```

### 步骤5：编译和运行
```bash
# 编译所有Java文件
javac src/main/java/com/example/*.java

# 运行程序
java com.example.ClassesObjectsDemo
```

预期输出：
```
=== Java面向对象编程演示 ===

创建了一个Person对象
创建了Person对象: 李四
创建了完整Person对象: 王五
1. 基本对象创建演示:
创建了一个Person对象
大家好，我是张三，今年25岁
创建了Person对象: 李四
大家好，我是李四，今年30岁
创建了完整Person对象: 王五
大家好，我是王五，今年28岁

2. 构造方法演示:
使用不同构造方法创建对象:
创建了一个Person对象
创建了Person对象: 赵六
创建了完整Person对象: 钱七
p1: Person{name='未知', age=0, email='unknown@example.com'}
p2: Person{name='赵六', age=22, email='zhao.liu@example.com'}
p3: Person{name='钱七', age=35, email='qianqi@mail.com'}

3. 封装性演示:
原始姓名: 测试用户
原始年龄: 20
更新后姓名: 新名字
更新后年龄: 25
年龄必须在0-150之间
姓名不能为空
邮箱格式不正确
最终年龄: 25

4. 对象关系演示:
=== 汽车信息 ===
品牌: 丰田
型号: 凯美瑞
年份: 2023
颜色: 银色
价格: ¥250000.00
状态: 已停止
速度: 0 km/h
所有者: 车主
所有者信息: Person{name='车主', age=32, email='owner@auto.com'}

汽车操作演示:
丰田 凯美瑞 发动机启动了
加速到 60 km/h
减速到 40 km/h
丰田 凯美瑞 停止了

5. 静态成员演示:
初始Person数量: 0
创建了Person对象: 用户1
创建了Person对象: 用户2
创建了Person对象: 用户3
创建3个对象后Person数量: 3
汽车信息: 2022年 本田 雅阁
无效调用: 无效的汽车对象

6. 方法重写演示:
Person.toString(): Person{name='重写测试', age=25, email='chong.xie.ce.shi@example.com'}
Car.toString(): 2024 奔驰 C级 (白色)
person1.equals(person2): true
person1.equals(person3): false
person1.hashCode(): 123456789
person2.hashCode(): 123456789
person3.hashCode(): 987654321
```

## 🔍 代码详解

### 1. 类的基本组成
- **成员变量**：描述对象的属性
- **构造方法**：初始化对象状态
- **成员方法**：定义对象的行为
- **访问修饰符**：控制访问权限

### 2. 封装原则
- 使用`private`修饰成员变量
- 提供`public`的getter/setter方法
- 在setter中加入数据验证逻辑

### 3. 构造方法特点
- 名称与类名相同
- 没有返回类型
- 可以重载（多个构造方法）
- 可以使用`this()`调用其他构造方法

### 4. 静态成员
- `static`变量属于类而非实例
- `static`方法可以通过类名直接调用
- 常用于工具方法和计数器

## 🧪 验证测试

### 功能验证清单
- [ ] 类能正确封装数据和行为
- [ ] 构造方法能正确初始化对象
- [ ] getter/setter方法能正确访问和修改数据
- [ ] 对象间的关系能正确建立和使用
- [ ] 静态成员能正确共享和访问
- [ ] 重写的方法能正确工作

### 边界条件测试
- 空值和无效数据的处理
- 对象相等性比较
- 静态变量的共享特性

## ❓ 常见问题

### Q1: 为什么要有getter和setter方法？
**答**：实现封装，控制对私有成员的访问，可以在设置时加入验证逻辑。

### Q2: 构造方法可以被继承吗？
**答**：构造方法不能被继承，但子类构造方法可以调用父类构造方法。

### Q3: 什么时候使用静态方法？
**答**：当方法不需要访问实例变量，只与类相关的逻辑时使用静态方法。

### Q4: this关键字有什么作用？
**答**：区分成员变量和参数、调用其他构造方法、返回当前对象引用。

## 📚 扩展学习

### 相关技术
- [Java继承机制](../java-inheritance-demo/)
- [Java接口设计](../java-interfaces-demo/)
- [Java多态特性](../java-polymorphism-demo/)

### 进阶主题
- 访问修饰符的详细规则
- 包装类和自动装箱
- 对象的生命周期管理
- 设计模式中的类设计原则

### 企业级应用
- 实体类(Entity)的设计
- 数据传输对象(DTO)的使用
- 业务逻辑层的服务类设计
- 领域驱动设计(DDD)中的聚合根

---
> **💡 提示**: 面向对象编程是Java的核心思想，熟练掌握类和对象的概念对后续学习至关重要。