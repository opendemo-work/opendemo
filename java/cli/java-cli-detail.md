# Java CLI命令详解

本文档详细解释Java开发常用CLI命令的用途、输出示例、内容解析、注意事项以及在生产环境中执行的安全风险。

## 1. java (Java虚拟机)

### 用途
`java` 是Java虚拟机的启动命令，用于运行已编译的Java程序（.class文件）和JAR包。是Java应用部署和执行的核心工具。

### 输出示例
```bash
# 运行简单的Java程序
$ java HelloWorld
Hello, World!

# 运行指定类文件
$ java -cp . com.example.MyApplication
Application started successfully
Loading configuration...
Connecting to database...

# 运行JAR文件
$ java -jar myapp.jar
2023-12-07 15:30:15 INFO  Starting application
2023-12-07 15:30:16 INFO  Server started on port 8080

# 指定JVM参数
$ java -Xmx1024m -Xms512m -jar myapp.jar
2023-12-07 15:32:10 INFO  JVM Heap: 512MB initial, 1024MB maximum

# 设置系统属性
$ java -Dserver.port=9090 -Dspring.profiles.active=prod -jar myapp.jar
2023-12-07 15:33:22 INFO  Active profile: prod
2023-12-07 15:33:23 INFO  Server started on port 9090

# 启用远程调试
$ java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar myapp.jar
Listening for transport dt_socket at address: 5005
2023-12-07 15:34:45 INFO  Application started

# 查看Java版本
$ java -version
openjdk version "17.0.8" 2023-07-18
OpenJDK Runtime Environment (build 17.0.8+7-Ubuntu-120.04)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Ubuntu-120.04, mixed mode, sharing)

# 显示详细版本信息
$ java -fullversion
openjdk full version "17.0.8+7-Ubuntu-120.04"

# 显示Java系统属性
$ java -XshowSettings:properties -version
Property settings:
    awt.toolkit = sun.awt.X11.XToolkit
    file.encoding = UTF-8
    file.separator = /
    java.awt.graphicsenv = sun.awt.X11GraphicsEnvironment
    java.class.path = .
    java.home = /usr/lib/jvm/java-17-openjdk-amd64
    java.io.tmpdir = /tmp
    java.runtime.name = OpenJDK Runtime Environment
    java.runtime.version = 17.0.8+7-Ubuntu-120.04
    java.vendor = Private Build
    java.vendor.url = Unknown
    java.vendor.url.bug = Unknown
    java.version = 17.0.8
    java.version.date = 2023-07-18
    java.vm.name = OpenJDK 64-Bit Server VM
    java.vm.specification.name = Java Virtual Machine Specification
    java.vm.specification.vendor = Oracle Corporation
    java.vm.specification.version = 17
    java.vm.vendor = Private Build
    java.vm.version = 17.0.8+7-Ubuntu-120.04
    line.separator = \n
    os.arch = amd64
    os.name = Linux
    os.version = 5.15.0-76-generic
    path.separator = :
    user.dir = /home/user/project
    user.home = /home/user
    user.name = user

openjdk version "17.0.8" 2023-07-18
OpenJDK Runtime Environment (build 17.0.8+7-Ubuntu-120.04)
OpenJDK 64-Bit Server VM (build 17.0.8+7-Ubuntu-120.04, mixed mode, sharing)
```

### 内容解析
- **程序输出**: Java应用程序的标准输出内容
- **版本信息**: JVM版本、供应商和构建信息
- **系统属性**: Java运行时环境的各种配置参数
- **调试信息**: 远程调试连接的端口和状态
- **内存配置**: JVM堆内存的初始和最大设置

### 常用参数详解
- `-jar <file.jar>`: 运行JAR文件
- `-cp, -classpath <path>`: 设置类路径
- `-D<name>=<value>`: 设置系统属性
- `-Xmx<size>`: 设置最大堆内存大小
- `-Xms<size>`: 设置初始堆内存大小
- `-agentlib:jdwp=...`: 启用JDWP调试代理
- `-version`: 显示Java版本信息
- `-showversion`: 显示版本信息并继续执行

### 注意事项
- 生产环境应固定JVM版本避免兼容性问题
- 合理设置堆内存大小避免OOM错误
- 启用GC日志便于性能分析
- 使用JVM参数优化应用性能

### 安全风险
- ⚠️ 运行不受信任的Java代码存在安全风险
- ⚠️ JVM参数配置不当可能影响系统安全
- ⚠️ 远程调试端口暴露可能带来安全威胁
- ⚠️ 系统属性可能包含敏感配置信息

## 2. javac (Java编译器)

### 用途
`javac` 是Java源代码编译器，将.java文件编译为JVM可执行的.class字节码文件。是Java开发的基础工具。

### 输出示例
```bash
# 编译单个Java文件
$ javac HelloWorld.java
$ ls -la HelloWorld.class
-rw-r--r-- 1 user user 426 Dec  7 15:45 HelloWorld.class

# 编译多个Java文件
$ javac Main.java Utils.java Models.java
$ ls -la *.class
-rw-r--r-- 1 user user 1024 Dec  7 15:46 Main.class
-rw-r--r-- 1 user user  845 Dec  7 15:46 Utils.class
-rw-r--r-- 1 user user 1267 Dec  7 15:46 Models.class

# 指定输出目录
$ javac -d build/classes Main.java
$ ls -la build/classes/
total 12
drwxr-xr-x 2 user user 4096 Dec  7 15:47 .
drwxr-xr-x 3 user user 4096 Dec  7 15:47 ..
-rw-r--r-- 1 user user 1024 Dec  7 15:47 Main.class

# 指定类路径编译
$ javac -cp lib/commons-lang3-3.12.0.jar -d build/classes src/com/example/Main.java
$ ls -la build/classes/com/example/
-rw-r--r-- 1 user user 2048 Dec  7 15:48 Main.class

# 编译整个源码目录
$ javac -d build/classes -sourcepath src $(find src -name "*.java")
$ find build/classes -name "*.class" | wc -l
25

# 显示编译详细信息
$ javac -verbose Main.java
[parsing started RegularFileObject[Main.java]]
[parsing completed 12ms]
[search path for source files: .]
[search path for class files: ...]
[loading RegularFileObject[java/lang/Object.class]]
[checking com.example.Main]
[writing to RegularFileObject[Main.class]]
[total 85ms]

# 编译时显示警告信息
$ javac -Xlint Main.java
Main.java:15: warning: [deprecation] Date() in Date has been deprecated
        Date now = new Date();
                   ^
1 warning

# 生成调试信息
$ javac -g Main.java
$ javap -v Main.class | grep "LineNumberTable" -A 5
LineNumberTable:
        line 3: 0
        line 4: 8
        line 5: 16
        line 6: 24

# 编译指定Java版本
$ javac -source 11 -target 11 Main.java
$ file Main.class
Main.class: compiled Java class data, version 55.0 (Java 11)
```

