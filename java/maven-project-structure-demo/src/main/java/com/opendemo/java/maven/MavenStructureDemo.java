package com.opendemo.java.maven;

import com.opendemo.java.maven.model.Student;
import com.opendemo.java.maven.service.StudentService;
import com.opendemo.java.maven.util.MathUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class MavenStructureDemo {

    private static final Logger logger = LoggerFactory.getLogger(MavenStructureDemo.class);

    public static void main(String[] args) {
        logger.info("=== Maven Project Structure Demo ===");
        logger.info("本项目演示Maven标准目录结构规范");
        logger.info("");

        logger.info("--- 1. 项目结构说明 ---");
        printProjectStructure();

        logger.info("");
        logger.info("--- 2. Student Service 演示 ---");
        demonstrateStudentService();

        logger.info("");
        logger.info("--- 3. MathUtils 工具类演示 ---");
        demonstrateMathUtils();
    }

    private static void printProjectStructure() {
        String[] structure = {
            "maven-project-structure-demo/",
            "├── pom.xml                          (项目对象模型配置文件)",
            "├── README.md                        (项目说明文档)",
            "├── metadata.json                    (项目元数据)",
            "├── src/",
            "│   ├── main/",
            "│   │   ├── java/                    (Java源代码目录)",
            "│   │   │   └── com/opendemo/java/maven/",
            "│   │   │       ├── MavenStructureDemo.java  (主入口类)",
            "│   │   │       ├── model/           (数据模型层)",
            "│   │   │       ├── service/         (业务逻辑层)",
            "│   │   │       ├── util/            (工具类)",
            "│   │   │       └── exception/       (自定义异常)",
            "│   │   └── resources/               (资源文件目录)",
            "│   └── test/",
            "│       └── java/                    (测试代码目录)",
            "└── target/                          (构建输出目录)"
        };
        for (String line : structure) {
            logger.info(line);
        }
    }

    private static void demonstrateStudentService() {
        StudentService studentService = new StudentService();

        studentService.addStudent(new Student(1, "张三", 20, "计算机科学"));
        studentService.addStudent(new Student(2, "李四", 21, "软件工程"));
        studentService.addStudent(new Student(3, "王五", 22, "数据科学"));

        List<Student> allStudents = studentService.getAllStudents();
        logger.info("所有学生数量: {}", allStudents.size());

        Student student = studentService.getStudentById(1);
        logger.info("查询ID=1的学生: {} - {}", student.getName(), student.getMajor());

        double avgAge = studentService.getAverageAge();
        logger.info("学生平均年龄: {}", avgAge);
    }

    private static void demonstrateMathUtils() {
        logger.info("计算阶乘 5! = {}", MathUtils.factorial(5));
        logger.info("判断质数 17 是否为质数: {}", MathUtils.isPrime(17));
        logger.info("斐波那契数列第10项: {}", MathUtils.fibonacci(10));
        logger.info("最大公约数 gcd(48, 36) = {}", MathUtils.gcd(48, 36));
    }
}
