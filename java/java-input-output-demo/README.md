# Java 输入输出演示

## 🎯 概述

Java IO (Input/Output) 是Java标准库中用于处理输入输出操作的核心API。本演示展示了Java中各种IO操作的使用方法，包括文件读写、流处理和NIO新特性。

## 🏗️ 技术架构

### 核心组件
- **主要技术**: Java IO/NIO API
- **适用场景**: 文件操作、数据流处理、网络通信
- **难度等级**: 🟡 中级

### 技术栈
```java
// 核心包
import java.io.*;
import java.nio.*;
import java.nio.channels.*;
import java.nio.file.*;
```

## 🚀 快速开始

### 环境准备
```bash
# 系统要求
- JDK 8+
- IDE (IntelliJ IDEA / Eclipse)

# 编译运行
javac -d bin src/**/*.java
java -cp bin com.example.io.DemoMain
```

## 📁 项目结构

```
java-input-output-demo/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── io/
│                       ├── FileOperations.java     # 文件操作示例
│                       ├── StreamExamples.java     # 流处理示例
│                       ├── NIOExamples.java        # NIO示例
│                       └── SerializationDemo.java  # 序列化示例
├── resources/
│   └── sample-data.txt
└── README.md
```

## 🔧 核心功能

### 功能特性
1. **文件读写**: 传统IO和NIO文件操作
2. **流处理**: 字节流、字符流、缓冲流
3. **序列化**: 对象序列化和反序列化
4. **通道操作**: NIO Channel和Buffer使用

## 📊 使用示例

### 基本文件读写
```java
// 传统IO文件读取
try (BufferedReader reader = Files.newBufferedReader(Paths.get("data.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
}

// NIO文件写入
String content = "Hello, Java NIO!";
Files.write(Paths.get("output.txt"), content.getBytes(), 
            StandardOpenOption.CREATE, StandardOpenOption.WRITE);
```

### 对象序列化
```java
// 序列化对象
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;
    private String name;
    private int age;
    
    // getters and setters...
}

// 序列化操作
Person person = new Person("张三", 25);
try (ObjectOutputStream oos = new ObjectOutputStream(
        Files.newOutputStream(Paths.get("person.ser")))) {
    oos.writeObject(person);
}
```

## ⚙️ 配置说明

### 系统属性
```bash
# JVM IO相关参数
-Dfile.encoding=UTF-8
-Djava.io.tmpdir=/tmp/java-io
-Dsun.nio.ch.disableSystemWideOverlappingFileLockCheck=true
```

## 🔍 故障排除

### 常见问题
1. **问题**: FileNotFoundException
   - **解决方案**: 检查文件路径和权限

2. **问题**: EOFException
   - **解决方案**: 确保文件完整性和正确的读取方式

## 🧪 测试验证

### 单元测试
```java
@Test
public void testFileReadWrite() throws IOException {
    Path tempFile = Files.createTempFile("test", ".txt");
    String testData = "Test data for IO operations";
    
    // 写入测试
    Files.write(tempFile, testData.getBytes());
    
    // 读取验证
    String content = new String(Files.readAllBytes(tempFile));
    assertEquals(testData, content);
    
    // 清理
    Files.delete(tempFile);
}
```

## 📚 相关资源

### 官方文档
- [Java IO Tutorial](https://docs.oracle.com/javase/tutorial/essential/io/)
- [Java NIO Documentation](https://docs.oracle.com/javase/8/docs/api/java/nio/package-summary.html)

### 学习资源
- 《Java核心技术》IO章节
- Oracle Java IO最佳实践指南

---
*最后更新: 2026年2月3日*