### 内容解析
- **编译输出**: 生成的.class文件
- **编译过程**: verbose模式显示的详细编译步骤
- **警告信息**: 代码中潜在问题的警告
- **调试信息**: 行号表等调试相关数据
- **版本信息**: 编译目标的Java版本

### 常用参数详解
- `<source files>`: 要编译的Java源文件
- `-d <directory>`: 指定编译输出目录
- `-cp, -classpath <path>`: 设置类路径
- `-sourcepath <path>`: 设置源文件搜索路径
- `-verbose`: 显示详细编译信息
- `-Xlint`: 启用额外的警告检查
- `-g`: 生成所有调试信息
- `-source <release>`: 指定源代码版本
- `-target <release>`: 指定目标JVM版本

### 注意事项
- 确保源文件编码与编译器设置一致
- 大型项目建议使用构建工具（Maven/Gradle）
- 合理组织包结构便于编译管理
- 注意依赖包的版本兼容性

### 安全风险
- ⚠️ 编译恶意Java代码可能带来安全风险
- ⚠️ 依赖的第三方库可能存在安全漏洞
- ⚠️ 编译参数设置不当可能影响代码安全性
- ⚠️ 生成的字节码可能被反编译分析

## 3. jar (Java Archive工具)

### 用途
`jar` 用于创建和管理JAR（Java Archive）文件，可以打包Java类文件、资源文件和元数据，便于分发和部署Java应用程序。

### 输出示例
```bash
# 创建简单的JAR文件
$ jar cf myapp.jar *.class
$ ls -la myapp.jar
-rw-r--r-- 1 user user 2048 Dec  7 16:00 myapp.jar

# 创建带清单的JAR文件
$ echo "Main-Class: com.example.Main" > manifest.txt
$ jar cfm myapp.jar manifest.txt -C build/classes .
$ java -jar myapp.jar
Hello, World!

# 查看JAR文件内容
$ jar tf myapp.jar
META-INF/
META-INF/MANIFEST.MF
com/
com/example/
com/example/Main.class
com/example/Utils.class

# 详细查看JAR文件内容
$ jar tvf myapp.jar
     0 Fri Dec 07 16:00:00 CST 2023 META-INF/
   168 Fri Dec 07 16:00:00 CST 2023 META-INF/MANIFEST.MF
     0 Fri Dec 07 16:00:00 CST 2023 com/
     0 Fri Dec 07 16:00:00 CST 2023 com/example/
  1024 Fri Dec 07 16:00:00 CST 2023 com/example/Main.class
   845 Fri Dec 07 16:00:00 CST 2023 com/example/Utils.class

# 解压JAR文件
$ jar xf myapp.jar
$ ls -la
total 20
drwxr-xr-x 4 user user 4096 Dec  7 16:02 .
drwxr-xr-x 8 user user 4096 Dec  7 16:00 ..
drwxr-xr-x 3 user user 4096 Dec  7 16:02 com
drwxr-xr-x 2 user user 4096 Dec  7 16:02 META-INF

# 更新JAR文件
$ echo "Updated content" > newfile.txt
$ jar uf myapp.jar newfile.txt
$ jar tf myapp.jar | grep newfile
newfile.txt

# 创建可执行JAR并压缩
$ jar cfe app.jar com.example.Main -C build/classes .
$ ls -la app.jar
-rw-r--r-- 1 user user 1536 Dec  7 16:05 app.jar

# 验证JAR文件签名
$ jarsigner -verify my-signed-app.jar
jar verified.

# 签名JAR文件
$ jarsigner -keystore mykeystore.jks myapp.jar myalias
Enter Passphrase for keystore: *****
jar signed.

# 创建模块化JAR（Java 9+）
$ jar --create --file modular-app.jar --main-class com.example.Main -C build/modules .
$ java -p modular-app.jar -m com.example/com.example.Main
```

### 内容解析
- **文件列表**: JAR包中包含的文件和目录结构
- **详细信息**: 文件大小、修改时间和权限信息
- **清单文件**: MANIFEST.MF中的元数据信息
- **签名状态**: JAR文件的数字签名验证结果
- **模块信息**: Java 9+模块化JAR的模块描述

### 常用参数详解
- `cf <jar-file> <input-files>`: 创建JAR文件
- `cfm <jar-file> <manifest-file> <input-files>`: 创建带清单的JAR
- `tf <jar-file>`: 列出JAR文件内容
- `xf <jar-file>`: 解压JAR文件
- `uf <jar-file> <input-files>`: 更新JAR文件
- `cfe <jar-file> <main-class> <input-files>`: 创建可执行JAR
- `-v`: 显示详细输出
- `--create`: 创建操作（Java 9+）
- `--file`: 指定JAR文件名（Java 9+）

### 注意事项
- 可执行JAR需要正确的Main-Class清单项
- 大型JAR文件应考虑压缩和分片
- 注意JAR文件中的路径分隔符（Unix使用/）
- 生产环境应使用数字签名保护JAR文件

### 安全风险
- ⚠️ 运行未签名的JAR文件存在安全风险
- ⚠️ JAR文件可能包含恶意代码
- ⚠️ 签名密钥管理不当可能被滥用
- ⚠️ 解压JAR文件可能覆盖重要系统文件

## 4. mvn (Maven构建工具)

### 用途
`mvn` 是Apache Maven的命令行工具，用于Java项目的依赖管理、构建、测试和部署。是企业级Java开发的标准构建工具。

