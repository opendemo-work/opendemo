package com.opendemo.java.io;

import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class StreamReaderWriter {

    public static String readFileWithEncoding(Path path, Charset charset) throws IOException {
        StringBuilder content = new StringBuilder();
        try (InputStream inputStream = Files.newInputStream(path);
             InputStreamReader reader = new InputStreamReader(inputStream, charset);
             BufferedReader bufferedReader = new BufferedReader(reader)) {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                content.append(line).append("\n");
            }
        }
        return content.toString();
    }

    public static void writeFileWithEncoding(Path path, String content, Charset charset) throws IOException {
        try (OutputStream outputStream = Files.newOutputStream(path);
             OutputStreamWriter writer = new OutputStreamWriter(outputStream, charset);
             BufferedWriter bufferedWriter = new BufferedWriter(writer)) {
            bufferedWriter.write(content);
        }
    }

    public static byte[] convertStringToBytes(String text, Charset charset) {
        return text.getBytes(charset);
    }

    public static String convertBytesToString(byte[] bytes, Charset charset) {
        return new String(bytes, charset);
    }

    public static void demonstrateEncodingConversion() throws IOException {
        Path tempFile = Files.createTempFile("encoding-test-", ".txt");
        String chineseText = "你好，世界！Hello, World!";

        writeFileWithEncoding(tempFile, chineseText, StandardCharsets.UTF_8);
        String readBack = readFileWithEncoding(tempFile, StandardCharsets.UTF_8);

        System.out.println("原始文本: " + chineseText);
        System.out.println("读取文本: " + readBack.trim());

        byte[] utf8Bytes = convertStringToBytes(chineseText, StandardCharsets.UTF_8);
        System.out.println("UTF-8字节数: " + utf8Bytes.length);

        String restored = convertBytesToString(utf8Bytes, StandardCharsets.UTF_8);
        System.out.println("还原文本: " + restored);

        Files.deleteIfExists(tempFile);
    }

    public static void main(String[] args) throws IOException {
        System.out.println("=== 字符编码与转换流演示 ===\n");
        demonstrateEncodingConversion();
    }
}
