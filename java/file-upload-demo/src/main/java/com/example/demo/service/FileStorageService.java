package com.example.demo.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

@Service
public class FileStorageService {

    private static final Logger logger = LoggerFactory.getLogger(FileStorageService.class);
    private static final long MAX_FILE_SIZE = 10 * 1024 * 1024;

    @Value("${file.upload-dir:./uploads}")
    private String uploadDir;

    public String storeFile(MultipartFile file) throws IOException {
        validateFile(file);

        Path uploadPath = getUploadPath();
        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        String originalFilename = file.getOriginalFilename();
        String uniqueFilename = generateUniqueFilename(originalFilename);
        Path targetPath = uploadPath.resolve(uniqueFilename);

        Files.copy(file.getInputStream(), targetPath, StandardCopyOption.REPLACE_EXISTING);
        logger.info("文件存储成功: {} -> {}", originalFilename, targetPath);

        return uniqueFilename;
    }

    public byte[] loadFile(String filename) throws IOException {
        Path filePath = getUploadPath().resolve(filename);
        if (!Files.exists(filePath)) {
            throw new IOException("文件不存在: " + filename);
        }
        return Files.readAllBytes(filePath);
    }

    public boolean deleteFile(String filename) throws IOException {
        Path filePath = getUploadPath().resolve(filename);
        return Files.deleteIfExists(filePath);
    }

    public List<Map<String, Object>> listFiles() throws IOException {
        Path uploadPath = getUploadPath();
        List<Map<String, Object>> fileList = new ArrayList<>();

        if (!Files.exists(uploadPath)) {
            return fileList;
        }

        try (Stream<Path> paths = Files.list(uploadPath)) {
            paths.filter(Files::isRegularFile).forEach(path -> {
                Map<String, Object> fileInfo = new HashMap<>();
                fileInfo.put("name", path.getFileName().toString());
                try {
                    fileInfo.put("size", Files.size(path));
                    fileInfo.put("lastModified", Files.getLastModifiedTime(path).toString());
                } catch (IOException e) {
                    logger.error("获取文件信息失败: {}", path, e);
                }
                fileList.add(fileInfo);
            });
        }

        return fileList;
    }

    public String getContentType(String filename) {
        try {
            Path filePath = getUploadPath().resolve(filename);
            return Files.probeContentType(filePath);
        } catch (IOException e) {
            return "application/octet-stream";
        }
    }

    private void validateFile(MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            throw new IOException("上传文件不能为空");
        }
        if (file.getSize() > MAX_FILE_SIZE) {
            throw new IOException("文件大小超过限制 (最大10MB)");
        }
        String originalFilename = file.getOriginalFilename();
        if (originalFilename == null || originalFilename.contains("..")) {
            throw new IOException("文件名不合法");
        }
    }

    private Path getUploadPath() {
        String datePath = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"));
        return Paths.get(uploadDir).resolve(datePath);
    }

    private String generateUniqueFilename(String originalFilename) {
        String timestamp = String.valueOf(System.currentTimeMillis());
        int dotIndex = originalFilename.lastIndexOf('.');
        if (dotIndex > 0) {
            String name = originalFilename.substring(0, dotIndex);
            String ext = originalFilename.substring(dotIndex);
            return name + "_" + timestamp + ext;
        }
        return originalFilename + "_" + timestamp;
    }
}
