<!-- TEMPLATE: 待完善 - 本 README 包含自动生成的模板内容，需要人工精修 -->

# File Upload 文件上传演示

> 深入理解 Spring Boot 文件上传，掌握 MultipartFile、文件存储、下载和校验

## 🎯 学习目标

- ✅ 掌握 MultipartFile 文件上传处理
- ✅ 学会文件存储服务的设计和实现
- ✅ 理解文件上传大小限制配置
- ✅ 掌握文件下载、列表和删除功能
- ✅ 了解文件上传安全校验

---

## 📚 核心概念

| 概念 | 说明 |
|------|------|
| **MultipartFile** | Spring 封装的上传文件接口 |
| **multipart/form-data** | 文件上传的 HTTP 编码类型 |
| **MultipartResolver** | 多部分请求解析器 |
| **MultipartConfig** | 文件上传大小和阈值配置 |

---

## 🛠️ 文件上传流程

```
┌────────────────────────────────────────────────────┐
│              文件上传处理流程                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  客户端 POST (multipart/form-data)                 │
│       ↓                                            │
│  MultipartResolver 解析请求                         │
│       ↓                                            │
│  Controller 接收 MultipartFile                     │
│       ↓                                            │
│  ┌──────────────────┐                              │
│  │ FileStorageService│                              │
│  │  ├─ 校验文件       │                              │
│  │  ├─ 生成文件名     │                              │
│  │  ├─ 创建目录       │                              │
│  │  └─ 存储文件       │                              │
│  └──────────────────┘                              │
│       ↓                                            │
│  返回上传结果                                       │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 💻 核心代码

### 1. FileStorageService 文件存储服务

```java
@Service
public class FileStorageService {

    public String storeFile(MultipartFile file) throws IOException {
        validateFile(file);

        Path uploadPath = getUploadPath();
        Files.createDirectories(uploadPath);

        String uniqueFilename = generateUniqueFilename(file.getOriginalFilename());
        Path targetPath = uploadPath.resolve(uniqueFilename);

        Files.copy(file.getInputStream(), targetPath, REPLACE_EXISTING);
        return uniqueFilename;
    }

    private void validateFile(MultipartFile file) throws IOException {
        if (file.isEmpty()) throw new IOException("上传文件不能为空");
        if (file.getSize() > MAX_FILE_SIZE) throw new IOException("文件大小超过限制");
        if (file.getOriginalFilename().contains("..")) throw new IOException("文件名不合法");
    }
}
```

### 2. FileController 文件上传控制器

```java
@RestController
@RequestMapping("/api/files")
public class FileController {

    @PostMapping("/upload")
    public ResponseEntity<Map<String, String>> uploadFile(
            @RequestParam("file") MultipartFile file) {
        String storedFilename = fileStorageService.storeFile(file);
        // 返回上传结果
    }

    @GetMapping("/download/{filename}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String filename) {
        byte[] data = fileStorageService.loadFile(filename);
        // 返回文件流
    }
}
```

### 3. application.yml 配置

```yaml
spring:
  servlet:
    multipart:
      enabled: true
      max-file-size: 10MB
      max-request-size: 20MB
      file-size-threshold: 2KB

file:
  upload-dir: ./uploads
```

---

## 🚀 快速开始

### 1. 启动应用

```bash
cd java/file-upload-demo
mvn spring-boot:run
```

### 2. 上传文件

```bash
# 创建测试文件
echo "Hello World" > test.txt

# 上传文件
curl -X POST -F "file=@test.txt" http://localhost:8080/api/files/upload

# 上传图片
curl -X POST -F "file=@photo.jpg" http://localhost:8080/api/files/upload
```

### 3. 管理文件

```bash
# 查看文件列表
curl http://localhost:8080/api/files/list

# 下载文件
curl -O http://localhost:8080/api/files/download/test_1234567890.txt

# 删除文件
curl -X DELETE http://localhost:8080/api/files/download/test_1234567890.txt
```

---

## 📁 项目结构

```
file-upload-demo/
├── src/main/java/com/example/demo/
│   ├── FileUploadApplication.java              # 应用入口
│   ├── controller/
│   │   └── FileController.java                 # 文件上传/下载控制器
│   └── service/
│       └── FileStorageService.java             # 文件存储服务
├── src/main/resources/
│   └── application.yml                         # 应用配置
├── src/test/java/com/example/demo/
│   └── FileUploadDemoTest.java                 # 单元测试
├── pom.xml
└── README.md
```

---

## 📋 API 端点

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | /api/files/upload | 上传文件 |
| GET | /api/files/download/{filename} | 下载文件 |
| GET | /api/files/list | 列出已上传文件 |
| DELETE | /api/files/{filename} | 删除文件 |

---

## 🔧 安全注意事项

- 校验文件大小限制，防止超大文件攻击
- 检查文件名，防止路径穿越（`../`）
- 限制上传文件的类型和扩展名
- 使用唯一文件名避免覆盖
- 上传目录不应在 Web 可直接访问的路径下

---

## 🧪 测试

```bash
mvn test
```

---

## 📚 扩展学习

- [Spring MVC Web](../spring-mvc-web-demo/) - REST API 基础
- [Exception Handling](../exception-handling-demo/) - 异常处理

---

*最后更新：2026年4月*

## 📖 核心概念

### 1. 基本概念

本节介绍本案例涉及的核心概念。

### 2. 适用场景

- 场景 1：学习与实验
- 场景 2：工程实践
- 场景 3：面试准备

## 💻 代码示例

### 基本用法

```bash
# 请根据实际案例替换
./scripts/demo.sh
```