### 输出示例
```bash
# 查看Maven版本
$ mvn -version
Apache Maven 3.9.4 (72683492debc477de33f04c34aa97c75ecd3890f)
Maven home: /opt/apache-maven-3.9.4
Java version: 17.0.8, vendor: Private Build, runtime: /usr/lib/jvm/java-17-openjdk-amd64
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "5.15.0-76-generic", arch: "amd64", family: "unix"

# 清理项目
$ mvn clean
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- clean:3.2.0:clean (default-clean) @ my-project ---
[INFO] Deleting /home/user/project/target
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.456 s
[INFO] Finished at: 2023-12-07T16:15:23+08:00
[INFO] ------------------------------------------------------------------------

# 编译项目
$ mvn compile
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- maven-resources-plugin:3.3.1:resources (default-resources) @ my-project ---
[INFO] Copying 2 resources from src/main/resources to target/classes
[INFO] 
[INFO] --- maven-compiler-plugin:3.11.0:compile (default-compile) @ my-project ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 15 source files with javac [debug target 17] to target/classes
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.345 s
[INFO] Finished at: 2023-12-07T16:16:45+08:00

# 运行测试
$ mvn test
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- surefire:3.1.2:test (default-test) @ my-project ---
[INFO] Using auto detected provider org.apache.maven.surefire.junitplatform.JUnitPlatformProvider
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.example.MyServiceTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.456 s - in com.example.MyServiceTest
[INFO] Running com.example.util.StringUtilsTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.123 s - in com.example.util.StringUtilsTest
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  4.567 s
[INFO] Finished at: 2023-12-07T16:18:12+08:00

# 打包项目
$ mvn package
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- jar:3.3.0:jar (default-jar) @ my-project ---
[INFO] Building jar: /home/user/project/target/my-project-1.0.0.jar
[INFO] 
[INFO] --- spring-boot-maven-plugin:3.1.2:repackage (repackage) @ my-project ---
[INFO] Replacing main artifact with repackaged archive
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  6.789 s
[INFO] Finished at: 2023-12-07T16:20:34+08:00

# 安装到本地仓库
$ mvn install
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- install:3.1.1:install (default-install) @ my-project ---
[INFO] Installing /home/user/project/target/my-project-1.0.0.jar to /home/user/.m2/repository/com/example/my-project/1.0.0/my-project-1.0.0.jar
[INFO] Installing /home/user/project/pom.xml to /home/user/.m2/repository/com/example/my-project/1.0.0/my-project-1.0.0.pom
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  2.345 s
[INFO] Finished at: 2023-12-07T16:22:15+08:00

# 下载依赖
$ mvn dependency:resolve
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- dependency:3.6.0:resolve (default-cli) @ my-project ---
[INFO] Dependencies resolved successfully
[INFO] The following files have been resolved:
[INFO]    org.springframework:spring-core:jar:6.0.11:compile
[INFO]    org.springframework:spring-context:jar:6.0.11:compile
[INFO]    org.springframework.boot:spring-boot-starter-web:jar:3.1.2:compile
[INFO]    ch.qos.logback:logback-classic:jar:1.4.8:compile
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  3.456 s
[INFO] Finished at: 2023-12-07T16:24:28+08:00

# 分析依赖树
$ mvn dependency:tree
[INFO] Scanning for projects...
[INFO] 
[INFO] ---------------------< com.example:my-project >----------------------
[INFO] Building my-project 1.0.0
[INFO]   from pom.xml
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- dependency:3.6.0:tree (default-cli) @ my-project ---
[INFO] com.example:my-project:jar:1.0.0
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:3.1.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:3.1.2:compile
[INFO] |  |  +- org.springframework.boot:spring-boot:jar:3.1.2:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-autoconfigure:jar:3.1.2:compile
[INFO] |  |  +- jakarta.annotation:jakarta.annotation-api:jar:2.1.1:compile
[INFO] |  |  \- org.yaml:snakeyaml:jar:1.33:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-json:jar:3.1.2:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.15.2:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-annotations:jar:2.15.2:compile
[INFO] |  |  \- com.fasterxml.jackson.core:jackson-core:jar:2.15.2:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-tomcat:jar:3.1.2:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-core:jar:10.1.11:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-el:jar:10.1.11:compile
[INFO] |  |  \- org.apache.tomcat.embed:tomcat-embed-websocket:jar:10.1.11:compile
[INFO] |  +- org.springframework:spring-web:jar:6.0.11:compile
[INFO] |  |  \- org.springframework:spring-beans:jar:6.0.11:compile
[INFO] |  \- org.springframework:spring-webmvc:jar:6.0.11:compile
[INFO] |     +- org.springframework:spring-aop:jar:6.0.11:compile
[INFO] |     +- org.springframework:spring-context:jar:6.0.11:compile
[INFO] |     \- org.springframework:spring-expression:jar:6.0.11:compile
[INFO] \- org.springframework.boot:spring-boot-starter-test:jar:3.1.2:test
[INFO]    +- org.springframework.boot:spring-boot-test:jar:3.1.2:test
[INFO]    +- org.springframework.boot:spring-boot-test-autoconfigure:jar:3.1.2:test
[INFO]    +- com.jayway.jsonpath:json-path:jar:2.8.0:test
[INFO]    +- jakarta.xml.bind:jakarta.xml.bind-api:jar:4.0.0:test
[INFO]    +- net.minidev:json-smart:jar:2.4.11:test
[INFO]    +- org.assertj:assertj-core:jar:3.24.2:test
[INFO]    +- org.hamcrest:hamcrest:jar:2.2:test
[INFO]    +- org.junit.jupiter:junit-jupiter:jar:5.9.3:test
[INFO]    +- org.mockito:mockito-core:jar:5.3.1:test
[INFO]    +- org.skyscreamer:jsonassert:jar:1.5.1:test
[INFO]    +- org.springframework:spring-core:jar:6.0.11:compile
[INFO]    |  \- org.springframework:spring-jcl:jar:6.0.11:compile
[INFO]    +- org.springframework:spring-test:jar:6.0.11:test
[INFO]    \- org.xmlunit:xmlunit-core:jar:2.9.1:test
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

### 内容解析
- **构建阶段**: 显示Maven生命周期的各个执行阶段
- **插件执行**: 显示各Maven插件的执行过程和结果
- **依赖解析**: 显示项目依赖的下载和解析过程
- **测试结果**: 显示单元测试的执行情况和统计
- **构建产物**: 显示生成的JAR文件和其他构建产物

### 常用参数详解
- `clean`: 清理构建目录
- `compile`: 编译源代码
- `test`: 运行单元测试
- `package`: 打包项目
- `install`: 安装到本地仓库
- `deploy`: 部署到远程仓库
- `dependency:resolve`: 解析并下载依赖
- `dependency:tree`: 显示依赖树
- `-U`: 强制更新SNAPSHOT依赖
- `-X`: 显示调试信息

### 注意事项
- 确保pom.xml配置正确
- 定期清理本地仓库避免空间不足
- 生产环境应使用Release版本而非SNAPSHOT
- 注意依赖版本冲突问题
- 合理配置Maven镜像提高下载速度

### 安全风险
- ⚠️ 第三方依赖可能存在安全漏洞
- ⚠️ SNAPSHOT版本可能引入不稳定代码
- ⚠️ 仓库配置不当可能下载恶意依赖
- ⚠️ 插件配置错误可能影响构建安全

## 5. gradle (Gradle构建工具)

### 用途
`gradle` 是现代化的构建自动化工具，使用Groovy或Kotlin DSL配置，支持增量构建和丰富的插件生态。逐渐成为Java开发的主流选择。

### 输出示例
```bash
# 查看Gradle版本
$ gradle --version
------------------------------------------------------------
Gradle 8.4
------------------------------------------------------------

