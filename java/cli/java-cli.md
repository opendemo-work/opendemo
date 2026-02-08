# ☕ Java 命令行速查表 (java-cli.md)

> Java开发必备的命令行参考手册，涵盖JDK工具、构建工具、JVM调优、调试等核心功能，按功能分类整理，方便快速查找和使用

---

## 📋 目录索引

- [JDK基础命令](#jdk基础命令)
- [构建工具](#构建工具)
- [JVM调试](#jvm调试)
- [性能监控](#性能监控)
- [内存分析](#内存分析)
- [线程分析](#线程分析)
- [GC调优](#gc调优)
- [应用部署](#应用部署)
- [测试工具](#测试工具)
- [最佳实践](#最佳实践)

---

## JDK基础命令

### 编译和运行
```bash
# 编译Java文件
javac HelloWorld.java
javac -d classes src/**/*.java

# 运行Java程序
java HelloWorld
java -cp classes com.example.Main

# 查看Java版本
java -version
javac -version

# JAR文件操作
jar cf myapp.jar -C classes .
java -jar myapp.jar
```

### JVM参数设置
```bash
# 堆内存设置
java -Xms512m -Xmx2g MyApp

# 新生代设置
java -XX:NewRatio=2 -XX:SurvivorRatio=8 MyApp

# 栈内存设置
java -Xss1m MyApp

# 元空间设置
java -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m MyApp
```

---

## 构建工具

### Maven
```bash
# 项目构建
mvn clean compile
mvn clean package
mvn clean install

# 依赖管理
mvn dependency:tree
mvn dependency:analyze

# 插件执行
mvn spring-boot:run
mvn tomcat7:run

# 配置查看
mvn help:effective-pom
```

### Gradle
```bash
# 基础命令
gradle build
gradle clean build
gradle assemble

# 依赖管理
gradle dependencies
gradle dependencyInsight --dependency spring-core

# 任务查看
gradle tasks
gradle --gui
```

---

## JVM调试

### JDB调试器
```bash
# 启动调试模式
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 MyApp

# 连接调试器
jdb -attach localhost:5005

# JDB命令
> stop at com.example.MyClass:42
> run
> step
> print variableName
```

### 远程调试
```bash
# 启动应用时开启调试
JAVA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005"
java $JAVA_OPTS -jar myapp.jar

# IDE远程连接端口5005
```

---

## 性能监控

### JPS进程查看
```bash
# 查看Java进程
jps -l
jps -v  # 显示JVM参数
jps -m  # 显示main方法参数
```

### JStat统计监控
```bash
# GC统计
jstat -gc <pid> 1000 5

# 编译统计
jstat -compiler <pid>

# 类加载统计
jstat -class <pid>
```

### JInfo配置查看
```bash
# 查看JVM参数
jinfo <pid>
jinfo -flag MaxHeapSize <pid>
jinfo -flags <pid>
```

---

## 内存分析

### Heap Dump分析
```bash
# 生成堆转储
jmap -dump:live,format=b,file=heap.hprof <pid>

# 查看堆内存使用
jmap -heap <pid>
jmap -histo <pid>

# 内存分析工具
jhat heap.hprof
# 或使用Eclipse MAT, VisualVM等图形工具
```

### 内存泄漏检测
```bash
# 启用内存溢出时自动dump
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/path/to/dumps/

# OQL查询示例（MAT中使用）
SELECT * FROM java.util.HashMap WHERE size > 1000
```

---

## 线程分析

### JStack线程快照
```bash
# 生成线程快照
jstack <pid> > thread.dump

# 查找死锁
jstack -l <pid>

# 连续采样
while true; do jstack <pid> >> thread.log; sleep 10; done
```

### 线程状态分析
```bash
# 统计线程状态
grep "java.lang.Thread.State" thread.dump | sort | uniq -c

# 查找阻塞线程
grep -A 10 "BLOCKED" thread.dump

# 查找等待线程
grep -A 10 "WAITING" thread.dump
```

---

## GC调优

### GC日志分析
```bash
# 启用GC日志
-XX:+PrintGC
-XX:+PrintGCDetails
-XX:+PrintGCTimeStamps
-Xloggc:gc.log

# GC日志分析工具
gcviewer gc.log
gceasy.io (在线分析)
```

### 常用GC参数
```bash
# G1垃圾收集器
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16m

# CMS垃圾收集器
-XX:+UseConcMarkSweepGC
-XX:+CMSParallelRemarkEnabled
-XX:CMSInitiatingOccupancyFraction=70

# Parallel收集器
-XX:+UseParallelGC
-XX:ParallelGCThreads=4
```

---

## 应用部署

### Spring Boot应用
```bash
# 打包部署
mvn clean package
java -jar target/myapp-1.0.0.jar

# 环境配置
java -jar myapp.jar --spring.profiles.active=prod
export SPRING_PROFILES_ACTIVE=prod

# 系统属性设置
java -Dserver.port=8080 -Dspring.datasource.url=jdbc:mysql://localhost:3306/mydb -jar myapp.jar
```

### 容器化部署
```dockerfile
FROM openjdk:11-jre-slim
COPY target/myapp.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

```bash
docker build -t myapp:1.0 .
docker run -p 8080:8080 myapp:1.0
```

---

## 测试工具

### JUnit测试
```bash
# Maven测试
mvn test
mvn test -Dtest=MyTestClass
mvn test -Dtest=*IntegrationTest

# 测试覆盖率
mvn jacoco:prepare-agent test jacoco:report

# 并行测试
mvn test -Dparallel=methods -DthreadCount=4
```

### 性能测试
```bash
# JMH微基准测试
# 添加依赖后创建基准测试类
@Benchmark
public void testMethod() {
    // 测试代码
}

# 运行基准测试
java -jar target/benchmarks.jar
```

---

## 最佳实践

### 启动参数模板
```bash
JAVA_OPTS="
-server
-Xms2g -Xmx4g
-XX:NewRatio=2
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/logs/
-Xloggc:/logs/gc.log
-XX:+PrintGCDetails
-XX:+PrintGCTimeStamps
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
"
```

### 监控脚本示例
```bash
#!/bin/bash
# monitor.sh

PID=$(jps | grep MyApp | awk '{print $1}')
if [ ! -z "$PID" ]; then
    echo "=== Memory Info ==="
    jstat -gc $PID
    
    echo "=== Thread Count ==="
    jstack $PID | grep "java.lang.Thread.State" | wc -l
    
    echo "=== Heap Usage ==="
    jmap -heap $PID
fi
```

### 故障排查流程
```bash
# 1. 查看进程状态
jps -v

# 2. 检查内存使用
jstat -gc <pid> 1000 10

# 3. 生成线程快照
jstack <pid> > thread_$(date +%Y%m%d_%H%M%S).dump

# 4. 生成堆转储
jmap -dump:live,format=b,file=heap_$(date +%Y%m%d_%H%M%S).hprof <pid>

# 5. 分析GC日志
tail -f gc.log
```

---