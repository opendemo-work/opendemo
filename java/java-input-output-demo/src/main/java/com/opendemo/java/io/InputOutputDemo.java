package com.opendemo.java.io;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;

public class InputOutputDemo {

    public static void main(String[] args) throws IOException {
        System.out.println("=== Java输入输出演示 ===\n");

        demonstrateFileReadWrite();
        demonstrateBufferedStreams();
        demonstrateNIO();
    }

    private static void demonstrateFileReadWrite() throws IOException {
        System.out.println("1. 文件读写演示:");
        Path tempDir = Files.createTempDirectory("io-demo-");
        Path filePath = tempDir.resolve("test.txt");

        Files.write(filePath, "Hello, Java IO!\n".getBytes(StandardCharsets.UTF_8),
                StandardOpenOption.CREATE, StandardOpenOption.WRITE);
        Files.write(filePath, "Second line\n".getBytes(StandardCharsets.UTF_8),
                StandardOpenOption.APPEND);

        List<String> lines = Files.readAllLines(filePath, StandardCharsets.UTF_8);
        System.out.println("文件内容:");
        lines.forEach(line -> System.out.println("  " + line));

        byte[] bytes = Files.readAllBytes(filePath);
        System.out.println("文件字节数: " + bytes.length);

        Files.deleteIfExists(filePath);
        Files.deleteIfExists(tempDir);
        System.out.println();
    }

    private static void demonstrateBufferedStreams() throws IOException {
        System.out.println("2. 缓冲流演示:");
        Path tempDir = Files.createTempDirectory("buffered-demo-");
        Path filePath = tempDir.resolve("buffered.txt");

        try (BufferedWriter writer = Files.newBufferedWriter(filePath, StandardCharsets.UTF_8)) {
            writer.write("第一行数据");
            writer.newLine();
            writer.write("第二行数据");
            writer.newLine();
            writer.write("第三行数据");
        }

        try (BufferedReader reader = Files.newBufferedReader(filePath, StandardCharsets.UTF_8)) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("读取: " + line);
            }
        }

        Files.deleteIfExists(filePath);
        Files.deleteIfExists(tempDir);
        System.out.println();
    }

    private static void demonstrateNIO() throws IOException {
        System.out.println("3. NIO演示:");
        Path tempDir = Files.createTempDirectory("nio-demo-");
        Path sourcePath = tempDir.resolve("source.txt");
        Path targetPath = tempDir.resolve("target.txt");

        String content = "NIO file content for demonstration";
        Files.write(sourcePath, content.getBytes(StandardCharsets.UTF_8));

        Files.copy(sourcePath, targetPath, StandardCopyOption.REPLACE_EXISTING);
        System.out.println("文件复制完成: " + Files.exists(targetPath));

        String copiedContent = new String(Files.readAllBytes(targetPath), StandardCharsets.UTF_8);
        System.out.println("复制内容: " + copiedContent);

        System.out.println("源文件大小: " + Files.size(sourcePath) + " bytes");
        System.out.println("目标文件大小: " + Files.size(targetPath) + " bytes");

        Files.deleteIfExists(sourcePath);
        Files.deleteIfExists(targetPath);
        Files.deleteIfExists(tempDir);
        System.out.println();
    }

    public static List<String> readAllLines(String filePath) throws IOException {
        return Files.readAllLines(Paths.get(filePath), StandardCharsets.UTF_8);
    }

    public static void writeAllLines(String filePath, List<String> lines) throws IOException {
        Files.write(Paths.get(filePath), lines, StandardCharsets.UTF_8,
                StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
    }
}