Build time:   2023-09-25 12:34:34 UTC
Revision:     a89f255c1022c9575893ffff38fb9dc91fc781d7

Kotlin:       1.9.10
Groovy:       3.0.17
Ant:          Apache Ant(TM) version 1.10.13 compiled on January 4 2023
JVM:          17.0.8 (Private Build 17.0.8+7-Ubuntu-120.04)
OS:           Linux 5.15.0-76-generic amd64

# 列出可用任务
$ gradle tasks
> Task :tasks

------------------------------------------------------------
Tasks runnable from root project 'my-project'
------------------------------------------------------------

Application tasks
-----------------
run - Runs this project as a JVM application

Build tasks
-----------
assemble - Assembles the outputs of this project.
build - Assembles and tests this project.
buildDependents - Assembles and tests this project and all projects that depend on it.
buildNeeded - Assembles and tests this project and all projects it depends on.
classes - Assembles main classes.
clean - Deletes the build directory.
jar - Assembles a jar archive containing the main classes.
test - Runs the unit tests.

Build Setup tasks
-----------------
init - Initializes a new Gradle build.
wrapper - Generates Gradle wrapper files.

Documentation tasks
-------------------
javadoc - Generates Javadoc API documentation for the main source code.

Help tasks
----------
buildEnvironment - Displays all buildscript dependencies declared in root project 'my-project'.
components - Displays the components produced by root project 'my-project'.
dependencies - Displays all dependencies declared in root project 'my-project'.
dependencyInsight - Displays the insight into a specific dependency in root project 'my-project'.
dependentComponents - Displays the dependent components of components in root project 'my-project'.
help - Displays a help message.
model - Displays the configuration model of root project 'my-project'.
outgoingVariants - Displays the outgoing variants of root project 'my-project'.
projects - Displays the sub-projects of root project 'my-project'.
properties - Displays the properties of root project 'my-project'.
resolvableConfigurations - Displays the configurations that can be resolved in root project 'my-project'.
tasks - Displays the tasks runnable from root project 'my-project'.

Verification tasks
------------------
check - Runs all checks.
test - Runs the unit tests.

Other tasks
-----------
compileJava
compileTestJava
processResources
processTestResources

# 编译项目
$ gradle compileJava
> Task :compileJava
Note: Some input files use unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.

BUILD SUCCESSFUL in 2s
2 actionable tasks: 2 executed

# 运行测试
$ gradle test
> Task :test

MyServiceTest > testBasicFunctionality() PASSED
MyServiceTest > testEdgeCases() PASSED
StringUtilsTest > testNullOrEmptyStrings() PASSED
StringUtilsTest > testNormalStrings() PASSED

BUILD SUCCESSFUL in 3s
3 actionable tasks: 3 executed

# 打包项目
$ gradle jar
> Task :compileJava UP-TO-DATE
> Task :processResources NO-SOURCE
> Task :classes
> Task :jar

BUILD SUCCESSFUL in 1s
2 actionable tasks: 1 executed, 1 up-to-date

# 构建完整项目
$ gradle build
> Task :compileJava UP-TO-DATE
> Task :processResources NO-SOURCE
> Task :classes
> Task :jar
> Task :startScripts NO-SOURCE
> Task :distTar NO-SOURCE
> Task :distZip NO-SOURCE
> Task :assemble
> Task :compileTestJava UP-TO-DATE
> Task :processTestResources NO-SOURCE
> Task :testClasses UP-TO-DATE
> Task :test
> Task :check
> Task :build

BUILD SUCCESSFUL in 4s
5 actionable tasks: 3 executed, 2 up-to-date

# 查看依赖
$ gradle dependencies
> Task :dependencies

------------------------------------------------------------
Root project 'my-project'
------------------------------------------------------------

annotationProcessor - Annotation processors and their dependencies for source set 'main'.
No dependencies

api - API dependencies for source set 'main'. (n)
No dependencies

apiElements - API elements for main. (n)
No dependencies

archives - Configuration for archive artifacts. (n)
No dependencies

bootArchives - Configuration for Spring Boot archive artifacts.
No dependencies

