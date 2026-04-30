package com.example.demo;

import com.example.demo.service.FileStorageService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockMultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class FileUploadDemoTest {

    private FileStorageService fileStorageService;
    private final String testUploadDir = "./test-uploads";

    @BeforeEach
    void setUp() throws IOException {
        fileStorageService = new FileStorageService();
        cleanupTestDir();
    }

    private void cleanupTestDir() throws IOException {
        Path dir = Paths.get(testUploadDir);
        if (Files.exists(dir)) {
            Files.walk(dir)
                    .sorted((a, b) -> b.compareTo(a))
                    .forEach(p -> {
                        try { Files.deleteIfExists(p); } catch (IOException e) { }
                    });
        }
    }

    @Test
    void testStoreAndLoadFile() throws IOException {
        MockMultipartFile file = new MockMultipartFile(
                "file", "test.txt", "text/plain", "Hello World".getBytes());
        String stored = fileStorageService.storeFile(file);
        assertNotNull(stored);
        assertTrue(stored.contains("test"));
        assertTrue(stored.endsWith(".txt"));
    }

    @Test
    void testStoreEmptyFile() {
        MockMultipartFile emptyFile = new MockMultipartFile(
                "file", "empty.txt", "text/plain", new byte[0]);
        assertThrows(IOException.class, () -> fileStorageService.storeFile(emptyFile));
    }

    @Test
    void testStoreFileWithInvalidName() {
        MockMultipartFile file = new MockMultipartFile(
                "file", "../dangerous.txt", "text/plain", "data".getBytes());
        assertThrows(IOException.class, () -> fileStorageService.storeFile(file));
    }

    @Test
    void testGenerateUniqueFilename() throws IOException {
        MockMultipartFile file1 = new MockMultipartFile(
                "file", "doc.pdf", "application/pdf", "data1".getBytes());
        MockMultipartFile file2 = new MockMultipartFile(
                "file", "doc.pdf", "application/pdf", "data2".getBytes());
        String stored1 = fileStorageService.storeFile(file1);
        String stored2 = fileStorageService.storeFile(file2);
        assertNotEquals(stored1, stored2);
    }

    @Test
    void testListFilesEmpty() throws IOException {
        List<Map<String, Object>> files = fileStorageService.listFiles();
        assertNotNull(files);
    }

    @Test
    void testGetContentType() {
        String contentType = fileStorageService.getContentType("nonexistent.txt");
        assertNotNull(contentType);
    }

    @Test
    void testLoadNonExistentFile() {
        assertThrows(IOException.class, () -> fileStorageService.loadFile("nonexistent_file.txt"));
    }

    @Test
    void testDeleteNonExistentFile() throws IOException {
        boolean result = fileStorageService.deleteFile("nonexistent_file.txt");
        assertFalse(result);
    }

    @Test
    void testMockMultipartFileCreation() {
        MockMultipartFile file = new MockMultipartFile(
                "file", "test.txt", "text/plain", "content".getBytes());
        assertEquals("test.txt", file.getOriginalFilename());
        assertEquals("text/plain", file.getContentType());
        assertEquals(7, file.getSize());
        assertFalse(file.isEmpty());
    }
}
