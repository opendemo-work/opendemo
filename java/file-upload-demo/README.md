# File Upload Demo

文件上传演示项目，演示Spring Boot的文件上传处理。

## 技术栈

- Spring Boot 2.7
- MultipartFile

## 测试接口

```bash
curl -X POST -F "file=@test.txt" http://localhost:8080/api/files/upload
```