compileClasspath - Compile classpath for source set 'main'.
+--- org.springframework.boot:spring-boot-starter-web:3.1.2
|    +--- org.springframework.boot:spring-boot-starter:3.1.2
|    |    +--- org.springframework.boot:spring-boot:3.1.2
|    |    +--- org.springframework.boot:spring-boot-autoconfigure:3.1.2
|    |    +--- org.springframework.boot:spring-boot-starter-logging:3.1.2
|    |    |    +--- ch.qos.logback:logback-classic:1.4.8
|    |    |    |    +--- ch.qos.logback:logback-core:1.4.8
|    |    |    |    \--- org.slf4j:slf4j-api:2.0.7
|    |    |    +--- org.apache.logging.log4j:log4j-to-slf4j:2.20.0
|    |    |    |    +--- org.apache.logging.log4j:log4j-api:2.20.0
|    |    |    |    \--- org.slf4j:slf4j-api:2.0.7
|    |    |    \--- org.slf4j:jul-to-slf4j:2.0.7
|    |    |         \--- org.slf4j:slf4j-api:2.0.7
|    |    +--- jakarta.annotation:jakarta.annotation-api:2.1.1
|    |    +--- org.springframework:spring-core:6.0.11
|    |    |    \--- org.springframework:spring-jcl:6.0.11
|    |    \--- org.yaml:snakeyaml:1.33
|    +--- org.springframework.boot:spring-boot-starter-json:3.1.2
|    |    +--- com.fasterxml.jackson.core:jackson-databind:2.15.2
|    |    |    +--- com.fasterxml.jackson.core:jackson-annotations:2.15.2
|    |    |    \--- com.fasterxml.jackson.core:jackson-core:2.15.2
|    |    +--- com.fasterxml.jackson.datatype:jackson-datatype-jdk8:2.15.2
|    |    +--- com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.2
|    |    \--- com.fasterxml.jackson.module:jackson-module-parameter-names:2.15.2
|    +--- org.springframework.boot:spring-boot-starter-tomcat:3.1.2
|    |    +--- org.apache.tomcat.embed:tomcat-embed-core:10.1.11
|    |    +--- org.apache.tomcat.embed:tomcat-embed-el:10.1.11
|    |    \--- org.apache.tomcat.embed:tomcat-embed-websocket:10.1.11
|    +--- org.springframework:spring-web:6.0.11
|    |    \--- org.springframework:spring-beans:6.0.11
|    \--- org.springframework:spring-webmvc:6.0.11
|         +--- org.springframework:spring-aop:6.0.11
|         +--- org.springframework:spring-context:6.0.11
|         \--- org.springframework:spring-expression:6.0.11
\--- org.springframework.boot:spring-boot-starter-test:3.1.2
     +--- org.springframework.boot:spring-boot-test:3.1.2
     +--- org.springframework.boot:spring-boot-test-autoconfigure:3.1.2
     +--- com.jayway.jsonpath:json-path:2.8.0
     +--- jakarta.xml.bind:jakarta.xml.bind-api:4.0.0
     +--- net.minidev:json-smart:2.4.11
     +--- org.assertj:assertj-core:3.24.2
     +--- org.hamcrest:hamcrest:2.2
     +--- org.junit.jupiter:junit-jupiter:5.9.3
     +--- org.mockito:mockito-core:5.3.1
     +--- org.skyscreamer:jsonassert:1.5.1
     +--- org.springframework:spring-core:6.0.11 (*)
     +--- org.springframework:spring-test:6.0.11
     \--- org.xmlunit:xmlunit-core:2.9.1

# 运行应用程序
$ gradle run
> Task :compileJava UP-TO-DATE
> Task :processResources NO-SOURCE
> Task :classes
> Task :run
2023-12-07T16:35:12.345+08:00  INFO 12345 --- [           main] com.example.Application                  : Starting Application using Java 17.0.8
2023-12-07T16:35:12.456+08:00  INFO 12345 --- [           main] com.example.Application                  : No active profile set, falling back to 1 default profile: "default"
2023-12-07T16:35:13.567+08:00  INFO 12345 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2023-12-07T16:35:13.678+08:00  INFO 12345 --- [           main] com.example.Application                  : Started Application in 1.892 seconds (process running for 2.123)

BUILD SUCCESSFUL in 4s
3 actionable tasks: 2 executed, 1 up-to-date
```

### 内容解析
- **任务执行**: 显示Gradle任务的执行过程和状态
- **依赖解析**: 显示项目依赖的树状结构
- **构建输出**: 显示编译、测试、打包等各阶段的结果
- **应用运行**: 显示Spring Boot等应用的启动日志
- **性能信息**: 显示构建耗时和任务执行统计

### 常用参数详解
- `tasks`: 列出所有可用任务
- `build`: 完整构建项目
- `clean`: 清理构建目录
- `compileJava`: 编译Java源代码
- `test`: 运行测试
- `jar`: 打包JAR文件
- `run`: 运行应用程序
- `dependencies`: 显示依赖树
- `--info`: 显示详细信息
- `--debug`: 显示调试信息
- `--dry-run`: 预演构建过程不实际执行

### 注意事项
- Gradle Wrapper确保构建环境一致性
- 增量构建提高开发效率
- 合理配置构建缓存
- 注意插件版本兼容性
- 生产环境应使用稳定的Gradle版本

### 安全风险
- ⚠️ 第三方插件可能存在安全风险
- ⚠️ 构建脚本可能执行恶意代码
- ⚠️ 依赖管理不当可能引入漏洞
- ⚠️ 网络依赖下载可能被劫持

## 6. jstack (Java堆栈跟踪工具)

### 用途
`jstack` 用于打印Java进程的线程堆栈跟踪信息，是分析Java应用性能问题和死锁的重要诊断工具。

### 输出示例
```bash
# 查看Java进程列表
$ jps -l
12345 com.example.Application
12346 org.apache.catalina.startup.Bootstrap
12347 jdk.jcmd/sun.tools.jps.Jps

# 获取进程堆栈跟踪
$ jstack 12345
2023-12-07 16:45:12
Full thread dump OpenJDK 64-Bit Server VM (17.0.8+7-Ubuntu-120.04 mixed mode, sharing):

Threads class SMR info:
_java_thread_list=0x00007f8b4c000b60, length=15, elements={
0x00007f8b48012800, 0x00007f8b48014800, 0x00007f8b48016800,
0x00007f8b48018800, 0x00007f8b4801a800, 0x00007f8b4801c800,
0x00007f8b4801e800, 0x00007f8b48020800, 0x00007f8b48022800,
0x00007f8b48024800, 0x00007f8b48026800, 0x00007f8b48028800,
0x00007f8b4802a800, 0x00007f8b4802c800, 0x00007f8b4802e800
}

