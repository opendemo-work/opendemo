package com.example.demo.controller;

import com.example.demo.service.FileStorageService;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/files")
public class FileController {

    private final FileStorageService fileStorageService;

    public FileController(FileStorageService fileStorageService) {
        this.fileStorageService = fileStorageService;
    }

    @PostMapping("/upload")
    public ResponseEntity<Map<String, String>> uploadFile(@RequestParam("file") MultipartFile file) {
        Map<String, String> result = new HashMap<>();
        try {
            String storedFilename = fileStorageService.storeFile(file);
            result.put("message", "文件上传成功");
            result.put("originalFilename", file.getOriginalFilename());
            result.put("storedFilename", storedFilename);
            result.put("size", String.valueOf(file.getSize()));
            result.put("contentType", file.getContentType());
            return ResponseEntity.ok(result);
        } catch (IOException e) {
            result.put("error", "上传失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(result);
        }
    }

    @GetMapping("/download/{filename}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String filename) {
        try {
            byte[] data = fileStorageService.loadFile(filename);
            String contentType = fileStorageService.getContentType(filename);
            ByteArrayResource resource = new ByteArrayResource(data);

            return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(contentType))
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                            "attachment; filename=\"" + URLEncoder.encode(filename, StandardCharsets.UTF_8) + "\"")
                    .body(resource);
        } catch (IOException e) {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/list")
    public ResponseEntity<List<Map<String, Object>>> listFiles() {
        try {
            return ResponseEntity.ok(fileStorageService.listFiles());
        } catch (IOException e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @DeleteMapping("/{filename}")
    public ResponseEntity<Map<String, String>> deleteFile(@PathVariable String filename) {
        Map<String, String> result = new HashMap<>();
        try {
            boolean deleted = fileStorageService.deleteFile(filename);
            if (deleted) {
                result.put("message", "文件删除成功");
                return ResponseEntity.ok(result);
            } else {
                result.put("error", "文件不存在");
                return ResponseEntity.notFound().build();
            }
        } catch (IOException e) {
            result.put("error", "删除失败: " + e.getMessage());
            return ResponseEntity.internalServerError().body(result);
        }
    }
}