"main" #1 prio=5 os_prio=0 cpu=1234.56ms elapsed=123.45s tid=0x00007f8b48012800 nid=0x303b waiting on condition  [0x00007f8b50c4b000]
   java.lang.Thread.State: WAITING (parking)
	at jdk.internal.misc.Unsafe.park(java.base@17.0.8/Native Method)
	- parking to wait for  <0x0000000082345678> (a java.util.concurrent.FutureTask)
	at java.util.concurrent.locks.LockSupport.park(java.base@17.0.8/LockSupport.java:341)
	at java.util.concurrent.FutureTask.awaitDone(java.base@17.0.8/FutureTask.java:500)
	at java.util.concurrent.FutureTask.get(java.base@17.0.8/FutureTask.java:190)
	at org.springframework.context.support.AbstractApplicationContext.finishRefresh(AbstractApplicationContext.java:938)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:586)
	at org.springframework.boot.web.servlet.context.ServletWebServerApplicationContext.refresh(ServletWebServerApplicationContext.java:147)
	at org.springframework.boot.SpringApplication.refresh(SpringApplication.java:734)
	at org.springframework.boot.SpringApplication.refreshContext(SpringApplication.java:436)
	at org.springframework.boot.SpringApplication.run(SpringApplication.java:312)
	at com.example.Application.main(Application.java:15)

"http-nio-8080-exec-1" #20 daemon prio=5 os_prio=0 cpu=45.67ms elapsed=120.23s tid=0x00007f8b48024800 nid=0x304f runnable  [0x00007f8b2bff9000]
   java.lang.Thread.State: RUNNABLE
	at sun.nio.ch.EPoll.wait(java.base@17.0.8/Native Method)
	at sun.nio.ch.EPollSelectorImpl.doSelect(java.base@17.0.8/EPollSelectorImpl.java:120)
	at sun.nio.ch.SelectorImpl.lockAndDoSelect(java.base@17.0.8/SelectorImpl.java:129)
	- locked <0x0000000082456789> (a sun.nio.ch.Util$2)
	- locked <0x0000000082456790> (a sun.nio.ch.EPollSelectorImpl)
	at sun.nio.ch.SelectorImpl.select(java.base@17.0.8/SelectorImpl.java:141)
	at org.apache.tomcat.util.net.NioEndpoint$Poller.run(NioEndpoint.java:732)
	at java.lang.Thread.run(java.base@17.0.8/Thread.java:833)

"http-nio-8080-exec-2" #21 daemon prio=5 os_prio=0 cpu=23.45ms elapsed=120.23s tid=0x00007f8b48026800 nid=0x3050 waiting on condition  [0x00007f8b2bef8000]
   java.lang.Thread.State: WAITING (parking)
	at jdk.internal.misc.Unsafe.park(java.base@17.0.8/Native Method)
	- parking to wait for  <0x0000000082567890> (a org.apache.tomcat.util.threads.TaskQueue)
	at java.util.concurrent.locks.LockSupport.park(java.base@17.0.8/LockSupport.java:341)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionNode.await(java.base@17.0.8/AbstractQueuedSynchronizer.java:2404)
	at java.util.concurrent.LinkedBlockingQueue.take(java.base@17.0.8/LinkedBlockingQueue.java:435)
	at org.apache.tomcat.util.threads.TaskQueue.take(TaskQueue.java:107)
	at org.apache.tomcat.util.threads.TaskQueue.take(TaskQueue.java:33)
	at java.util.concurrent.ThreadPoolExecutor.getTask(java.base@17.0.8/ThreadPoolExecutor.java:1062)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@17.0.8/ThreadPoolExecutor.java:1122)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@17.0.8/ThreadPoolExecutor.java:635)
	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
	at java.lang.Thread.run(java.base@17.0.8/Thread.java:833)

# 检测死锁
$ jstack -l 12345
2023-12-07 16:46:25
Full thread dump OpenJDK 64-Bit Server VM (17.0.8+7-Ubuntu-120.04 mixed mode, sharing):

Found one Java-level deadlock:
=============================
"Thread-1":
  waiting to lock monitor 0x00007f8b4803a800 (object 0x0000000082678901, a java.lang.Object),
  which is held by "Thread-2"
"Thread-2":
  waiting to lock monitor 0x00007f8b4803b000 (object 0x0000000082678902, a java.lang.Object),
  which is held by "Thread-1"

Java stack information for the threads listed above:
===================================================
"Thread-1":
	at com.example.DeadlockExample.method1(DeadlockExample.java:15)
	- waiting to lock <0x0000000082678901> (a java.lang.Object)
	- locked <0x0000000082678902> (a java.lang.Object)
	at com.example.DeadlockExample.lambda$main$0(DeadlockExample.java:30)
	at com.example.DeadlockExample$$Lambda$1/0x0000000800b5a000.run(Unknown Source)
	at java.lang.Thread.run(java.base@17.0.8/Thread.java:833)

"Thread-2":
	at com.example.DeadlockExample.method2(DeadlockExample.java:25)
	- waiting to lock <0x0000000082678902> (a java.lang.Object)
	- locked <0x0000000082678901> (a java.lang.Object)
	at com.example.DeadlockExample.lambda$main$1(DeadlockExample.java:35)
	at com.example.DeadlockExample$$Lambda$2/0x0000000800b5a400.run(Unknown Source)
	at java.lang.Thread.run(java.base@17.0.8/Thread.java:833)

Found 1 deadlock.

# 显示混合模式堆栈（包含本地方法）
$ jstack -m 12345
2023-12-07 16:47:38
Full thread dump OpenJDK 64-Bit Server VM (17.0.8+7-Ubuntu-120.04 mixed mode):

siginfo: si_signo: 11 (SIGSEGV), si_code: 1 (SEGV_MAPERR), si_addr: 0x0000000000000000

Native frames: (J=compiled Java code, j=interpreted, Vv=VM code, C=native code)
C  [libc.so.6+0x18e000]  strlen+0x10
C  [libjava.so+0x1c5d5]  JNU_GetStringPlatformChars+0x35
j  java.lang.System.initProperties(Ljava/util/Properties;)Ljava/util/Properties;+0 java.base@17.0.8
j  java.lang.System.<clinit>()V+23 java.base@17.0.8
v  ~StubRoutines::call_stub
V  [libjvm.so+0x7b5c5c]  JavaCalls::call_helper(JavaValue*, methodHandle const&, JavaCallArguments*, Thread*)+0x4ac
V  [libjvm.so+0x7b57a1]  JavaCalls::call_static(JavaValue*, Klass*, Symbol*, Symbol*, Thread*)+0x101
V  [libjvm.so+0x912c5d]  initialize_class_outputstream(JNIEnviron

Java Threads: ( => current thread )
=>0x00007f8b48012800 JavaThread "main" [_thread_in_native, id=12347, stack(0x00007f8b50c4b000,0x00007f8b50d4c000)]
  0x00007f8b48014800 JavaThread "Reference Handler" daemon [_thread_blocked, id=12348, stack(0x00007f8b4f9fa000,0x00007f8b4fafb000)]
  0x00007f8b48016800 JavaThread "Finalizer" daemon [_thread_blocked, id=12349, stack(0x00007f8b4f8f9000,0x00007f8b4f9fa000)]
```

### 内容解析
- **线程信息**: 显示每个线程的ID、优先级、状态
- **堆栈跟踪**: 显示线程的调用堆栈信息
- **锁信息**: 显示线程持有的锁和等待的锁
- **死锁检测**: 自动检测并报告死锁情况
- **本地帧**: 显示JNI调用的本地方法堆栈

### 常用参数详解
- `<pid>`: 指定要分析的Java进程ID
- `-l`: 长列表格式，显示额外的锁信息
- `-m`: 混合模式，同时显示Java和本地方法堆栈
- `-F`: 强制模式，当正常模式失败时使用
- `-h`: 显示帮助信息

### 注意事项
- 需要与目标JVM相同用户权限
- 频繁采样可能影响应用性能
- 生产环境使用时要注意时机选择
- 结合其他工具进行综合分析

### 安全风险
- ⚠️ 堆栈信息可能暴露敏感业务逻辑
- ⚠️ 进程信息采集可能影响系统性能
- ⚠️ Root权限执行可能带来系统安全风险
- ⚠️ 详细的应用状态信息可能被恶意利用

## 7. jmap (Java内存映射工具)

### 用途
`jmap` 用于生成Java进程的堆内存快照（heap dump），分析内存使用情况和检测内存泄漏问题。

### 输出示例
```bash
# 生成堆内存快照
$ jmap -dump:format=b,file=heap_dump.hprof 12345
Dumping heap to /home/user/heap_dump.hprof ...
Heap dump file created

# 查看堆内存摘要
$ jmap -heap 12345
Attaching to process ID 12345, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 17.0.8+7-Ubuntu-120.04

using thread-local object allocation.
Garbage-First (G1) GC with 8 thread(s)

Heap Configuration:
   MinHeapFreeRatio         = 40
   MaxHeapFreeRatio         = 70
   MaxHeapSize              = 2147483648 (2048.0MB)
   NewSize                  = 1363144 (1.2999954223632812MB)
   MaxNewSize               = 1275068416 (1216.0MB)
   OldSize                  = 5452592 (5.1999969482421875MB)
   NewRatio                 = 2
   SurvivorRatio            = 8
   MetaspaceSize            = 21807104 (20.796875MB)
   CompressedClassSpaceSize = 1073741824 (1024.0MB)
   MaxMetaspaceSize         = 17592186044415 MB
   G1HeapRegionSize         = 1048576 (1.0MB)

Heap Usage:
G1 Heap:
    regions  = 2048
    capacity = 2147483648 (2048.0MB)
    used     = 838860800 (800.0MB)
    free     = 1308622848 (1248.0MB)
    37.1875% used

G1 Young Generation:
Eden Space:
    regions  = 512
    capacity = 536870912 (512.0MB)
    used     = 536870912 (512.0MB)
    free     = 0 (0.0MB)
    100.0% used
Survivor Space:
    regions  = 64
    capacity = 67108864 (64.0MB)
    used     = 67108864 (64.0MB)
    free     = 0 (0.0MB)
    100.0% used
G1 Old Generation:
    regions  = 256
    capacity = 1543503872 (1472.0MB)
    used     = 235019264 (224.0MB)
    free     = 1308484608 (1248.0MB)
    15.226340760869565% used

Metaspace       used 45678K, capacity 46540K, committed 46848K, reserved 1088512K
  class space    used 5678K, capacity 6120K, committed 6272K, reserved 1048576K

# 查看对象直方图
$ jmap -histo 12345 | head -20
 num     #instances         #bytes  class name (module)
-------------------------------------------------------
   1:         15434        1234720  [C (java.base@17.0.8)
   2:          8765         987654  java.lang.String (java.base@17.0.8)
   3:          5432         654321  [Ljava.lang.Object; (java.base@17.0.8)
   4:          4321         432100  java.util.HashMap$Node (java.base@17.0.8)
   5:          3210         385200  java.lang.Class (java.base@17.0.8)
   6:          2109         337440  java.util.ArrayList (java.base@17.0.8)
   7:          1098         263520  java.util.HashMap (java.base@17.0.8)
   8:           987         236880  com.example.User (my-project)
   9:           876         210240  com.example.Order (my-project)
  10:           765         183600  java.util.concurrent.ConcurrentHashMap (java.base@17.0.8)
  11:           654         156960  java.lang.reflect.Method (java.base@17.0.8)
  12:           543         130320  java.util.LinkedList$Node (java.base@17.0.8)
  13:           432         103680  java.util.HashSet (java.base@17.0.8)
  14:           321          77040  java.lang.Integer (java.base@17.0.8)
  15:           210          50400  java.lang.Long (java.base@17.0.8)
  16:           198          47520  java.util.LinkedHashMap$Entry (java.base@17.0.8)
  17:           187          44880  java.util.TreeMap$Entry (java.base@17.0.8)
  18:           176          42240  java.util.Hashtable$Entry (java.base@17.0.8)
  19:           165          39600  java.math.BigDecimal (java.base@17.0.8)

# 查看永久代/元空间使用情况
$ jmap -permstat 12345
Attaching to process ID 12345, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 17.0.8+7-Ubuntu-120.04

Finding object size using Printezis bits and skipping over...

Iterating over heap. This may take a while...
Total iterations: 0; saw 0 objects

# 强制执行垃圾回收后dump
$ jmap -dump:format=b,live,file=live_heap_dump.hprof 12345
Dumping heap to /home/user/live_heap_dump.hprof ...
Heap dump file created
```

### 内容解析
- **堆配置**: 显示JVM堆内存的各项配置参数
- **内存使用**: 显示各代内存的使用情况和利用率
- **对象统计**: 显示各类对象的实例数和占用字节数
- **类加载**: 显示Metaspace和类空间的使用情况
- **快照文件**: 生成可用于进一步分析的heap dump文件

### 常用参数详解
- `-heap <pid>`: 显示堆内存使用情况
- `-histo <pid>`: 显示对象直方图统计
- `-dump:<options> <pid>`: 生成堆内存快照
- `-permstat <pid>`: 显示永久代统计信息
- `format=b`: 指定二进制格式
- `file=<filename>`: 指定输出文件名
- `live`: 只dump存活的对象

### 注意事项
- heap dump文件通常较大，需要充足磁盘空间
- 生成dump可能暂时暂停应用运行
- 生产环境应在低峰期执行
- 定期清理旧的dump文件避免磁盘占满

### 安全风险
- ⚠️ heap dump文件包含敏感数据（密码、个人信息等）
- ⚠️ dump过程可能暴露内存中的敏感信息
- ⚠️ 大文件传输和存储存在安全风险
- ⚠️ 未授权访问dump文件可能导致数据泄露

## 8. jstat (JVM统计监控工具)

### 用途
`jstat` 用于监控JVM的垃圾回收、类加载、编译等运行时统计信息，帮助分析JVM性能问题。

### 输出示例
```bash
# 查看类加载统计
$ jstat -class 12345
Loaded  Bytes  Unloaded  Bytes     Time
  8765 12345.6       12    123.4    5.67

# 查看编译统计
$ jstat -compiler 12345
Compiled Failed Invalid   Time   FailedType FailedMethod
    1234      5        2   67.89          1 com/example/Service method1

# 查看垃圾回收统计
$ jstat -gc 12345
 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT    CGC    CGCT     GCT
1024.0 1024.0  0.0   512.0   8192.0   4096.0   16384.0    8192.0   4096.0 3845.2 512.0  487.3     25    0.456     3    0.789    12    0.234    1.479

# 查看详细的GC容量信息
$ jstat -gccapacity 12345
 NGCMN    NGCMX     NGC     S0C   S1C       EC      OGCMN      OGCMX       OGC         OC       MCMN     MCMX      MC     CCSMN    CCSMX     CCSC    YGC    FGC
 10240.0 128000.0  20480.0 1024.0 1024.0   8192.0   20480.0   256000.0    40960.0    40960.0    0.0 1152000.0   4096.0      0.0 1048576.0    512.0     25     3

# 查看GC详细统计
$ jstat -gcutil 12345
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT    CGC    CGCT     GCT
  0.00  50.00  50.00  50.00  93.87  95.18     25    0.456     3    0.789    12    0.234    1.479

# 实时监控GC（每2秒输出一次，共10次）
$ jstat -gc 12345 2s 10
 S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT    CGC    CGCT     GCT
1024.0 1024.0  0.0   512.0   8192.0   4096.0   16384.0    8192.0   4096.0 3845.2 512.0  487.3     25    0.456     3    0.789    12    0.234    1.479
1024.0 1024.0  0.0   512.0   8192.0   6144.0   16384.0    8192.0   4096.0 3845.2 512.0  487.3     25    0.456     3    0.789    12    0.234    1.479
# ... 后续8次输出 ...

# 查看JIT编译统计
$ jstat -printcompilation 12345
Compiled  Size  Type Method
    1234    123    1 com/example/Service method1
    1235     89    1 com/example/Util helperMethod
    1236    234    1 com/example/DataProcessor processData

# 查看老年代GC统计
$ jstat -gcold 12345
   MC       MU      CCSC     CCSU     OC       OU       YGC    FGC    FGCT     GCT
 4096.0   3845.2   512.0    487.3   16384.0   8192.0     25     3    0.789    1.479

# 查看元空间统计
$ jstat -gcmetacapacity 12345
   MCMN       MCMX        MC       CCSMN      CCSMX       CCSC     YGC   FGC    FGCT     GCT
       0.0  1152000.0    4096.0        0.0  1048576.0      512.0    25     3    0.789    1.479
```

### 内容解析
- **内存区域**: Eden、Survivor、Old、Metaspace等各区域容量和使用情况
- **GC统计**: 年轻代GC、老年代GC的次数和耗时
- **类加载**: 已加载类的数量和卸载情况
- **编译信息**: JIT编译的方法统计
- **实时监控**: 持续监控JVM运行状态变化

### 常用参数详解
- `-class <pid>`: 显示类加载统计
- `-compiler <pid>`: 显示JIT编译统计
- `-gc <pid>`: 显示基本GC统计
- `-gcutil <pid>`: 显示GC使用率百分比
- `-gccapacity <pid>`: 显示GC容量信息
- `-gcold <pid>`: 显示老年代GC统计
- `-gcmetacapacity <pid>`: 显示元空间容量统计
- `<interval> <count>`: 指定采样间隔和次数

### 注意事项
- 监控频率不宜过高避免影响性能
- 结合应用负载情况分析统计数据
- 长期监控有助于发现性能趋势
- 注意区分正常波动和异常情况

### 安全风险
- ⚠️ 监控数据可能暴露应用内部实现细节
- ⚠️ 频繁监控可能影响生产环境性能
- ⚠️ 未授权的监控访问可能带来安全风险
- ⚠️ 监控脚本可能存在执行风险

---

**总结**: 以上是Java开发常用的CLI工具详解。在生产环境中使用这些工具时，务必注意安全管理、性能影响和数据保护，确保Java应用的稳定运行和系统安全。